from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('game/<str:name>', views.join_game, name='join_game'),
    path('game/LEAVE-GAME', views.leave_game, name='leave-game')
]
