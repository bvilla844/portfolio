from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='portfolio'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('juegos/', views.game_menu, name='menu'),
]
