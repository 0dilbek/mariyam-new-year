from django.urls import path
from . import views
from . import language_views

urlpatterns = [
    path('', views.home, name='home'),
    path('scan/<str:token>/', views.scan_qr, name='scan_qr'),
    path('gift/', views.gift_reveal, name='gift_reveal'),
    path('claim/', views.claim_gift, name='claim_gift'),
    path('change-language/', language_views.set_language, name='change_language'),
    
    # Admin Panel URLs
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add-gift/', views.add_gift, name='add_gift'),
    path('admin-panel/delete-gift/<int:gift_id>/', views.delete_gift, name='delete_gift'),
    path('admin-panel/update-gift-count/<int:gift_id>/', views.update_gift_count, name='update_gift_count'),
    path('admin-panel/generate-qr/', views.generate_qr_codes, name='generate_qr'),
    path('admin-panel/delete-qr/<int:qr_id>/', views.delete_qr_code, name='delete_qr'),
]
