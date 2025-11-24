from django.urls import path
from . import views
urlpatterns = [
    path('major/', views.BreederView, name="breeder"),
    path('', views.front, name="home"),
]
