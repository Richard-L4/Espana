from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('cities', views.cities, name='cities'),
    path('city-details', views.city_details, name='city-details'),
    path('confirm-logout/', views.confirm_logout, name='confirm-logout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
]
