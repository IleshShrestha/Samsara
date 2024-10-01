from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_events, name='all_events'),
    path('event/<int:pk>', views.event, name='event'),

]