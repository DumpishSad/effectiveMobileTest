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
   https://github.com/DumpishSad/effectiveMobileTest.git
   cd cafe_manager
   ```
   
2. Создайте и активируйте виртуальное окружение
      ```bash
      python -m venv .venv
      ```
     Для Windows:
     ```bash
     .venv\Scripts\activate
      ```

     Для macOS/Linux:
     ```bash
     source .venv/bin/activate
      ```
3. Установите зависимости Убедитесь, что находитесь в активированном виртуальном окружении:
   ```bash
   pip install -r requirements.txt
   ```
4. Примените миграции базы данных Выполните команды для настройки базы данных:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Создайте суперпользователя (опционально)
   ```bash
   python manage.py createsuperuser
   ```
6. Запустите сервер
   ```bash
   python manage.py runserver
   ```

## Тесты

1. Для запуска тестов перейдите в /cafe_manager затем запускайте тесты:
   ```bash
   pytest orders/tests.py
   ```
