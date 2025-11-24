from django.db import models
import uuid
# Create your models here.

class Company_Model(models.Model):
    company_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_phone = models.IntegerField()

def __str__(self):
    return self.company_name
