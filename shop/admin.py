from django.contrib import admin
from .models import Laptop, Order, OrderItem, Favorite

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'price', 'created_at')
    search_fields = ('brand', 'model_name')
    list_filter = ('brand', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at', 'is_paid')
    list_filter = ('is_paid',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'laptop', 'quantity', 'price')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'laptop', 'created_at')