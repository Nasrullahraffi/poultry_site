from django.urls import path
from products import views
urlpatterns = [
    path('feed/', views.FeedView, name="feed"),
    path('medicine/', views.MedicineView, name="medicines"),
    path('disease/', views.DiseaseView, name="diseases"),
]
