from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('major.urls')),
    path('', include('company.urls')),
    path('', include('products.urls')),
]
