from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

# ---------------------------------------------------------------------------
# Enumerations / Choices
# ---------------------------------------------------------------------------
class BreederType(models.TextChoices):
    BROILER = "BROILER", "Broiler"
    LAYER = "LAYER", "Layer"
    GOLDEN = "GOLDEN", "Golden"

class Sex(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    UNKNOWN = "UNKNOWN", "Unknown"

class ChickStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    SOLD = "SOLD", "Sold"
    DECEASED = "DECEASED", "Deceased"
    CULLED = "CULLED", "Culled"

class DiseaseCaseStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RESOLVED = "RESOLVED", "Resolved"

class InventoryCategory(models.TextChoices):
    FEED = "FEED", "Feed"
    MEDICINE = "MEDICINE", "Medicine"
    EQUIPMENT = "EQUIPMENT", "Equipment"
    OTHER = "OTHER", "Other"

class MovementType(models.TextChoices):
    IN = "IN", "Stock In"
    OUT = "OUT", "Stock Out"
    ADJUST = "ADJUST", "Adjustment"

class PurchaseStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ORDERED = "ORDERED", "Ordered"
    RECEIVED = "RECEIVED", "Received"
    CANCELLED = "CANCELLED", "Cancelled"

# ---------------------------------------------------------------------------
# Abstract Base Models
# ---------------------------------------------------------------------------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# ---------------------------------------------------------------------------
# RFID Tag - can be assigned to a batch (future: to individual chicks)
# ---------------------------------------------------------------------------
class RFIDTag(TimeStampedModel):
    tag_uid = models.CharField(max_length=64, unique=True, help_text="Unique RFID tag identifier")
    is_active = models.BooleanField(default=True)
    assigned_batch = models.ForeignKey('ChickBatch', on_delete=models.SET_NULL, null=True, blank=True, related_name='rfid_tags')
    assigned_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def assign_to_batch(self, batch: 'ChickBatch'):
        self.assigned_batch = batch
        self.assigned_at = timezone.now()
        self.save(update_fields=['assigned_batch', 'assigned_at'])

    def __str__(self):
        return self.tag_uid

    class Meta:
        indexes = [
            models.Index(fields=['tag_uid']),
            models.Index(fields=['is_active']),
        ]

# ---------------------------------------------------------------------------
# Chick Batch (manages group of chicks rather than per chick granularity)
# ---------------------------------------------------------------------------
class ChickBatch(TimeStampedModel):
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices)
    hatch_date = models.DateField()
    initial_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    farm_location = models.CharField(max_length=120, blank=True)
    source = models.CharField(max_length=120, blank=True, help_text="Supplier or hatchery")
    notes = models.TextField(blank=True, max_length=1000)

    @property
    def age_days(self):
        return (timezone.now().date() - self.hatch_date).days

    @property
    def current_health(self):
        latest = self.health_checks.order_by('-check_date').first()
        return latest if latest else None

    def __str__(self):
        return f"Batch #{self.id} {self.breeder_type} ({self.initial_count})"

    class Meta:
        ordering = ['-hatch_date']
        indexes = [
            models.Index(fields=['breeder_type']),
            models.Index(fields=['hatch_date']),
        ]

# ---------------------------------------------------------------------------
# Health Check Log per Batch
# ---------------------------------------------------------------------------
class HealthCheck(TimeStampedModel):
    batch = models.ForeignKey(ChickBatch, on_delete=models.CASCADE, related_name='health_checks')
    check_date = models.DateField(default=timezone.now)
    diseased_count = models.PositiveIntegerField(default=0)
    mortality_count = models.PositiveIntegerField(default=0)
    average_weight_g = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return f"HealthCheck {self.batch_id} {self.check_date}"

    class Meta:
        unique_together = ('batch', 'check_date')
        ordering = ['-check_date']

# ---------------------------------------------------------------------------
# Feed Related
# ---------------------------------------------------------------------------
class FeedFormula(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices)
    description = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return self.name

class FeedSchedule(TimeStampedModel):
    batch = models.ForeignKey(ChickBatch, on_delete=models.CASCADE, related_name='feed_schedules')
    formula = models.ForeignKey(FeedFormula, on_delete=models.PROTECT, related_name='scheduled_feeds')
    date = models.DateField(default=timezone.now)
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Feed {self.batch_id} {self.date} {self.quantity_kg}kg"

    class Meta:
        ordering = ['-date']

