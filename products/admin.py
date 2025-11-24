from django.contrib import admin
from products.models import (
    RFIDTag, ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct, StockMovement, Vendor, PurchaseOrder, PurchaseOrderItem
)

# Simple admin registrations; customize later with list_display / search
admin.site.register(RFIDTag)
admin.site.register(ChickBatch)
admin.site.register(HealthCheck)
admin.site.register(FeedFormula)
admin.site.register(FeedSchedule)
admin.site.register(MedicineProduct)
admin.site.register(TreatmentRecord)
admin.site.register(DiseaseCatalog)
admin.site.register(DiseaseCase)
admin.site.register(InventoryProduct)
admin.site.register(StockMovement)
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
