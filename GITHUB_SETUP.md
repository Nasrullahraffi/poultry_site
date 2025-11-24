# GitHub Setup Guide

This guide will help you connect this local repository to your existing GitHub repository.

## Steps to Connect to GitHub

### 1. Configure Git User (if not already done)
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 2. Add Your GitHub Repository as Remote
Replace `<your-username>` and `<your-repo-name>` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
```

Or if you're using SSH:
```bash
git remote add origin git@github.com:<your-username>/<your-repo-name>.git
```

### 3. Verify the Remote
```bash
git remote -v
```

### 4. Push to GitHub

If your GitHub repository is empty:
```bash
git branch -M main
git push -u origin main
```

If your GitHub repository already has content:
```bash
# First, pull any existing changes
git pull origin main --allow-unrelated-histories

# Resolve any conflicts if they occur, then:
git push -u origin main
```

## Setting Up the Project for New Contributors

### For Team Members Cloning the Repository

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
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
   
   # Edit .env and add your SECRET_KEY
   # Generate a new key using:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Important Files to Keep Secret

The following files are already in `.gitignore` and will NOT be pushed to GitHub:

- `.env` - Contains your secret key and sensitive configuration
- `db.sqlite3` - Your local database
- `__pycache__/` - Python cache files
- `*.pyc` - Compiled Python files
- `venv/` - Virtual environment folder

## Updating Requirements

If you install new packages:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

## Branch Strategy (Optional)

Consider using branches for new features:
```bash
# Create a new branch for a feature
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push the branch
git push -u origin feature/feature-name

# Create a Pull Request on GitHub
```

## Troubleshooting

### If you encounter merge conflicts:
```bash
# View conflicted files
git status

# Edit the files to resolve conflicts
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push
```

### If you need to update from the remote repository:
```bash
git pull origin main
```

### If you want to see commit history:
```bash
git log --oneline
```

## Additional Resources

- [GitHub Documentation](https://docs.github.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Note**: Always keep your `.env` file secure and never commit it to the repository!

