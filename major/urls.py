from django.urls import path
from .views import BreederCreateView, HomeView

app_name = 'major'

urlpatterns = [
    path('major/', BreederCreateView.as_view(), name="breeder"),
    path('', HomeView.as_view(), name="home"),
]
