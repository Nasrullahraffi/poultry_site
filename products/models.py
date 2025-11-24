from django.db import models
import uuid
from major.models import *



# Create your models here.


BREEDER_CHOICES = [
    ( "Boiler Breeder" ,'Boiler Breeder'),
    ("Layer Breeder" ,'Layer Breeder' ),
    ("Golden Breeder",'Golden Breeder'),
]


        # Chicks Model




class Chick_Model(models.Model):
    Chick_id = models.IntegerField(primary_key=True, editable=False, unique=True)
    breeder_type = models.CharField(choices=BREEDER_CHOICES, max_length=100)
    # total_chicks = models.DecimalField(decimal_places=2, max_digits=10)
    number_of_diseased_chicks = models.IntegerField(db_column='Number Of Diseased Chicks')
    chicks_age = models.IntegerField()
    date = models.DateTimeField(auto_now=
    True)

def __str__(self):
    return self.breeder




        #  Medicines Model 

class Medicine_Model(models.Model):
    medicine_id = models.IntegerField(primary_key=True , unique=True)
    medicine_name = models.CharField(max_length=100)
    medicine_for_type_breed = models.CharField(choices=BREEDER_CHOICES,max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=
    True)
def __str__(self):
    return self.medicine_name

        #  Disease Model

class Disease_Model(models.Model):
    disease_id = models.IntegerField(primary_key=True,unique=True)
    disease_name = models.CharField(max_length=100)
    disease_in_type_of_breed = models.CharField(choices=BREEDER_CHOICES,max_length=100)
    description = models.TextField(max_length=500)
def __str__(self):
    return self.disease_name

        # Feed Model 

class Feed_Model(models.Model):
    feed_id = models.IntegerField(primary_key=True, unique=True)
    feed_name = models.CharField(max_length=100)
    feed_type = models.CharField(choices=BREEDER_CHOICES,max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=
    True)
def __str__(self):
    return self.feed_name


