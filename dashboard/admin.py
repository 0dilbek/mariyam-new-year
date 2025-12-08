from django.contrib import admin
from .models import Gifts, Order, QRCode

@admin.register(Gifts)
class GiftsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count')
    list_filter = ('price',)
    search_fields = ('name',)
    list_editable = ('count',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gift', 'order_date', 'is_viewed')
    list_filter = ('order_date', 'is_viewed')
    search_fields = ('gift__name',)
    readonly_fields = ('order_date',)

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_image', 'available', 'created_at')
    list_filter = ('available', 'created_at')
    list_editable = ('available',)

