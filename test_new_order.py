import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard.models import Gifts, Order

# Get a random gift
gift = Gifts.objects.first()

# Create a new unviewed order
order = Order.objects.create(
    gift=gift,
    customer_name="Test User",
    customer_phone="+998901234567",
    is_viewed=False
)

print(f"✅ Yangi buyurtma yaratildi: #{order.id}")
print(f"   Mijoz: {order.customer_name}")
print(f"   Sovg'a: {order.gift.name}")
print(f"   Ko'rilgan: {order.is_viewed}")
print("\n🌐 Dashboardni oching: http://127.0.0.1:8000/admin-panel/")
print("   Yangi buyurtma sariq rangda ko'rinadi va 'YANGI' belgisi bor")
