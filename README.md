# Poultry Management System

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

