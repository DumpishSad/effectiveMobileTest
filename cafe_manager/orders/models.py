from typing import List, Tuple
from django.db import models


class Order(models.Model):
    """
    Модель заказа, представляющая запись в системе управления заказами.

    Атрибуты:
        table_number (int): Номер стола.
        items (str): Список блюд с указанием их цен в формате "блюдо1:цена1,блюдо2:цена2".
        total_price (Decimal): Общая стоимость всех блюд в заказе.
        status (str): Статус заказа, выбирается из доступных вариантов.
        created_at (datetime): Время создания заказа.
    """
    STATUS_CHOICES: List[Tuple[str, str]] = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: int = models.PositiveIntegerField("Номер стола")
    items: str = models.TextField("Список блюд и цены")
    total_price: models.DecimalField = models.DecimalField(
        "Общая стоимость", max_digits=10, decimal_places=2
    )
    status: str = models.CharField(
        "Статус", max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    created_at: models.DateTimeField = models.DateTimeField(
        "Дата создания", auto_now_add=True
    )

    def calculate_total_price(self) -> None:
        """
        Рассчитывает общую стоимость заказа на основе списка блюд.

        Парсит поле `items`, ожидая, что оно имеет формат "блюдо:цена", разделённый запятыми.
        Устанавливает рассчитанную стоимость в атрибут `total_price`.

        Исключения:
            ValueError: Если одно из блюд имеет некорректный формат.
        """
        items_list = self.items.split(",")
        total = sum(float(item.split(":")[1]) for item in items_list)
        self.total_price = total

    def save(self, *args, **kwargs) -> None:
        """
        Переопределение метода сохранения объекта.

        Перед сохранением пересчитывает общую стоимость заказа и вызывает стандартное
        сохранение модели.
        """
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта.

        Формат:
            "Order {id} - Table {table_number}"

        Возвращает:
            str: Строка, представляющая заказ.
        """
        return f"Order {self.id} - Table {self.table_number}"
