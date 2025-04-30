from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('<str:username>/', views.account, name='user_profile'),
]