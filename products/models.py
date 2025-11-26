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

# ---------------------------------------------------------------------------
# Abstract Base Models
# ---------------------------------------------------------------------------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CompanyScopedModel(TimeStampedModel):
    """
    Abstract base for models that belong to a company
    """
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='%(class)s_set', null=True, blank=True)

    class Meta:
        abstract = True

# ---------------------------------------------------------------------------
# Chick Batch (manages group of chicks)
# ---------------------------------------------------------------------------
class ChickBatch(CompanyScopedModel):
    breeder_type = models.CharField(max_length=16, choices=BreederType.choices)
    hatch_date = models.DateField()
    initial_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    current_count = models.PositiveIntegerField(null=True, blank=True, help_text="Current live count")
    farm_location = models.CharField(max_length=120, blank=True)
    source = models.CharField(max_length=120, blank=True, help_text="Supplier or hatchery")
    status = models.CharField(max_length=16, choices=ChickStatus.choices, default=ChickStatus.ACTIVE)
    notes = models.TextField(blank=True, max_length=1000)

    @property
    def age_days(self):
        return (timezone.now().date() - self.hatch_date).days

    @property
    def current_health(self):
        latest = self.health_checks.order_by('-check_date').first()
        return latest if latest else None

    @property
    def mortality_rate(self):
        if self.current_count is not None and self.initial_count > 0:
            return ((self.initial_count - self.current_count) / self.initial_count) * 100
        return 0

    def __str__(self):
        return f"Batch #{self.id} {self.breeder_type} ({self.initial_count})"

    class Meta:
        ordering = ['-hatch_date']
        indexes = [
            models.Index(fields=['company', 'breeder_type']),
            models.Index(fields=['company', 'hatch_date']),
            models.Index(fields=['company', 'status']),
        ]
        verbose_name_plural = "Chick Batches"

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
# Inventory
# ---------------------------------------------------------------------------
class InventoryProduct(CompanyScopedModel):
    sku = models.CharField(max_length=40)
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
        unique_together = ('company', 'sku')
        indexes = [
            models.Index(fields=['company', 'sku']),
            models.Index(fields=['company', 'category']),
            models.Index(fields=['company', 'is_active']),
        ]

# ---------------------------------------------------------------------------
# NOTE: Removed non-essential models (RFIDTag, StockMovement, Vendor, PurchaseOrder, PurchaseOrderItem)
# ---------------------------------------------------------------------------
