from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('login_view/', login_view, name='login_view'),

]
