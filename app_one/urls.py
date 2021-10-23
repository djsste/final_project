from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('user_page', views.success),
    path('logout', views.logout),
    path('create_task', views.create_task),
]