from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, ProductViewSet, ShoppingCartViewSet,
                    SubcategoryViewSet)

router = routers.DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("shoppingcart", ShoppingCartViewSet)
router.register("subcategories", SubcategoryViewSet)

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("v1/", include(router.urls)),
]
