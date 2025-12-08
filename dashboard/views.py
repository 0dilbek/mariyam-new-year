from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Gifts, Order
import random

def scan_qr(request):
    """Sovg'a berish"""
    # Mavjud sovg'alarni filterlash
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
    
    context = {
        'total_gifts': total_gifts,
        'available_gifts': available_gifts,
        'total_gifts_count': total_gifts_count,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'all_gifts': all_gifts,
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
