from django.contrib import admin
from .models import Gifts, Order

@admin.register(Gifts)
class GiftsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count')
    list_filter = ('price',)
    search_fields = ('name',)
    list_editable = ('count',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gift', 'order_date', 'is_viewed', 'ip_address')
    list_filter = ('order_date', 'is_viewed')
    search_fields = ('gift__name', 'ip_address')
    readonly_fields = ('order_date',)

