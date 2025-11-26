# Tokyo Farm - Poultry Management System

A comprehensive, company-centric poultry management system built with Django. This system allows poultry farms and companies to manage their chick batches, inventory, health records, feeding schedules, and disease tracking all in one place.

## 🌟 Features

### Company Management
- **Multi-tenant Architecture**: Each company operates independently with isolated data
- **User Registration**: Complete registration flow creating both user account and company profile
- **Company Dashboard**: Real-time statistics and quick actions
- **Company Profile Management**: Update business details, address, and license information
- **Role-based Access**: OWNER, MANAGER, STAFF, and VIEWER roles

### Chick Batch Management
- **Batch Tracking**: Monitor chick batches from hatch to sale/harvest
- **Breeder Types**: Support for BROILER, LAYER, and GOLDEN breeds
- **Live Count Tracking**: Monitor current count vs initial count
- **Mortality Rate**: Automatic calculation of batch mortality
- **Status Management**: ACTIVE, SOLD, DECEASED, CULLED states
- **Age Calculation**: Automatic age tracking in days

### Health Management
- **Health Checks**: Regular health check logging per batch
- **Disease Catalog**: Maintain database of common poultry diseases
- **Disease Cases**: Track disease outbreaks with affected counts
- **Treatment Records**: Log medicine administration and treatments
- **Severity Tracking**: 1-5 severity ratings for diseases

### Feed Management
- **Feed Formulas**: Create and manage feed recipes per breeder type
- **Feed Schedules**: Track daily/periodic feeding with quantities
- **Batch-specific Feeding**: Link feed schedules to specific batches

### Inventory Management
- **Product Catalog**: Manage feed, medicine, equipment inventory
- **Stock Tracking**: Real-time stock on hand monitoring
- **Reorder Alerts**: Low stock notifications
- **SKU Management**: Per-company unique SKU system
- **Cost & Sale Price**: Track cost and selling prices

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nasrullahraffi/poultry_site.git
   cd poultry_site/Poultry
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update `SECRET_KEY` and other settings as needed

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open browser to `http://127.0.0.1:8000`
   - Register a new company account
   - Start managing your poultry operations!

## 📱 Usage Flow

### First Time Setup
1. Visit `/company/register/`
2. Fill in your personal information
3. Enter your company/farm details
4. Click "Create Account"
5. You're automatically logged in and redirected to dashboard

### Daily Operations
1. **Dashboard**: View statistics and recent batches
2. **Create Batch**: Add new chick batch with hatch date and count
3. **Health Checks**: Log regular health inspections
4. **Feed Management**: Schedule feeding and track consumption
5. **Inventory**: Monitor stock levels and reorder supplies
6. **Disease Tracking**: Record any disease cases and treatments

## 🗂️ Project Structure

