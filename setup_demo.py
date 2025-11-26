#!/usr/bin/env python
"""
Setup script for Tokyo Farm Poultry Management System
Run this script to set up the database and create initial data
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Poultry.settings')
django.setup()

from django.contrib.auth.models import User
from company.models import Company, CompanyMembership
from products.models import (
    ChickBatch, FeedFormula, MedicineProduct,
    DiseaseCatalog, InventoryProduct
)
from django.utils.text import slugify
from datetime import date, timedelta

def create_demo_company():
    """Create a demo company with sample data"""
    print("\n🏢 Creating Demo Company...")

    # Create demo user
    user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@tokyofarm.com',
            'first_name': 'Demo',
            'last_name': 'User',
        }
    )
    if created:
        user.set_password('demo123')
        user.save()
        print(f"✅ Created demo user: demo / demo123")
    else:
        print(f"ℹ️  Demo user already exists")

    # Create demo company
    company, created = Company.objects.get_or_create(
        slug='tokyo-demo-farm',
        defaults={
            'name': 'Tokyo Demo Farm',
            'email': 'info@tokyodemofarm.com',
            'phone': '+1234567890',
            'city': 'Tokyo',
            'state_province': 'Tokyo',
            'address_line1': '123 Farm Street',
            'postal_code': '100-0001',
            'country': 'Japan',
            'license_number': 'TDF-2025-001',
            'owner': user,
            'is_active': True,
        }
    )
    if created:
        print(f"✅ Created demo company: {company.name}")
    else:
        print(f"ℹ️  Demo company already exists")

    # Create company membership
    membership, created = CompanyMembership.objects.get_or_create(
        user=user,
        company=company,
        defaults={
            'role': 'OWNER',
            'is_active': True,
        }
    )
    if created:
        print(f"✅ Created company membership")

    return company

def create_sample_batches(company):
    """Create sample chick batches"""
    print("\n🐔 Creating Sample Batches...")

    batches_data = [
        {
            'breeder_type': 'BROILER',
            'hatch_date': date.today() - timedelta(days=30),
            'initial_count': 500,
            'current_count': 485,
            'farm_location': 'Building A',
            'source': 'Hatchery Inc.',
            'status': 'ACTIVE',
            'notes': 'Broiler batch for meat production'
        },
        {
            'breeder_type': 'LAYER',
            'hatch_date': date.today() - timedelta(days=60),
            'initial_count': 300,
            'current_count': 295,
            'farm_location': 'Building B',
            'source': 'Premium Eggs Co.',
            'status': 'ACTIVE',
            'notes': 'Layer batch for egg production'
        },
        {
            'breeder_type': 'GOLDEN',
            'hatch_date': date.today() - timedelta(days=45),
            'initial_count': 200,
            'current_count': 198,
            'farm_location': 'Building C',
            'source': 'Golden Breeds Ltd.',
            'status': 'ACTIVE',
            'notes': 'Premium golden breed batch'
        },
    ]

    created_count = 0
    for batch_data in batches_data:
        batch_data['company'] = company
        batch, created = ChickBatch.objects.get_or_create(
            company=company,
            breeder_type=batch_data['breeder_type'],
            hatch_date=batch_data['hatch_date'],
            defaults=batch_data
        )
        if created:
            created_count += 1
            print(f"✅ Created {batch.breeder_type} batch - {batch.initial_count} chicks")

    print(f"✅ Created {created_count} batches")

def create_sample_inventory(company):
    """Create sample inventory items"""
    print("\n📦 Creating Sample Inventory...")

    inventory_data = [
        {
            'sku': 'FEED-001',
            'name': 'Starter Feed',
            'category': 'FEED',
            'breeder_type': 'BROILER',
            'unit': 'kg',
            'stock_on_hand': 500,
            'reorder_point': 100,
            'cost_price': 25.00,
            'sale_price': 35.00,
        },
        {
            'sku': 'FEED-002',
            'name': 'Layer Feed',
            'category': 'FEED',
            'breeder_type': 'LAYER',
            'unit': 'kg',
            'stock_on_hand': 300,
            'reorder_point': 100,
            'cost_price': 22.00,
            'sale_price': 30.00,
        },
        {
            'sku': 'MED-001',
            'name': 'Vitamin Supplement',
            'category': 'MEDICINE',
            'breeder_type': '',
            'unit': 'bottle',
            'stock_on_hand': 50,
            'reorder_point': 20,
            'cost_price': 15.00,
            'sale_price': 25.00,
        },
        {
            'sku': 'MED-002',
            'name': 'Antibiotic Powder',
            'category': 'MEDICINE',
            'breeder_type': '',
            'unit': 'packet',
            'stock_on_hand': 25,
            'reorder_point': 10,
            'cost_price': 30.00,
            'sale_price': 45.00,
        },
        {
            'sku': 'EQ-001',
            'name': 'Water Feeder',
            'category': 'EQUIPMENT',
            'breeder_type': '',
            'unit': 'piece',
            'stock_on_hand': 100,
            'reorder_point': 20,
            'cost_price': 5.00,
            'sale_price': 10.00,
        },
    ]

    created_count = 0
    for inv_data in inventory_data:
        inv_data['company'] = company
        inv, created = InventoryProduct.objects.get_or_create(
            company=company,
            sku=inv_data['sku'],
            defaults=inv_data
        )
        if created:
            created_count += 1
            print(f"✅ Created {inv.name} ({inv.sku})")

    print(f"✅ Created {created_count} inventory items")

def create_sample_data():
    """Create all sample data"""
    print("=" * 60)
    print("🚀 Tokyo Farm Setup - Creating Demo Data")
    print("=" * 60)

    company = create_demo_company()
    create_sample_batches(company)
    create_sample_inventory(company)

    print("\n" + "=" * 60)
    print("✅ Demo data created successfully!")
    print("=" * 60)
    print("\n📝 Demo Account Credentials:")
    print("   Username: demo")
    print("   Password: demo123")
    print("\n🌐 Login at: http://127.0.0.1:8000/company/login/")
    print("=" * 60)

if __name__ == '__main__':
    create_sample_data()

