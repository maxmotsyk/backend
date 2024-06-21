from django.contrib import admin
from .models import DeliveryMethod, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')
    list_display_links = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'status', 'first_name', 'last_name', 'phone_num', 'email', 'total_amount')
    search_fields = ('first_name', 'last_name', 'phone_num', 'email', 'city')
    list_display_links = ('id', 'product')
    inlines = [OrderItemInline]
