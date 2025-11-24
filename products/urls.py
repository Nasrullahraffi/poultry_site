from django.urls import path
from products.views import (
    BatchListView, BatchCreateView, BatchDetailView,
    HealthCheckCreateView, FeedFormulaListView, FeedFormulaCreateView,
    FeedScheduleCreateView, MedicineListView, MedicineCreateView,
    TreatmentCreateView, DiseaseCatalogListView, DiseaseCatalogCreateView,
    DiseaseCaseCreateView, InventoryListView, InventoryCreateView,
    StockMovementCreateView, VendorListView, VendorCreateView,
    PurchaseOrderListView, PurchaseOrderCreateView, RFIDTagListView, RFIDTagCreateView,
    BatchUpdateView, BatchDeleteView, FeedFormulaUpdateView, FeedFormulaDeleteView,
    MedicineUpdateView, MedicineDeleteView, DiseaseCatalogUpdateView, DiseaseCatalogDeleteView,
    InventoryUpdateView, InventoryDeleteView, VendorUpdateView, VendorDeleteView,
    RFIDTagUpdateView, RFIDTagDeleteView, PurchaseOrderDetailView, PurchaseOrderUpdateView,
    PurchaseOrderDeleteView, StockMovementListView
)

app_name = 'products'

urlpatterns = [
    # Batches
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/new/', BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/edit/', BatchUpdateView.as_view(), name='batch_update'),
    path('batches/<int:pk>/delete/', BatchDeleteView.as_view(), name='batch_delete'),
    path('batches/<int:batch_pk>/health/add/', HealthCheckCreateView.as_view(), name='health_check_add'),
    path('batches/<int:batch_pk>/feed/add/', FeedScheduleCreateView.as_view(), name='feed_schedule_add'),
    path('batches/<int:batch_pk>/treatment/add/', TreatmentCreateView.as_view(), name='treatment_add'),
    path('batches/<int:batch_pk>/disease/add/', DiseaseCaseCreateView.as_view(), name='disease_case_add'),

    # Feed formulas
    path('feed/formulas/', FeedFormulaListView.as_view(), name='feed_formula_list'),
    path('feed/formulas/new/', FeedFormulaCreateView.as_view(), name='feed_formula_create'),
    path('feed/formulas/<int:pk>/edit/', FeedFormulaUpdateView.as_view(), name='feed_formula_update'),
    path('feed/formulas/<int:pk>/delete/', FeedFormulaDeleteView.as_view(), name='feed_formula_delete'),

    # Medicine
    path('medicine/', MedicineListView.as_view(), name='medicine_list'),
    path('medicine/new/', MedicineCreateView.as_view(), name='medicine_create'),
    path('medicine/<int:pk>/edit/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('medicine/<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),

    # Disease catalog
    path('diseases/catalog/', DiseaseCatalogListView.as_view(), name='disease_catalog_list'),
    path('diseases/catalog/new/', DiseaseCatalogCreateView.as_view(), name='disease_catalog_create'),
    path('diseases/catalog/<int:pk>/edit/', DiseaseCatalogUpdateView.as_view(), name='disease_catalog_update'),
    path('diseases/catalog/<int:pk>/delete/', DiseaseCatalogDeleteView.as_view(), name='disease_catalog_delete'),

    # Inventory
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/new/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/edit/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('inventory/movement/new/', StockMovementCreateView.as_view(), name='stock_movement_add'),
    path('inventory/movement/', StockMovementListView.as_view(), name='stock_movement_list'),

    # Vendors & Purchase Orders
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/new/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendors/<int:pk>/edit/', VendorUpdateView.as_view(), name='vendor_update'),
    path('vendors/<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor_delete'),

    path('purchase-orders/', PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-orders/new/', PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    path('purchase-orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    path('purchase-orders/<int:pk>/edit/', PurchaseOrderUpdateView.as_view(), name='purchase_order_update'),
    path('purchase-orders/<int:pk>/delete/', PurchaseOrderDeleteView.as_view(), name='purchase_order_delete'),

    # RFID
    path('rfid/', RFIDTagListView.as_view(), name='rfid_tag_list'),
    path('rfid/new/', RFIDTagCreateView.as_view(), name='rfid_tag_create'),
    path('rfid/<int:pk>/edit/', RFIDTagUpdateView.as_view(), name='rfid_tag_update'),
    path('rfid/<int:pk>/delete/', RFIDTagDeleteView.as_view(), name='rfid_tag_delete'),
]
