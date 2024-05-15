from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import (MAX_AMOUNT_PRODUCT, Category, Product,
                             ShoppingCart, ShoppingCartProduct, Subcategory)
from .paginations import CustomPagination
from .permissions import IsOwnerOrAdmin
from .serializers import (CategorySerializer, ListShoppingCartSerializer,
                          ProductSerializer, ShoppingCartProductSerializer,
                          SubcategorySerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для подкатегорий."""
    queryset = Subcategory.objects.select_related("category")
    serializer_class = SubcategorySerializer
    pagination_class = CustomPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для продуктов."""
    queryset = Product.objects.select_related("subcategory").prefetch_related(
        "subcategory__category"
    )
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class ShoppingCartViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для продуктовой корзины."""
    queryset = ShoppingCartProduct.objects.all()
    permission_classes = (IsOwnerOrAdmin,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Получить сериализатор."""
        if self.action == "show_total_info":
            return ListShoppingCartSerializer
        return ShoppingCartProductSerializer

    def get_queryset(self):
        """Отфильтровать queryset по текущему пользователю."""
        user = self.request.user
        return ShoppingCartProduct.objects.select_related(
            "shopping_cart__user"
        ).prefetch_related("product").filter(
            shopping_cart__user=user
        )

    @action(methods=["GET"], detail=False)
    def show_total_info(self, request):
        """Вывести общую стоимость и количество продуктов в корзине."""
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if not shopping_cart:
            return Response(
                "Продуктовая корзина пуста.",
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer_class()
        serializer = serializer(
            instance=shopping_cart,
            context={"request": request}
        )
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def add_product(self, request):
        """Добавить продукт в корзину или увеличить его количество."""
        serializer = ShoppingCartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = request.data.get("product")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return (
                Response(
                    "Такого продукта нет.",
                    status=status.HTTP_400_BAD_REQUEST
                )
            )

        user = request.user
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

        shopping_cart_product, created = (
            ShoppingCartProduct.objects.get_or_create(
                shopping_cart=shopping_cart,
                product=product,
            )
        )

        amount = request.data.get("amount")
        if shopping_cart_product.amount + amount > MAX_AMOUNT_PRODUCT:
            return Response(
                "Ошибка! "
                f"Максимальное количество продукта - {MAX_AMOUNT_PRODUCT} шт. "
                f"В корзине - {shopping_cart_product.amount}.",
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_cart_product.amount += amount
        shopping_cart_product.save()
        return Response(
            f"Продукт {product.name} добавлен в корзину "
            f"в количестве {amount} шт.",
            status=status.HTTP_200_OK
        )

    @action(methods=["POST"], detail=False)
    def remove_product(self, request):
        """Удалить продукт из корзины или уменьшить его количество."""
        serializer = ShoppingCartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if not shopping_cart:
            return Response(
                "Продуктовая корзина пуста.",
                status=status.HTTP_400_BAD_REQUEST
            )

        product_id = request.data.get("product")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                "Такого продукта нет.",
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_cart_product = ShoppingCartProduct.objects.filter(
            shopping_cart=shopping_cart,
            product=product
        ).first()
        if not shopping_cart_product:
            return Response(
                "Такого продукта в продуктовой корзине нет.",
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = request.data.get("amount")
        if shopping_cart_product.amount - amount < 0:
            return Response(
                f"В продуктовой корзине количество товара меньше, "
                "чем Вы хотите убрать! "
                f"В ней {shopping_cart_product.amount} шт. данного продукта.",
                status=status.HTTP_400_BAD_REQUEST)
        if shopping_cart_product.amount - amount == 0:
            shopping_cart_product.delete()
            return Response(
                f"Продукт {product.name} удален из корзины.",
                status=status.HTTP_204_NO_CONTENT
            )

        shopping_cart_product.amount -= amount
        shopping_cart_product.save()

        return Response(
            f"Продукт {product.name} удален из корзины. "
            f"Осталось {shopping_cart_product.amount} шт.",
            status=status.HTTP_200_OK
        )

    @action(methods=["POST"], detail=False)
    def clear_shopping_cart(self, request):
        """Очистить продуктовую корзину."""
        shopping_cart_product = self.get_queryset()

        if not shopping_cart_product:
            return Response(
                "Продуктовая корзина пуста.",
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_cart_product.delete()
        return Response(
            "Продуктовая корзина очищена.",
            status=status.HTTP_204_NO_CONTENT
        )
