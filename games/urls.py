from django.urls import path

from . import views

app_name = 'games'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /games/5/
    path('<int:game_id>/', views.detail, name='detail'),
]