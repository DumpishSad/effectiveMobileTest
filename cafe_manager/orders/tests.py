import json
import pytest
from .models import Order
from django.urls import reverse
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_order_list_search_by_table_number(client):
    """
    Тест поиска заказа по номеру стола.

    Шаги:
    1. Создаем тестовый заказ с определенным номером стола.
    2. Выполняем GET-запрос с параметром `query`, содержащим номер стола.
    3. Проверяем, что ответ имеет код 200 и заказ присутствует в контексте ответа.
    """
    order = Order.objects.create(table_number=10, items="Блюдо1:100, Блюдо2:200", status="pending")
    url = reverse('order_list')

    response = client.get(url, {'query': '10'})
    assert response.status_code == 200
    assert order in response.context['orders']

@pytest.mark.django_db
def test_order_list_search_by_status(client):
    """
    Тест поиска заказа по статусу.

    Шаги:
    1. Создаем тестовый заказ с определенным статусом.
    2. Выполняем GET-запрос с параметром `query`, содержащим статус заказа.
    3. Проверяем, что ответ имеет код 200 и заказ присутствует в контексте ответа.
    """
    order = Order.objects.create(table_number=10, items="Блюдо1:100", status="pending")
    url = reverse('order_list')

    response = client.get(url, {'query': 'в ожидании'})
    assert response.status_code == 200
    assert order in response.context['orders']

@pytest.mark.django_db
def test_order_create_valid_data(client):
    """
    Тест успешного создания заказа.

    Шаги:
    1. Выполняем POST-запрос с корректными данными.
    2. Проверяем, что после успешного создания происходит редирект.
    3. Убеждаемся, что заказ сохранен в базе данных.
    """
    url = reverse('order_create')
    data = {
        'table_number': '5',
        'items': 'Блюдо1:100, Блюдо2:200'
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert Order.objects.filter(table_number=5).exists()

@pytest.mark.django_db
def test_order_create_invalid_data(client):
    """
    Тест создания заказа с некорректными данными.

    Шаги:
    1. Выполняем POST-запрос с неверными данными (нечисловой номер стола, неправильный формат цены).
    2. Проверяем, что страница с формой отобразилась, а заказ не создан.
    3. Убеждаемся, что соответствующее сообщение об ошибке отображается.
    """
    url = reverse('order_create')
    data = {
        'table_number': 'abc',
        'items': 'Блюдо1:сто'
    }

    response = client.post(url, data)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert "Номер стола должен быть числом." in str(messages[0])

@pytest.mark.django_db
def test_order_delete(client):
    """
    Тест удаления заказа.

    Шаги:
    1. Создаем тестовый заказ.
    2. Выполняем POST-запрос на удаление заказа.
    3. Проверяем, что после удаления происходит редирект.
    4. Убеждаемся, что заказ отсутствует в базе данных.
    """
    order = Order.objects.create(table_number=10, items="Блюдо1:100", status="pending")
    url = reverse('order_delete', args=[order.id])

    response = client.post(url)
    assert response.status_code == 302
    assert not Order.objects.filter(id=order.id).exists()

@pytest.mark.django_db
def test_order_update_status(client):
    """
    Тест обновления статуса заказа через AJAX.

    Шаги:
    1. Создаем тестовый заказ.
    2. Выполняем POST-запрос с новым статусом.
    3. Проверяем, что статус обновлен успешно и возвращен правильный JSON-ответ.
    """
    order = Order.objects.create(table_number=10, items="Блюдо1:100", status="pending")
    url = reverse('update_status', args=[order.id])
    data = {'status': 'ready'}

    response = client.post(url, json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['success'] is True

    order.refresh_from_db()
    assert order.status == 'ready'

@pytest.mark.django_db
def test_calculate_revenue(client):
    """
    Тест подсчета выручки.

    Шаги:
    1. Создаем несколько оплаченных заказов с известными ценами.
    2. Выполняем GET-запрос для получения выручки.
    3. Проверяем, что сумма всех оплаченных заказов рассчитана правильно.
    """
    Order.objects.create(table_number=10, items="Блюдо1:100", status="paid")
    Order.objects.create(table_number=11, items="Блюдо2:200", status="paid")
    url = reverse('calculate_revenue')

    response = client.get(url)
    assert response.status_code == 200
    assert response.context['revenue'] == 300  # Проверяем общую сумму оплаченных заказов
