import os
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .constants import VOLUME_CHOICES

User = get_user_model()

class Product(models.Model):
    """Продукты для продажи."""

    number_of_product = models.IntegerField('Номер продукта', unique=True)
    picture_of_product = models.ImageField('Карточка товара')
    show = models.BooleanField('Показывать ли в каталоге', default=True)

    picture_of_product_small = models.ImageField('Карточка товара для покупки')
    volume = models.IntegerField(
        'Объём',
        choices=VOLUME_CHOICES,
        default=1,
    )
    price = models.DecimalField('Цена', max_digits=6, decimal_places=2)
    name = models.TextField('Название')

    def __str__(self):
        return f"Продукт №{self.number_of_product}"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Korzina(models.Model):
    """Корзина"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='korzina',
        verbose_name='Пользователь'
    )
    products = models.ManyToManyField(
        'Product',
        through='ProductKorzina',
        related_name='korziny',
        verbose_name='Продукты'
    )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class ProductKorzina(models.Model):
    """Связующая между продуктом и корзиной."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    korzina = models.ForeignKey(
        Korzina,
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )
    volume = models.IntegerField(
        'Объём',
        choices=VOLUME_CHOICES,
        default=1,
    )
    quantity = models.IntegerField('Количество', default=1)
    email = models.EmailField('Почта')
    phone = models.CharField('Номер телефона', max_length=13)

    def __str__(self):
        return f'{self.product} в корзине {self.korzina.user.username}'

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'


class Cooperation(models.Model):
    """Сотрдничество."""

    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    country = models.CharField('Страна', max_length=100)
    city = models.CharField('Город', max_length=100)
    number_of_phone = models.CharField('Номер телефона', max_length=13)
    email = models.EmailField('Электронная почта')

    def __str__(self):
        return f'Имя: {self.name}, Фамилия: {self.surname}, Почта: {self.email}, Телефон: {self.number_of_phone}'

    class Meta:
        verbose_name = 'Сотрудничество'
        verbose_name_plural = 'Сотрудничество'


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    """
    Удаляет файл изображения при удалении продукта.
    """
    if instance.picture_of_product:
        if os.path.isfile(instance.picture_of_product.path):
            os.remove(instance.picture_of_product.path)
