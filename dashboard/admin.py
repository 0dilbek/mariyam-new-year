from django.contrib import admin
from .models import Gifts, Order, QRCode

@admin.register(Gifts)
class GiftsAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'order_number')
    list_filter = ('available',)
    search_fields = ('name',)
    list_editable = ('available',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gift', 'customer_name', 'customer_phone', 'order_date')
    list_filter = ('order_date',)
    search_fields = ('customer_name', 'customer_phone', 'gift__name')
    readonly_fields = ('order_date',)

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_image', 'available')
    list_filter = ('available',)
    list_editable = ('available',)
