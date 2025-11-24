from django.urls import path
from . import views

app_name = 'major'

urlpatterns = [
    path('major/', views.BreederView, name="breeder"),
    path('', views.front, name="home"),
]
