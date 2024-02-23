from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('promotions', views.PromotionViewSet)
router.register('carts', views.CartViewSet)
# router.register('cart_items', views.CartItemViewSet)
router.register('carts', views.CartViewSet)
router.register('merchants', views.MerchantViewSet)

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('promotions', views.PromotionViewSet, basename='product-promotions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('', include(product_router.urls)),
]
