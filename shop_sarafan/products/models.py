from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

MAX_LEN_SLUG = 200
MAX_LEN_TITLE = 200
MIN_PRICE = 1.0
MIN_AMOUNT_PRODUCT = 1
MAX_AMOUNT_PRODUCT = 32000


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField("Название", unique=True, max_length=MAX_LEN_TITLE)
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=MAX_LEN_SLUG
    )
    image = models.ImageField(
        "Изображение",
        upload_to="products/images/categories"
    )

    class Meta:
        """Конфигурация модели категории."""
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        """Строковое представление объекта категории."""
        return self.name


class Subcategory(models.Model):
    """Модель подкатегории."""
    name = models.CharField("Название", unique=True, max_length=MAX_LEN_TITLE)
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=MAX_LEN_SLUG
    )
    image = models.ImageField(
        "Изображение",
        upload_to="products/images/subcategories"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )

    class Meta:
        """Конфигурация модели подкатегории."""
        verbose_name = "подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ("name",)

    def __str__(self):
        """Строковое представление объекта подкатегории."""
        return self.name


class Product(models.Model):
    """Модель продукта."""
    name = models.CharField("Название", unique=True, max_length=MAX_LEN_TITLE)
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=MAX_LEN_SLUG,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Подкатегория"
    )
    image_large = models.ImageField(
        "Большое изображение",
        upload_to="products/images/products/large"
    )
    image_medium = models.ImageField(
        "Среднее изображение",
        upload_to="products/images/products/medium"
    )
    image_small = models.ImageField(
        "Маленькое изображение",
        upload_to="products/images/products/small"
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(MIN_PRICE)]
    )

    class Meta:
        """Конфигурация модели продукта."""
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

    def __str__(self):
        """Строковое представление объекта продукта."""
        return self.name


class ShoppingCart(models.Model):
    """Модель продуктовой корзины."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """Конфигурация модели продуктовой корзины."""
        verbose_name = "продуктовая корзина"
        verbose_name_plural = "Продуктовые корзины"
        ordering = ("user",)

    def __str__(self):
        """Строковое представление продуктовой корзины."""
        return f"{self.user}"


class ShoppingCartProduct(models.Model):
    """Модель для связующей таблицы между ShoppingCart и Product."""
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name="shopping_cart_products",
        verbose_name="Продуктовая корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Продукт"
    )
    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=[
            MinValueValidator(MIN_AMOUNT_PRODUCT),
            MaxValueValidator(MAX_AMOUNT_PRODUCT)
        ],
        default=0
    )

    class Meta:
        """Конфигурация для связующей таблицы."""
        unique_together = ("shopping_cart", "product")
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзинах"
        ordering = ("product",)

    def __str__(self):
        """Строковое представление продуктов в продуктовой корзине."""
        return f"{self.product.name} - {self.amount} шт."
