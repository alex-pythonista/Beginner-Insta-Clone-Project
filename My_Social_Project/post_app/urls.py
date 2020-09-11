from . import views
from django.urls import path
app_name = 'post_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/',views.unliked, name='unliked'),
]