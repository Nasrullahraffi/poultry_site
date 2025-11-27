from django.urls import path
from .views import BreederCreateView, FrontpageView

app_name = 'major'

urlpatterns = [
    path('breader/create/', BreederCreateView.as_view(), name="breeder"),
    path('', FrontpageView.as_view(), name="frontpage"),
]
