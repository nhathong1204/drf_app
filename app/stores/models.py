from django.db import models
from accounts.models import Merchant, User
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.   
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(default= None, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(**kwargs)
    
class Product(models.Model):
    
    TYPE_CHOICES = (
        ('Product', 'Product'),
        ('Service', 'Service')
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(default=None, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='PRODUCT')
    tags = TaggableManager(blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'images',  blank = True, null=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999, decimal_places=2,default="10.99")
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(**kwargs)
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    product_image.short_description = "Image"
    
class ProductImages(models.Model):
    image = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'
        
class Promotion(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, related_name='promotions', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "Cart "+str(self.pk)
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        verbose_name_plural = 'Cart Items'
