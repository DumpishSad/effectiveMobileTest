from django.contrib import admin
from django.urls import path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # Административная панель Django.

    path('', views.home, name='home'),
    # Главная страница приложения.

    path('orders/', views.order_list, name='order_list'),
    # Отображение списка всех заказов с возможностью поиска и фильтрации.

    path('create/', views.order_create, name='order_create'),
    # Создание нового заказа. Обработка формы с вводом данных.

    path('delete/<int:order_id>/', views.order_delete, name='order_delete'),
    # Удаление конкретного заказа по его ID.

    path('revenue/', views.calculate_revenue, name='calculate_revenue'),
    # Подсчет общей выручки на основе оплаченных заказов.

    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    # Обновление статуса конкретного заказа (ожидание, готово, оплачено).
]
