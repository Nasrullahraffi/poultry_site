from django.urls import path
from products import views

urlpatterns = [
    # Batches
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/new/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/<int:batch_pk>/health/add/', views.health_check_add, name='health_check_add'),
    path('batches/<int:batch_pk>/feed/add/', views.feed_schedule_add, name='feed_schedule_add'),
    path('batches/<int:batch_pk>/treatment/add/', views.treatment_add, name='treatment_add'),
    path('batches/<int:batch_pk>/disease/add/', views.disease_case_add, name='disease_case_add'),

    # Feed formulas
    path('feed/formulas/', views.feed_formula_list, name='feed_formula_list'),
    path('feed/formulas/new/', views.feed_formula_create, name='feed_formula_create'),

    # Medicine
    path('medicine/', views.medicine_list, name='medicine_list'),
    path('medicine/new/', views.medicine_create, name='medicine_create'),

    # Disease catalog
    path('diseases/catalog/', views.disease_catalog_list, name='disease_catalog_list'),
    path('diseases/catalog/new/', views.disease_catalog_create, name='disease_catalog_create'),

    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/new/', views.inventory_create, name='inventory_create'),
    path('inventory/movement/new/', views.stock_movement_add, name='stock_movement_add'),

    # Vendors & Purchase Orders
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/new/', views.vendor_create, name='vendor_create'),
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/new/', views.purchase_order_create, name='purchase_order_create'),

    # RFID
    path('rfid/', views.rfid_tag_list, name='rfid_tag_list'),
    path('rfid/new/', views.rfid_tag_create, name='rfid_tag_create'),
]
