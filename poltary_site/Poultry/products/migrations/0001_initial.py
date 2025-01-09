# Generated by Django 5.1.4 on 2025-01-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chick_Model',
            fields=[
                ('Chick_id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('breeder_type', models.CharField(choices=[('BB', 'Boiler Breeder'), ('LB', 'Layer Breeder'), ('GB', 'Golden Breeder')], max_length=100)),
                ('number_of_diseased_chicks', models.IntegerField(db_column='Number Of Diseased Chicks')),
                ('chicks_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Disease_Model',
            fields=[
                ('disease_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('disease_name', models.CharField(max_length=100)),
                ('disease_in_type_of_breed', models.CharField(choices=[('BB', 'Boiler Breeder'), ('LB', 'Layer Breeder'), ('GB', 'Golden Breeder')], max_length=100)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Feed_Model',
            fields=[
                ('feed_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('feed_name', models.CharField(max_length=100)),
                ('feed_type', models.CharField(choices=[('BB', 'Boiler Breeder'), ('LB', 'Layer Breeder'), ('GB', 'Golden Breeder')], max_length=100)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine_Model',
            fields=[
                ('medicine_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('medicine_name', models.CharField(max_length=100)),
                ('medicine_for_type_breed', models.CharField(choices=[('BB', 'Boiler Breeder'), ('LB', 'Layer Breeder'), ('GB', 'Golden Breeder')], max_length=100)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
    ]
