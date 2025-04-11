from django.urls import path
from .views import index, play_slot

urlpatterns = [
    path('', index, name='index'),
    path('api/play/', play_slot, name='play_slot'),
]
