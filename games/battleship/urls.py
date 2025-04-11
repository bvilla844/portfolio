from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start-game/', views.start_game, name='start_game'),
    path('make-move/', views.make_move, name='make_move'),
    path('place-ships/', views.place_ships, name='place_ships'),  # Asegúrate de que esté aquí
]
