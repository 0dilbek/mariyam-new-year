from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Gifts, Order, QRCode
import random
import qrcode
from io import BytesIO
import uuid

def scan_qr(request, token):
    """QR kod skanerlanganda ishlaydigan view"""
    qr_code = get_object_or_404(QRCode, token=token)
    
    # Agar QR kod allaqachon ishlatilgan bo'lsa
    if not qr_code.available:
        return render(request, 'qr_used.html', {
            'message': 'Bu QR kod allaqachon ishlatilgan!'
        })
    
    # QR kodni ishlatilgan deb belgilash
    qr_code.available = False
    qr_code.save()
    
    # Mavjud sovg'alarni order_number ga qarab filterlash
    available_gifts = Gifts.objects.filter(
        count__gt=0
    )
    

    if not available_gifts.exists():
        return render(request, 'no_gifts.html', {
            'message': 'Afsuski, hozirda sovg\'alar tugab qoldi!'
        })

    total_fund = Gifts.objects.filter(count__gt=0).aggregate(total=Sum('price'))['total'] or 0
    weights = []
    for gift in available_gifts:
        weight = (total_fund - gift.price + 1)  # +1 to avoid zero probability
        weights.append(weight)

    # Tasodifiy sovg'ani ehtimollar asosida tanlash
    selected_gift = random.choices(list(available_gifts), weights=weights, k=1)[0]

    selected_gift.count -= 1
    selected_gift.save()
    
    request.session['gift_name'] = selected_gift.name
    request.session['gift_id'] = selected_gift.id
    
    # Sovg'a sahifasiga yo'naltirish
    return redirect('gift_reveal')

def gift_reveal(request):
    """Sovg'ani ko'rsatish sahifasi (gifts.html dizayni)"""
    gift_name = request.session.get('gift_name', None)
    
    if not gift_name:
        return redirect('home')
    
    return render(request, 'gift_reveal.html', {
        'gift_name': gift_name
    })

def claim_gift(request):
    if request.method == 'POST':
        gift_id = request.session.get('gift_id')
        
        if gift_id:
            gift = get_object_or_404(Gifts, id=gift_id)
            
            # Buyurtma yaratish
            order = Order.objects.create(
                gift=gift,
            )
            
            # Sessiyani tozalash
            request.session.pop('gift_name', None)
            request.session.pop('gift_id', None)
            
            return render(request, 'success.html', {
                'order': order
            })
    
    return redirect('home')

def home(request):
    """Asosiy sahifa"""
    return render(request, 'home.html')

# ============= ADMIN PANEL VIEWS =============

def admin_login(request):
    """Admin login sahifasi"""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri!')
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    """Admin logout"""
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    """Admin dashboard - statistika va boshqaruv"""
    total_gifts = Gifts.objects.count()
    available_gifts = Gifts.objects.filter(count__gt=0).count()
    total_gifts_count = Gifts.objects.aggregate(total=Sum('count'))['total'] or 0
    total_orders = Order.objects.count()
    total_qr_codes = QRCode.objects.count()
    available_qr_codes = QRCode.objects.filter(available=True).count()
    
    # So'nggi buyurtmalar - pagination
    orders_list = Order.objects.select_related('gift').order_by('-order_date')
    orders_paginator = Paginator(orders_list, 10)  # 10 per page
    orders_page = request.GET.get('orders_page')
    try:
        recent_orders = orders_paginator.page(orders_page)
    except PageNotAnInteger:
        recent_orders = orders_paginator.page(1)
    except EmptyPage:
        recent_orders = orders_paginator.page(orders_paginator.num_pages)
    
    # Mark displayed orders as viewed
    order_ids = [order.id for order in recent_orders]
    Order.objects.filter(id__in=order_ids, is_viewed=False).update(is_viewed=True)
    
    # Barcha sovg'alar - pagination
    gifts_list = Gifts.objects.all().order_by('-price')
    gifts_paginator = Paginator(gifts_list, 15)  # 15 per page
    gifts_page = request.GET.get('gifts_page')
    try:
        all_gifts = gifts_paginator.page(gifts_page)
    except PageNotAnInteger:
        all_gifts = gifts_paginator.page(1)
    except EmptyPage:
        all_gifts = gifts_paginator.page(gifts_paginator.num_pages)
    
    # Barcha QR kodlar - pagination
    qr_list = QRCode.objects.all().order_by('-id')
    qr_paginator = Paginator(qr_list, 20)  # 20 per page
    qr_page = request.GET.get('qr_page')
    try:
        all_qr_codes = qr_paginator.page(qr_page)
    except PageNotAnInteger:
        all_qr_codes = qr_paginator.page(1)
    except EmptyPage:
        all_qr_codes = qr_paginator.page(qr_paginator.num_pages)
    
    context = {
        'total_gifts': total_gifts,
        'available_gifts': available_gifts,
        'total_gifts_count': total_gifts_count,
        'total_orders': total_orders,
        'total_qr_codes': total_qr_codes,
        'available_qr_codes': available_qr_codes,
        'recent_orders': recent_orders,
        'all_gifts': all_gifts,
        'all_qr_codes': all_qr_codes,
    }
    
    return render(request, 'dashboard.html', context)

@login_required(login_url='admin_login')
def add_gift(request):
    """Yangi sovg'a qo'shish"""
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price', 0)
        count = request.POST.get('count', 1)
        
        Gifts.objects.create(
            name=name,
            price=price,
            count=count
        )
        messages.success(request, 'Sovg\'a muvaffaqiyatli qo\'shildi!')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def delete_gift(request, gift_id):
    """Sovg'ani o'chirish"""
    gift = get_object_or_404(Gifts, id=gift_id)
    gift.delete()
    messages.success(request, 'Sovg\'a o\'chirildi!')
    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def update_gift_count(request, gift_id):
    """Sovg'a sonini yangilash"""
    if request.method == 'POST':
        gift = get_object_or_404(Gifts, id=gift_id)
        count = int(request.POST.get('count', 0))
        gift.count = count
        gift.save()
        messages.success(request, 'Sovg\'a soni yangilandi!')
    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def generate_qr_codes(request):
    """Ko'p QR kodlarni yaratish"""
    if request.method == 'POST':
        count = int(request.POST.get('count', 1))
        
        # Base URL ni olish
        base_url = request.build_absolute_uri('/scan/')
        
        created_count = 0
        for _ in range(count):
            # Noyob token yaratish
            token = str(uuid.uuid4())
            
            # QR kod yaratish
            qr_code_obj = QRCode.objects.create(token=token)
            
            # URL yaratish - token bilan
            qr_url = f"{base_url}{token}/"
            
            # QR kod generatsiya qilish
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            # Rasm yaratish
            img = qr.make_image(fill_color="black", back_color="white")
            
            # BytesIO ga saqlash
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Faylni saqlash
            filename = f'qr_code_{qr_code_obj.id}.png'
            qr_code_obj.qr_image.save(filename, ContentFile(buffer.read()), save=True)
            
            created_count += 1
        
        messages.success(request, f'{created_count} ta QR kod muvaffaqiyatli yaratildi!')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def delete_qr_code(request, qr_id):
    """QR kodni o'chirish"""
    qr_code = get_object_or_404(QRCode, id=qr_id)
    qr_code.delete()
    messages.success(request, 'QR kod o\'chirildi!')
    return redirect('admin_dashboard')


# Custom Error Handlers
def custom_404(request, exception):
    """404 - Sahifa topilmadi"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """500 - Server xatosi"""
    return render(request, '500.html', status=500)


def custom_403(request, exception):
    """403 - Ruxsat yo'q"""
    return render(request, '403.html', status=403)
