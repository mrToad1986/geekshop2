from django.contrib import admin
from authapp.models import ShopUser
from django.contrib.auth.admin import UserAdmin
from mainapp.models import Product, ProductCategory

# admin.site.register(Product)
admin.site.register(ProductCategory)
# admin.site.register(ShopUser)


@admin.register(ShopUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'short_desc', 'description', 'price', 'quantity', 'category')
    # readonly_fields = ('description',)
    ordering = ('name',)
    search_fields = ('name',)
