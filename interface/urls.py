from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_join),
    path('lobby/', views.render_lobby_view),
    path('register/', views.register),
    path('charAtribute/', views.associate_char),
    path('wait_room/', views.render_wait_room, name='wait_room'),
    path('shared_screen/', views.render_shared),
    path('select_char/', views.render_select_char),
    path('char_specs/<str:char_rule>/<path:char_url>/', views.render_char_specs, name='char_specs'),
    path('finish_game/', views.finish_game),
    # path('leave_game/', views.leave_game),
    path('game/<str:room_name>/<str:key>', views.render_game_room, name='game_room'),
    path('render_visited/', views.render_room),
    path('check_answer/', views.check_answer),
    path('end_game/<str:message>/', views.render_end),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
