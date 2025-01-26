import json
from typing import List, Dict, Any
from django.contrib import messages
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from django.db.models import Sum

# Словарь для перевода статусов с русского на английский
STATUS_TRANSLATIONS: Dict[str, str] = {
    'в ожидании': 'pending',
    'готово': 'ready',
    'оплачено': 'paid',
}

def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображение списка заказов с поиском и фильтрацией.

    Пользователь может:
    1. Искать заказы по номеру стола, введя его в поле поиска.
    2. Искать заказы по статусу (например, "в ожидании", "готово", "оплачено").
    3. Фильтровать заказы по выбранному статусу через выпадающий список.

    Дополнительно:
    - Все найденные заказы включают детализированные позиции и общую сумму.
    - Если ввод некорректен, пользователю показываются сообщения об ошибках.

    :param request: HTTP-запрос с параметрами поиска (query) и фильтрации (status).
    :return: Ответ с HTML-страницей, содержащей список заказов.
    """
    query: str = request.GET.get('query', '').strip().lower()
    status_filter: str = request.GET.get('status', '').strip().lower()
    orders = Order.objects.all()
    errors: List[str] = []

    if query:
        try:
            table_number = int(query)
            orders = orders.filter(table_number=table_number)
        except ValueError:
            status_key = STATUS_TRANSLATIONS.get(query)
            if status_key:
                orders = orders.filter(status=status_key)
            else:
                errors.append(f"Некорректный запрос: '{query}'. Попробуйте ввести номер стола или статус заказа.")

    if status_filter:
        if status_filter in STATUS_TRANSLATIONS.values():
            orders = orders.filter(status=status_filter)
        else:
            errors.append(f"Некорректный статус: '{status_filter}'. Попробуйте выбрать правильный статус.")

    for order in orders:
        items: List[str] = []
        total_price: int = 0
        if order.items:
            for item in order.items.split(','):
                try:
                    name, price = item.split(':')
                    items.append(name.strip())
                    total_price += int(price.strip())
                except ValueError:
                    continue
        order.parsed_items = items
        order.total_price = total_price

    for error in errors:
        messages.error(request, error)

    return render(request, 'order_list.html', {
        'orders': orders,
        'query': query,
        'status_filter': status_filter,
    })


def order_create(request: HttpRequest) -> HttpResponse:
    """
    Создание нового заказа с проверкой введенных данных.

    Валидация:
    - Номер стола должен быть числом.
    - Формат блюд: "название:цена". Несколько блюд разделяются запятой.
      Пример: "Блюдо1:100, Блюдо2:200".

    Поведение:
    - Если данные корректны, заказ сохраняется, и пользователь перенаправляется
      на список заказов.
    - Если есть ошибки, пользователю отображаются соответствующие сообщения.

    :param request: HTTP-запрос с данными о новом заказе (POST).
    :return: HTML-страница с формой или редирект на список заказов.
    """
    if request.method == 'POST':
        table_number: str = request.POST.get('table_number')
        items: str = request.POST.get('items')
        errors: List[str] = []

        if not table_number.isdigit():
            errors.append("Номер стола должен быть числом.")

        parsed_items = items.split(",")
        valid_items = []
        for item in parsed_items:
            parts = item.split(":")
            if len(parts) == 2 and parts[1].isdigit():
                valid_items.append(item.strip())
            else:
                errors.append(f"Некорректный формат для позиции: '{item}'. Используйте формат 'блюдо:цена'.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'order_form.html', {'table_number': table_number, 'items': items})

        order = Order(table_number=table_number, items=",".join(valid_items))
        order.save()
        messages.success(request, "Заказ успешно добавлен!")
        return redirect('order_list')

    return render(request, 'order_form.html')


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Удаление существующего заказа.

    :param request: HTTP-запрос для удаления.
    :param order_id: ID заказа, который нужно удалить.
    :return: Редирект на страницу списка заказов.
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


def order_update_status(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Изменение статуса заказа.

    Пользователь может обновить статус заказа на один из следующих:
    - "в ожидании"
    - "готово"
    - "оплачено"

    :param request: HTTP-запрос с новым статусом (POST).
    :param order_id: ID заказа, статус которого изменяется.
    :return: Редирект на страницу списка заказов.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status: str = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('order_list')
    return render(request, 'order_update_status.html', {'order': order})


def calculate_revenue(request: HttpRequest) -> HttpResponse:
    """
    Подсчет общей выручки на основе оплаченных заказов.

    Выручка рассчитывается как сумма всех заказов со статусом "оплачено".

    :param request: HTTP-запрос.
    :return: HTML-страница с отображением общей выручки.
    """
    revenue = Order.objects.filter(status='paid').aggregate(total_revenue=Sum('total_price'))['total_revenue']
    return render(request, 'revenue.html', {'revenue': revenue})


def home(request: HttpRequest) -> HttpResponse:
    """
    Отображение главной страницы приложения.

    :param request: HTTP-запрос.
    :return: HTML-страница главной страницы.
    """
    return render(request, 'home.html')


def update_status(request: HttpRequest, order_id: int) -> JsonResponse:
    """
    Изменение статуса заказа через AJAX.

    Используется для обновления статуса в списке заказов без перезагрузки страницы.

    :param request: HTTP-запрос с данными в формате JSON.
    :param order_id: ID заказа, который нужно обновить.
    :return: JSON-ответ с результатом обновления.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status: str = data.get('status')
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
