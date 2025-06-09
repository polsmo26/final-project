from django.urls import path
from .views import register, login_view, logout_view, dashboard, edit_profile
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]