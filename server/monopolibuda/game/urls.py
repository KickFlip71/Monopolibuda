from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:game_id>/', views.board, name='board'),
    path('client/<int:game_id>/', views.client, name='client'),
    path('new_game', views.new_game, name='new_game'),
]