# proapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.index, name='index'),
    path('properties/', views.properties, name='properties'),
    path('property-details/', views.property_details, name='property_details'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin: users
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/users/<int:id>/edit/', views.edit_user, name='edit_user'),
    path('admin/users/<int:id>/delete/', views.delete_user, name='delete_user'),

    # Admin: flats
    path('admin/flats/', views.manage_flats, name='manage_flats'),
    path('admin/flats/add/', views.add_flat, name='add_flat'),
    path('admin/flats/list/', views.list_flats, name='list_flats'),
    path('admin/flats/sold/', views.sold_flats, name='sold_flats'),
    path('admin/flats/rented/', views.rented_flats, name='rented_flats'),
    path('admin/flats/<int:id>/edit/', views.edit_flat, name='edit_flat'),
    path('admin/flats/<int:id>/delete/', views.delete_flat, name='delete_flat'),
    path('admin/flats/<str:flat_id>/', views.view_flat, name='view_flat'),

    # User: profile
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # User: flats browse & details
    path('flats/available/', views.user_flat_view, name='user_flat_view'),
    path('flats/<str:flat_id>/', views.flat_details, name='flat_details'),

    # User: rent / buy landing pages
    path('flats/rent/<str:flat_id>/', views.rent_flat, name='rent_flat'),
    path('flats/buy/<str:flat_id>/', views.buy_flat, name='buy_flat'),

    # Optional “review/confirm” pages before final payment (you created these)
    path('payment/rent/<str:flat_id>/', views.rpayment, name='rpayment'),
    path('payment/buy/<str:flat_id>/', views.bpayment, name='bpayment'),

    # Final processors that create Payment and show proof
    path('payment/process/rent/<str:flat_id>/', views.process_rent_payment, name='process_rent_payment'),
    path('payment/process/buy/<str:flat_id>/', views.process_buy_payment, name='process_buy_payment'),

    # Payment proof (you render this right after creating Payment)
    path('payment/proof/', views.payment_proof, name='payment_proof'),

    # Programs
    path('programs/', views.programs, name='programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/approve/', views.approve_program, name='approve_program'),
    path('programs/approved/', views.approved_programs, name='approved_programs'),
    path('programs/fees/', views.program_fees, name='program_fees'),
    path('programs/amount/', views.program_amount, name='program_amount'),
]
