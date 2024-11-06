from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_join),
    path('lobby/', views.render_lobby_view),
    path('register/', views.register),
    path('wait_room/', views.render_wait_room),
    path('shared_screen/', views.render_shared),
    path('choose_char/', views.render_choose_char),
    path('finish_game/', views.finish_game),
    path('leave_game/', views.leave_game),
]
