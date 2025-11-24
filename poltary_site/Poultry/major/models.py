from django.db import models
import uuid
from company.models import Company_Model
from products.models import *
# Create your models here.




# EMPLOYEE_CHOICES = [
#     ("CEO"),
#     ("Manager"),
#     ("Zonal Manager"),
#     ("Dealer"),
#     ("Farmer"),
# ]

# class Employee_Model(models.Model):
#     employ_id = models.IntegerField(primary_key=True, default=uuid.uuid4, unique=True,  editable=False, blank=True, null=True)
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     role = models.CharField(choices=EMPLOYEE_CHOICES)
#     contact_id = models.IntegerField(max_length=100)
#     Email = models.EmailField()

# def __str__(self):
#     return self.first_name

BREEDER_CHOICES = [
    ( "Boiler Breeder" ,'Boiler Breeder'),
    ("Layer Breeder" ,'Layer Breeder' ),
    ("Golden Breeder",'Golden Breeder'),
]

class Breeder_Model(models.Model):
    breeder_id = models.IntegerField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    breeder_type = models.CharField(choices=BREEDER_CHOICES,max_length=100)
    breeder_age = models.IntegerField()
    

def __str__(self):
    return self.breeder_type
    



class Distributed_among_companies(models.Model):
    medicine_id = models.IntegerField(primary_key=True,default=uuid.uuid4, unique=True)
    company_name = models.ForeignKey(Company_Model, on_delete=models.CASCADE, )
    type_of_chick = models.CharField(choices=BREEDER_CHOICES,max_length=100 )
    total_number_of_chicks = models.IntegerField()
    infacted_chicks = models.IntegerField()
    diseased_chicks = models.IntegerField()
    date_of_departure = models.DateField(auto_now=False, auto_now_add=False, editable=False)

def __str__(self):
    return self.company_name