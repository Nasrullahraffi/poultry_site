from django.urls import path
from products.views import (
    BatchListView, BatchCreateView, BatchDetailView,
    HealthCheckCreateView, FeedFormulaListView, FeedFormulaCreateView,
    FeedScheduleCreateView, MedicineListView, MedicineCreateView,
    TreatmentCreateView, DiseaseCatalogListView, DiseaseCatalogCreateView,
    DiseaseCaseCreateView, InventoryListView, InventoryCreateView,
    BatchUpdateView, BatchDeleteView, FeedFormulaUpdateView, FeedFormulaDeleteView,
    MedicineUpdateView, MedicineDeleteView, DiseaseCatalogUpdateView, DiseaseCatalogDeleteView,
    InventoryUpdateView, InventoryDeleteView
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
]
