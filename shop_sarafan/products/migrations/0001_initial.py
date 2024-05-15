# Generated by Django 5.0.6 on 2024-05-14 18:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(max_length=200, unique=True, verbose_name="Уникальный слаг")),
                ("image", models.ImageField(upload_to="products/images/categories", verbose_name="Изображение")),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(max_length=200, unique=True, verbose_name="Уникальный слаг")),
                ("image_large", models.ImageField(upload_to="products/images/products/large", verbose_name="Большое изображение")),
                ("image_medium", models.ImageField(upload_to="products/images/products/medium", verbose_name="Среднее изображение")),
                ("image_small", models.ImageField(upload_to="products/images/products/small", verbose_name="Маленькое изображение")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)], verbose_name="Цена")),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "Продукты",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="shopping_cart", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={
                "verbose_name": "продуктовая корзина",
                "verbose_name_plural": "Продуктовые корзины",
                "ordering": ("user",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingCartProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32000)], verbose_name="Количество")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="products.product", verbose_name="Продукт")),
                ("shopping_cart", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products_shopping_cart", to="products.shoppingcart", verbose_name="Продуктовая корзина")),
            ],
            options={
                "unique_together": {("shopping_cart", "product")},
            },
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="product",
            field=models.ManyToManyField(related_name="in_shopping_cart", through="products.ShoppingCartProduct", to="products.product", verbose_name="Продукт"),
        ),
        migrations.CreateModel(
            name="Subcategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(max_length=200, unique=True, verbose_name="Уникальный слаг")),
                ("image", models.ImageField(upload_to="products/images/subcategories", verbose_name="Изображение")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subcategories", to="products.category", verbose_name="Категория")),
            ],
            options={
                "verbose_name": "подкатегория",
                "verbose_name_plural": "Подкатегории",
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="product",
            name="subcategory",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="products.subcategory", verbose_name="Подкатегория"),
        ),
    ]