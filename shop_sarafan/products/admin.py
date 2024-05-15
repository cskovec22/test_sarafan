from django.contrib.admin import ModelAdmin, TabularInline, register

from products.models import (Category, Product, ShoppingCart,
                             ShoppingCartProduct, Subcategory)


@register(Category)
class CategoryAdmin(ModelAdmin):
    """Административный класс для модели Category."""
    list_display = ("pk", "name", "slug")
    search_fields = ("name", "slug")
    list_editable = ("name", "slug")


@register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    """Административный класс для модели Subcategory."""
    list_display = ("pk", "name", "slug", "category")
    search_fields = ("name", "slug")
    list_editable = ("name", "slug", "category")
    list_filter = ("category",)


@register(Product)
class ProductAdmin(ModelAdmin):
    """Административный класс для модели Product."""
    list_display = (
        "pk",
        "name",
        "slug",
        "category",
        "subcategory",
        "price"
    )
    search_fields = ("name", "slug")
    list_editable = ("name", "slug", "subcategory", "price")
    list_filter = ("subcategory",)

    def category(self, obj):
        return obj.subcategory.category.name
    category.short_description = "Категория"


@register(ShoppingCartProduct)
class ShoppingCartProductAdmin(ModelAdmin):
    """Административный класс для модели ShoppingCartProduct."""
    list_display = ("id", "shopping_cart", "product", "amount")
    list_editable = ("amount",)
    ordering = ("shopping_cart", "product")
    search_fields = ("product__name", "shopping_cart__user__username")
    list_filter = ("shopping_cart", "product")


class ProductInline(TabularInline):
    model = ShoppingCartProduct


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    """Административный класс для модели ShoppingCart."""
    list_display = ("user",)
    ordering = ("user",)
    search_fields = ("user__username",)
    inlines = [ProductInline]