```
Poultry/
├── company/                 # Company management app
│   ├── models.py           # Company & CompanyMembership models
│   ├── views.py            # Registration, login, dashboard, profile
│   ├── forms.py            # Company registration & profile forms
│   ├── urls.py             # Company app routes
│   └── templates/
│       └── company/
│           ├── registration.html
│           ├── login.html
│           ├── dashboard.html
│           └── profile.html
│
├── products/               # Products/batch management app
│   ├── models.py           # ChickBatch, Health, Feed, Medicine, Inventory
│   ├── views.py            # CRUD views with company scoping
│   ├── forms.py            # ModelForms for all entities
│   ├── urls.py             # Products app routes
│   └── templates/
│       └── products/       # Batch, inventory, health templates
│
├── major/                  # Homepage & public pages
│   └── templates/
│       └── base.html       # Base template with navbar
│
└── Poultry/                # Project settings
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🔒 Security Features

- **Data Isolation**: Users only see their company's data
- **Authentication Required**: All management pages require login
- **Automatic Scoping**: CompanyScopedMixin filters all queries by company
- **Password Validation**: Django's built-in password validators
- **CSRF Protection**: Enabled on all forms
- **Environment Variables**: Secrets stored in .env file

## 🎨 Tech Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5.3.3 + Bootstrap Icons
- **Authentication**: Django built-in auth system
- **Form Handling**: Django ModelForms with crispy styling

## 📊 Models Overview

### Company Models
- **Company**: Central organization entity
- **CompanyMembership**: User-company relationship with roles

### Products Models
- **ChickBatch**: Group of chicks with tracking
- **HealthCheck**: Health inspection records
- **FeedFormula**: Feed recipes
- **FeedSchedule**: Feeding schedule per batch
- **MedicineProduct**: Medicine catalog
- **TreatmentRecord**: Treatment administration
- **DiseaseCatalog**: Disease database
- **DiseaseCase**: Disease outbreak records
- **InventoryProduct**: Inventory items

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database
Default: SQLite (db.sqlite3)
For production, update settings.py to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'poultry_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚧 Roadmap

- [ ] Add egg production tracking for LAYER breeds
- [ ] Multi-vendor purchasing system
- [ ] Advanced reporting and analytics
- [ ] Mobile app / PWA
- [ ] REST API for integrations
- [ ] Automated feeding schedules
- [ ] Weight gain analysis
- [ ] Feed conversion ratio (FCR) tracking
- [ ] Export data to Excel/PDF
- [ ] Email notifications for low stock

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Nasrullah Raffi** - Initial work - [GitHub](https://github.com/Nasrullahraffi)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the UI components
- All contributors who help improve this project

## 📞 Support

For support, email support@tokyofarm.com or open an issue in the GitHub repository.

---

**Built with ❤️ for the poultry farming community**
 Management System

A comprehensive Django-based web application for managing poultry farms, tracking breeders, chicks, medicines, feeds, and disease management across multiple companies.

## 📋 Features

- **Company Management**: Register and manage poultry companies
- **Breeder Tracking**: Monitor different types of breeders (Boiler, Layer, Golden)
- **Chick Management**: Track chicks by breed type, age, and health status
- **Medicine Inventory**: Maintain medicine records for different breed types
- **Disease Tracking**: Monitor and manage diseases affecting different breeds
- **Feed Management**: Track feed types and their distribution
- **Distribution System**: Manage chick distribution among different companies
- **User Authentication**: Secure login and registration for companies

## 🛠️ Technology Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite (Development)
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django Authentication System

## 📁 Project Structure

```
Poultry/
├── company/            # Company registration and authentication
├── major/              # Breeder management and distribution
├── products/           # Chicks, medicines, feeds, and disease management
├── Poultry/            # Main project settings
├── db.sqlite3          # Database file (not in repo)
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not in repo)
└── .env.example        # Environment variables template
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Poultry
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and update the SECRET_KEY
   # You can generate a new secret key using:
   # python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📊 Database Models

### Company App
- **Company_Model**: Stores company information (name, location, contact details)

### Major App
- **Breeder_Model**: Manages breeder information (type, age)
- **Distributed_among_companies**: Tracks chick distribution to companies

### Products App
- **Chick_Model**: Manages chick inventory and health status
- **Medicine_Model**: Stores medicine information for different breeds
- **Disease_Model**: Tracks diseases affecting different breeds
- **Feed_Model**: Manages feed types and descriptions

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

## 🌐 Available Apps

1. **Company** (`/company/`)
   - Company registration
   - User authentication
   - Company profile management

2. **Major** (`/major/`)
   - Breeder management
   - Distribution tracking

3. **Products** (`/products/`)
   - Chick inventory
   - Medicine management
   - Disease tracking
   - Feed management

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Creating New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## 📝 Usage

1. **Register a Company**: Navigate to the registration page and create a company account
2. **Login**: Use your credentials to access the system
3. **Manage Breeders**: Add and track different types of breeders
4. **Track Inventory**: Monitor chicks, medicines, and feeds
5. **Record Diseases**: Document and track disease outbreaks
6. **Distribute Chicks**: Manage chick distribution to companies

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## ⚠️ Important Notes

- The SECRET_KEY in `.env` should be kept secret and never committed to version control
- The database file (`db.sqlite3`) is excluded from git
- For production deployment, use a production-grade database (PostgreSQL, MySQL)
- Set `DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS` for production

## 📄 License

This project is for educational/commercial purposes.

## 👥 Authors

- Your Name/Team

## 🐛 Known Issues

- Auto-increment for primary keys using `uuid.uuid4` as default may need adjustment
- Some model `__str__` methods are defined outside the class scope

## 📞 Support

For support, please open an issue in the GitHub repository.

---

**Note**: Make sure to update `.env` with your own secret key before deploying to production!

