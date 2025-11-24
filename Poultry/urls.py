from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('major.urls', 'major'), namespace='major')),
    path('', include(('company.urls', 'company'), namespace='company')),
    path('', include(('products.urls', 'products'), namespace='products')),
]
