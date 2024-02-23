from django.contrib import admin

# Register your models here.
from .models import User, Merchant
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['email','first_name','last_name']
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )


class MerchantAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name','last_name', 'mobile', 'address', 'verified']

admin.site.register(User,CustomUserAdmin)
admin.site.register(Merchant,MerchantAdmin)