from django.contrib import admin
from .models import Cart, CartItems, Category, Product, ProductImages, Promotion

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name','merchant','slug','image','category','price','status']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name','product', 'type','description', 'discount_percentage','start_date','end_date']
    
    def type(self, obj):
        if obj.product is not None:
            return obj.product.get_type_display()
        return None
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title','slug']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['owner','created','completed']
    
@admin.register(CartItems)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']
    
# admin.site.register(Product,ProductAdmin)
# admin.site.register(Promotion,PromotionAdmin)
# admin.site.register(Category,CategoryAdmin)