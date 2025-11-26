from django.contrib import admin
from products.models import (
    ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct
)

# Simple admin registrations; customize later with list_display / search

admin.site.register(ChickBatch)
admin.site.register(HealthCheck)
admin.site.register(FeedFormula)
admin.site.register(FeedSchedule)
admin.site.register(MedicineProduct)
admin.site.register(TreatmentRecord)
admin.site.register(DiseaseCatalog)
admin.site.register(DiseaseCase)
admin.site.register(InventoryProduct)

