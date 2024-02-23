from .serializers import MerchantSerializer, CategorySerializer, ProductSerializer, CartSerializer, CartItemsSerializer, AddCartItemSerializer, UpdateCartItemSerializer, PromotionSerializer
from stores.models import Merchant, Category, Product, Cart, CartItems, Promotion
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class MerchantViewSet(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]
    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
class CartItemViewSet(ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.kwargs.get('cart_pk') is not None:
            return CartItems.objects.filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemsSerializer
    
    def get_serializer_context(self):
        if self.kwargs.get('cart_pk') is not None:
            return {'cart_id': self.kwargs['cart_pk']}

class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.kwargs.get('product_pk') is not None:
            return Promotion.objects.filter(product_id=self.kwargs['product_pk'])
        else:
            return Promotion.objects.all()
    
    def get_serializer_context(self):
        if self.kwargs.get('product_pk') is not None:
            product_id = self.kwargs['product_pk']
            return {'product_id': product_id}