# ---------------------------------------------------------------------------
# Medicine & Treatments
# ---------------------------------------------------------------------------
class MedicineProduct(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices, blank=True)
    description = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return self.name

class TreatmentRecord(TimeStampedModel):
    batch = models.ForeignKey(ChickBatch, on_delete=models.CASCADE, related_name='treatments')
    medicine = models.ForeignKey(MedicineProduct, on_delete=models.PROTECT, related_name='treatments')
    date_administered = models.DateField(default=timezone.now)
    dosage = models.CharField(max_length=80, blank=True)
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return f"Treatment {self.medicine_id} {self.date_administered}"

    class Meta:
        ordering = ['-date_administered']

# ---------------------------------------------------------------------------
# Disease Catalog & Cases
# ---------------------------------------------------------------------------
class DiseaseCatalog(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices, blank=True)
    severity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="1=Low 5=High")
    description = models.TextField(blank=True, max_length=1500)

    def __str__(self):
        return self.name

class DiseaseCase(TimeStampedModel):
    batch = models.ForeignKey(ChickBatch, on_delete=models.CASCADE, related_name='disease_cases')
    disease = models.ForeignKey(DiseaseCatalog, on_delete=models.PROTECT, related_name='cases')
    date_detected = models.DateField(default=timezone.now)
    affected_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=16, choices=DiseaseCaseStatus.choices, default=DiseaseCaseStatus.ACTIVE)
    notes = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return f"Case {self.disease.name} Batch {self.batch_id}"

    class Meta:
        ordering = ['-date_detected']
        indexes = [
            models.Index(fields=['status']),
        ]

# ---------------------------------------------------------------------------
# Inventory & Stock Movements
# ---------------------------------------------------------------------------
class InventoryProduct(TimeStampedModel):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=16, choices=InventoryCategory.choices, default=InventoryCategory.OTHER)
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices, blank=True)
    unit = models.CharField(max_length=40, default="unit")
    stock_on_hand = models.PositiveIntegerField(default=0)
    reorder_point = models.PositiveIntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @property
    def needs_reorder(self):
        return self.stock_on_hand <= self.reorder_point and self.reorder_point > 0

    class Meta:
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
        ]

class StockMovement(TimeStampedModel):
    product = models.ForeignKey(InventoryProduct, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=8, choices=MovementType.choices)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reason = models.CharField(max_length=200, blank=True)
    related_batch = models.ForeignKey(ChickBatch, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def apply(self):
        # Simple stock adjustment logic (no concurrency protection here)
        if self.movement_type == MovementType.IN:
            self.product.stock_on_hand += self.quantity
        elif self.movement_type == MovementType.OUT:
            self.product.stock_on_hand = max(0, self.product.stock_on_hand - self.quantity)
        elif self.movement_type == MovementType.ADJUST:
            # For adjustments, 'quantity' is applied as absolute delta (positive or negative encoded via reason)
            self.product.stock_on_hand += self.quantity
        self.product.save(update_fields=['stock_on_hand'])

    def __str__(self):
        return f"Movement {self.product.sku} {self.movement_type} {self.quantity}"

    class Meta:
        ordering = ['-created_at']

# ---------------------------------------------------------------------------
# Vendors & Purchasing (foundation for multi-vendor system)
# ---------------------------------------------------------------------------
class Vendor(TimeStampedModel):
    name = models.CharField(max_length=140, unique=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return self.name

class PurchaseOrder(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='purchase_orders')
    order_date = models.DateField(default=timezone.now)
    expected_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=PurchaseStatus.choices, default=PurchaseStatus.DRAFT)
    reference_code = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True, max_length=1000)

    def total_cost(self):
        return sum(item.quantity * item.unit_cost for item in self.items.all())

    def __str__(self):
        return f"PO #{self.id} {self.vendor.name} {self.status}"

    class Meta:
        ordering = ['-order_date']

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(InventoryProduct, on_delete=models.PROTECT, related_name='purchase_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    received_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"POItem {self.product.sku} x {self.quantity}"

    class Meta:
        unique_together = ('purchase_order', 'product')

# ---------------------------------------------------------------------------
# NOTE: Legacy models removed. Any old references (Chick_Model, Medicine_Model, etc.)
#       should be updated in forms/views to new equivalents.
# ---------------------------------------------------------------------------
