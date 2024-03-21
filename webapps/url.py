from django.urls import path
from django.contrib.auth import views as auth_views
from ws_todolist import views

urlpatterns = [
    path('', views.home),
]