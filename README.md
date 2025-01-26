# Effective Mobile Test Project

Проект для управления заказами в кафе. Реализован на Django.

## Функционал
- Управление заказами (создание, удаление, обновление статуса).
- Расчет общей выручки.
- Поиск заказов по номеру стола или статусу.

---

## Установка и развертывание

1. Клонируйте репозиторий

   Склонируйте проект с GitHub:
   ```bash
   git clone https://github.com/ваш_пользователь/название_проекта.git
   cd название_проекта
   ```
   
2. **Создайте и активируйте виртуальное окружение**
      python -m venv .venv
     # Для Windows:
     .venv\Scripts\activate
     # Для macOS/Linux:
     source .venv/bin/activate
3. **Установите зависимости Убедитесь, что находитесь в активированном виртуальном окружении:**
   pip install -r requirements.txt
4. **Примените миграции базы данных Выполните команды для настройки базы данных:**
   python manage.py makemigrations
   python manage.py migrate
5. **Создайте суперпользователя (опционально)**
   python manage.py createsuperuser
6. **Запустите сервер**
   python manage.py runserver 

## Тесты

1. **Для запуска тестов перейдите в /cafe_manager затем запускайте тесты:**
   pytest orders/tests.py
