from rest_framework import serializers
from accounts.models import Merchant
from stores.models import Category, Product, ProductImages, Cart, CartItems, Promotion
from taggit.serializers import (TagListSerializerField, TaggitSerializer)

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id","user", "first_name", "last_name", "mobile", "address", "verified"]
        read_only_fields = ['id']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]
        read_only_fields = ['id', 'slug']
    
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'product', 'description', 'discount_percentage', 'start_date', 'end_date']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        if self.context is not None:
            product_id = self.context['product_id']
            return Promotion.objects.create(product_id=product_id, **validated_data)
        else:
            return Promotion.objects.create(**validated_data)
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'product', 'image', 'date']
        read_only_fields = ['id']
        
class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    images = ProductImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = Product
        fields = [ "id", "name", "tags", "type", "description", "price", 'category', 'merchant', 'image', 'images', 'upload_images']
        read_only_fields = ['id']

        
    def create(self, validated_data):
        uploaded_images = validated_data.pop('upload_images')
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            new_product_image = ProductImages.objects.create(product=product, image=image)
            
        product_tags = validated_data.pop('tags')
        if type(product_tags) is list:
            saved_product = Product.objects.get(pk=product.pk)
            for tag in product.tags:
                saved_product.tags.add(tag)
            
        return product
    
class SimplePromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['name', 'discount_percentage']
    
class SimpleProductSerializer(serializers.ModelSerializer):
    promotions = SimplePromoSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'promotions']
        
class CartItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)
    sub_total = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    
    class Meta:
        model = CartItems
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']
        read_only_fields = ['id', 'cart']
        
    def get_sub_total(self, obj):
        discountTotal = 0;
        for promo in obj.product.promotions.all():
            discountTotal += promo.discount_percentage
            
        price_after_discount = obj.product.price - ((discountTotal * obj.product.price)/100)
        return obj.quantity * price_after_discount

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = CartItemsSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField('grandtotal')
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'owner', 'completed', 'grand_total']
        read_only_fields = ['id']
        
    def grandtotal(self, cart:Cart):
        items = cart.items.all()
        total = 0
        for item in items:
            discountTotal = 0;
            for promo in item.product.promotions.all():
                discountTotal += promo.discount_percentage
                
            price_after_discount = item.product.price - ((discountTotal * item.product.price)/100)
            total += item.quantity * price_after_discount
        return total
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('There is no product associated with the given ID')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id =self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            
            self.instance = cart_item
        except:
            self.instance = CartItems.objects.create(cart_id=cart_id, **self.validated_data)
            
        
        return self.instance
    
    class Meta:
        model = CartItems
        fields = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ('quantity',)
        