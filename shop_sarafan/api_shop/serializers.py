from django.db.models import F, Sum
from rest_framework import serializers

from products.models import (MAX_AMOUNT_PRODUCT, MIN_AMOUNT_PRODUCT, MIN_PRICE,
                             Category, Product, ShoppingCart,
                             ShoppingCartProduct, Subcategory)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image")


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Subcategory
        fields = ("id", "name", "slug", "category", "image")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    category = serializers.SerializerMethodField()
    subcategory = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )
    images = serializers.SerializerMethodField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=MIN_PRICE
    )

    class Meta:
        """Конфигурация сериализатора для модели Product."""
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "subcategory",
            "price",
            "images"
        )

    @staticmethod
    def get_category(obj):
        """Получить название категории продукта."""
        return obj.subcategory.category.name

    @staticmethod
    def get_images(obj):
        """Получить список URL-адресов изображений продукта."""
        return [obj.image_large.url, obj.image_medium.url, obj.image_small.url]


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка продуктов в корзине."""
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    amount = serializers.IntegerField(
        max_value=MAX_AMOUNT_PRODUCT,
        min_value=MIN_AMOUNT_PRODUCT
    )
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Конфигурация сериализатора для модели ShoppingCartProduct."""
        model = ShoppingCartProduct
        fields = ("product", "amount", "total_price")

    @staticmethod
    def get_total_price(obj):
        """Получить общую стоимость каждого продукта в корзине."""
        return obj.product.price * obj.amount


class ListShoppingCartSerializer(serializers.Serializer):
    """Сериализатор для отображения общей стоимости и количества продуктов."""
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_amount(self, instance):
        """Получить общее количество продуктов в корзине."""
        request = self.context.get("request")
        user = request.user
        total_amount = ShoppingCart.objects.filter(user=user).aggregate(
            total_amount=Sum("shopping_cart_products__amount")
        )["total_amount"]
        return total_amount

    def get_total_price(self, instance):
        """Получить общую стоимость продуктов в корзине."""
        request = self.context.get("request")
        user = request.user
        total_price = ShoppingCart.objects.filter(user=user).annotate(
            product_total_price=F(
                "shopping_cart_products__product__price"
            ) * F(
                "shopping_cart_products__amount"
            )
        ).aggregate(total_price=Sum("product_total_price"))["total_price"]
        return total_price
