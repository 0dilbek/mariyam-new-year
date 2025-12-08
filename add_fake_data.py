import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard.models import Gifts, Order

# Gift names in Uzbek and Karakalpak
gift_names_uz = [
    "Elektron kitob", "Wireless quloqchin", "Smart soat", "Portativ zaryadlovchi",
    "Bluetooth karnay", "Sovg'a karta 100,000 so'm", "Telefon ushlagich",
    "Smartfon himoyachi", "USB Flash 32GB", "Simsiz sichqoncha",
    "Klaviatura RGB", "Veb kamera HD", "Mikrofon", "Naushniklar",
    "Telefon kabeli", "Avtomobil ushlagich", "Sumka", "Ruchka to'plami",
    "Daftar to'plami", "Stiker to'plami", "Magnit taxtasi", "Kalendar 2026",
    "Qog'oz kesuvchi", "Kanselyariya to'plami", "Sertifikat 50,000 so'm"
]

gift_names_kaa = [
    "Elektron kitap", "Wireless qulaqshin", "Smart sagat", "Portativ zaryadlawshi",
    "Bluetooth karnay", "Sowg'a karta 100,000 so'm", "Telefon ushlagish",
    "Smartfon himoyalawshi", "USB Flash 32GB", "Simsiz shishqonsha",
    "Klaviatura RGB", "Veb kamera HD", "Mikrofon", "Naushnikler",
    "Telefon kabeli", "Avtomobil' ushlagish", "Súmka", "Ruchka to'plami",
    "Dapter to'plami", "Stiker to'plami", "Magnit taxtasi", "Kalendar' 2026",
    "Qog'az keswshi", "Kanselyariya to'plami", "Sertifikat 50,000 so'm"
]

# Customer names
customer_names = [
    "Aziza Karimova", "Bekzod Tursunov", "Dilnoza Rahimova", "Eldor Sharipov",
    "Feruza Nurmatova", "Gulnora Abdullayeva", "Husniddin Alimov", "Iroda Yusupova",
    "Jasur Mahmudov", "Kamola Ergasheva", "Lochin Qodirov", "Madina Saidova",
    "Nuriddin Jumaev", "Ozoda Hasanova", "Pulat Rasulov", "Qodira Nazarova",
    "Rustam Ismoilov", "Sevara Akbarova", "Timur Xolmatov", "Umida Valiyeva",
    "Vohid Bahromov", "Yulduz Mirzayeva", "Zafar Sultanov", "Asal Toshmatova",
    "Bobur Kamolov", "Charos Ortiqova", "Davron Axmedov", "Elmira Raxmonova"
]

print("🎁 Fake ma'lumotlar qo'shilmoqda...")

# Add more gifts (already have 7, adding 20 more to reach 27 total)
existing_gifts = Gifts.objects.count()
print(f"\n📦 Mavjud sovg'alar: {existing_gifts} ta")

if existing_gifts < 25:
    gifts_to_add = 25 - existing_gifts
    print(f"➕ {gifts_to_add} ta yangi sovg'a qo'shilmoqda...")
    
    for i in range(gifts_to_add):
        idx = i % len(gift_names_uz)
        order_num = existing_gifts + i + 1
        
        Gifts.objects.create(
            order_number=order_num,
            name=gift_names_uz[idx],
            available=random.choice([True, True, True, False])  # 75% active
        )
    
    print(f"✅ {gifts_to_add} ta sovg'a qo'shildi!")
else:
    print("✅ Yetarli sovg'alar mavjud")

# Add more orders (need at least 15 to show pagination)
existing_orders = Order.objects.count()
print(f"\n📋 Mavjud buyurtmalar: {existing_orders} ta")

if existing_orders < 15:
    orders_to_add = 15 - existing_orders
    print(f"➕ {orders_to_add} ta yangi buyurtma qo'shilmoqda...")
    
    all_gifts = list(Gifts.objects.all())
    
    for i in range(orders_to_add):
        customer_name = random.choice(customer_names)
        gift = random.choice(all_gifts)
        
        # Create order with random recent date
        days_ago = random.randint(0, 30)
        created_time = datetime.now() - timedelta(days=days_ago)
        
        # Generate random phone number
        phone = f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}"
        
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=phone,
            gift=gift
        )
        # Manually set the created date
        order.order_date = created_time
        order.save()
    
    print(f"✅ {orders_to_add} ta buyurtma qo'shildi!")
else:
    print("✅ Yetarli buyurtmalar mavjud")

# Final statistics
total_gifts = Gifts.objects.count()
active_gifts = Gifts.objects.filter(available=True).count()
inactive_gifts = Gifts.objects.filter(available=False).count()
total_orders = Order.objects.count()

print("\n" + "="*50)
print("📊 JAMI STATISTIKA:")
print("="*50)
print(f"🎁 Jami sovg'alar: {total_gifts} ta")
print(f"   ✅ Faol: {active_gifts} ta")
print(f"   ❌ Nofaol: {inactive_gifts} ta")
print(f"📋 Jami buyurtmalar: {total_orders} ta")
print("="*50)
print("\n✨ Pagination endi ko'rinadi!")
print("🌐 Brauzerda sahifani yangilang: http://127.0.0.1:8000/admin-panel/")
