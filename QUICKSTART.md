# 🚀 Quick Start Guide - Tokyo Farm

## Ready to Use! ✅

Your poultry management system is **fully set up and ready to use** with demo data!

## 🎯 Start the Server

```bash
cd C:\desktop\poltary_site\Poultry
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## 🔑 Login Credentials

### Demo Account (With Sample Data)
- **Username:** `demo`
- **Password:** `demo123`
- **Company:** Tokyo Demo Farm
- **Includes:** 3 batches, 5 inventory items

### Admin Account (For Admin Panel)
- **Username:** `admin`
- **Password:** `admin123`
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 📱 What You Can Do Now

### 1. **Login & Explore Dashboard**
   - Go to http://127.0.0.1:8000/company/login/
   - Login with `demo / demo123`
   - View your company dashboard with statistics

### 2. **Manage Batches**
   - View 3 pre-created batches (Broiler, Layer, Golden)
   - Create new batches
   - Track mortality rate
   - Add health checks

### 3. **Manage Inventory**
   - View 5 sample inventory items
   - Track stock levels
   - Get low stock alerts
   - Add new products

### 4. **Health Tracking**
   - Log health checks for batches
   - Record treatments
   - Track disease cases

### 5. **Feed Management**
   - Create feed formulas
   - Schedule feeding
   - Track consumption

## 🏢 Create Your Own Company

Want to start fresh? Register a new company:

1. Go to http://127.0.0.1:8000/company/register/
2. Fill in your details
3. Start managing your own farm!

## 📊 Sample Data Overview

### Batches (3 total)
1. **Broiler Batch** - Building A
   - 500 chicks (485 alive)
   - 30 days old
   - Status: Active

2. **Layer Batch** - Building B
   - 300 chicks (295 alive)
   - 60 days old
   - Status: Active

3. **Golden Batch** - Building C
   - 200 chicks (198 alive)
   - 45 days old
   - Status: Active

### Inventory (5 items)
1. **Starter Feed** (FEED-001) - 500 kg
2. **Layer Feed** (FEED-002) - 300 kg
3. **Vitamin Supplement** (MED-001) - 50 bottles
4. **Antibiotic Powder** (MED-002) - 25 packets
5. **Water Feeder** (EQ-001) - 100 pieces

## 🛠️ Quick Commands

### Run Server
```bash
python manage.py runserver
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Reset Database (Start Fresh)
```bash
Remove-Item db.sqlite3
python manage.py migrate
python setup_demo.py
```

### Run Tests
```bash
python manage.py test
```

## 📝 Common Tasks

### Add a New Batch
1. Login to dashboard
2. Click "New Batch" button
3. Fill in:
   - Breeder type (Broiler/Layer/Golden)
   - Hatch date
   - Initial count
   - Location and source
4. Save

### Log Health Check
1. Go to batch detail page
2. Click "Add Health Check"
3. Enter:
   - Check date
   - Disease count
   - Mortality count
   - Average weight
4. Save

### Add Inventory Item
1. Go to Inventory page
2. Click "Add Inventory"
3. Fill in:
   - SKU (unique per company)
   - Name and category
   - Stock and reorder point
   - Prices
4. Save

## 🌐 Main URLs

- **Homepage:** http://127.0.0.1:8000/
- **Register:** http://127.0.0.1:8000/company/register/
- **Login:** http://127.0.0.1:8000/company/login/
- **Dashboard:** http://127.0.0.1:8000/company/dashboard/
- **Batches:** http://127.0.0.1:8000/batches/
- **Inventory:** http://127.0.0.1:8000/inventory/
- **Admin:** http://127.0.0.1:8000/admin/

## ⚙️ System Features

✅ **Multi-tenant company system**
✅ **Complete batch management**
✅ **Health tracking & disease monitoring**
✅ **Inventory management with alerts**
✅ **Feed scheduling**
✅ **Treatment records**
✅ **Modern responsive UI**
✅ **Role-based access control**

## 🎨 Tech Stack

- **Backend:** Django 5.1.4
- **Frontend:** Bootstrap 5.3.3
- **Database:** SQLite (development)
- **Icons:** Bootstrap Icons

## 📞 Need Help?

- Check the README.md for detailed documentation
- Visit Django docs: https://docs.djangoproject.com/
- Bootstrap docs: https://getbootstrap.com/docs/

---

**🐔 Happy Farming! 🌾**

Your poultry management system is ready to help you track and manage your farm operations efficiently!

