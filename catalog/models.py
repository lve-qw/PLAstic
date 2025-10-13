# catalog/models.py
from django.db import models

class Filament(models.Model):
    """Модель для хранения информации о филаменте."""

    brand = models.CharField(max_length=100, verbose_name="Бренд")
    material = models.CharField(max_length=100, verbose_name="Материал")
    diameter = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Диаметр (мм)")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    weight = models.PositiveIntegerField(verbose_name="Вес катушки (г)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена (₽)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="filaments/", blank=True, null=True, verbose_name="Изображение")  # новое поле
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Филамент"
        verbose_name_plural = "Филаменты"
        ordering = ["brand", "material", "color"]

    def __str__(self) -> str:
        return f"{self.brand} {self.material} {self.color} ({self.diameter} мм)"
