from django.urls import path
from products.views import (
    BatchListView, BatchCreateView, BatchDetailView,
    HealthCheckCreateView, FeedFormulaListView, FeedFormulaCreateView,
    FeedScheduleCreateView, MedicineListView, MedicineCreateView,
    TreatmentCreateView, DiseaseCatalogListView, DiseaseCatalogCreateView,
    DiseaseCaseCreateView, InventoryListView, InventoryCreateView,
    StockMovementCreateView, VendorListView, VendorCreateView,
    PurchaseOrderListView, PurchaseOrderCreateView, RFIDTagListView, RFIDTagCreateView
)

app_name = 'products'

urlpatterns = [
    # Batches
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/new/', BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:batch_pk>/health/add/', HealthCheckCreateView.as_view(), name='health_check_add'),
    path('batches/<int:batch_pk>/feed/add/', FeedScheduleCreateView.as_view(), name='feed_schedule_add'),
    path('batches/<int:batch_pk>/treatment/add/', TreatmentCreateView.as_view(), name='treatment_add'),
    path('batches/<int:batch_pk>/disease/add/', DiseaseCaseCreateView.as_view(), name='disease_case_add'),

    # Feed formulas
    path('feed/formulas/', FeedFormulaListView.as_view(), name='feed_formula_list'),
    path('feed/formulas/new/', FeedFormulaCreateView.as_view(), name='feed_formula_create'),

    # Medicine
    path('medicine/', MedicineListView.as_view(), name='medicine_list'),
    path('medicine/new/', MedicineCreateView.as_view(), name='medicine_create'),

    # Disease catalog
    path('diseases/catalog/', DiseaseCatalogListView.as_view(), name='disease_catalog_list'),
    path('diseases/catalog/new/', DiseaseCatalogCreateView.as_view(), name='disease_catalog_create'),

    # Inventory
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/new/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/movement/new/', StockMovementCreateView.as_view(), name='stock_movement_add'),

    # Vendors & Purchase Orders
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/new/', VendorCreateView.as_view(), name='vendor_create'),
    path('purchase-orders/', PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-orders/new/', PurchaseOrderCreateView.as_view(), name='purchase_order_create'),

    # RFID
    path('rfid/', RFIDTagListView.as_view(), name='rfid_tag_list'),
    path('rfid/new/', RFIDTagCreateView.as_view(), name='rfid_tag_create'),
]
