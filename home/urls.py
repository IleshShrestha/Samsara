from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('community/', views.community, name='community'),
    path('stores/', views.stores, name='stores'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy_policy'),
    path('shipping/', views.shipping, name='shipping_policy')


]