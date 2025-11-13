# Bionic Hand System - Complete Setup Guide

## Quick Start Guide

### 1. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Firebase Setup (IMPORTANT)

#### Step 2.1: Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click "Add project" or select existing project
3. Follow the setup wizard

#### Step 2.2: Enable Firestore Database

1. In Firebase Console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location
5. Click "Enable"

#### Step 2.3: Enable Firebase Storage

1. In Firebase Console, go to "Storage"
2. Click "Get started"
3. Accept the default security rules
4. Click "Done"

#### Step 2.4: Get Service Account Key

1. Go to Project Settings (gear icon) > Service Accounts
2. Click "Generate new private key"
3. Click "Generate key" - a JSON file will download
4. Rename the file to `serviceAccountKey.json`
5. Place it in the project root directory (same level as manage.py)

**IMPORTANT**: Never commit `serviceAccountKey.json` to version control!

#### Step 2.5: Get Storage Bucket Name

1. In Firebase Console, go to Storage
2. Copy the bucket name (format: `your-project-id.appspot.com`)
3. You'll need this for the `.env` file

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-django-secret-key-generate-a-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

To generate a new SECRET_KEY:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

## Firebase Security Rules

### Firestore Rules (Development)

Go to Firestore Database > Rules and paste:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if true;
      allow write: if true;
    }
  }
}
```

### Storage Rules (Development)

Go to Storage > Rules and paste:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read: if true;
      allow write: if true;
    }
  }
}
```

**Note**: These are permissive rules for development. For production, implement proper authentication.

## Testing the Application

### 1. Test Home Page
- Visit http://127.0.0.1:8000/
- Should see the home page with navigation

### 2. Test Admin Panel
- Visit http://127.0.0.1:8000/admin/
- Login with superuser credentials
- You should see the admin dashboard

### 3. Test Firebase Connection
- Go to Components page
- Try adding a component (requires admin login)
- Check Firebase Console > Firestore to see the data

### 4. Test Simulation
- Go to Simulation page
- Click any action button
- Check Firestore for simulation_logs collection

### 5. Test File Upload
- Go to Research Library
- Upload a PDF or image
- Check Firebase Storage for the uploaded file

## Troubleshooting

### Issue: Firebase not initialized

**Solution**: 
- Verify `serviceAccountKey.json` exists in project root
- Check file permissions
- Verify JSON format is correct

### Issue: Storage bucket error

**Solution**:
- Check `FIREBASE_STORAGE_BUCKET` in `.env`
- Format should be: `project-id.appspot.com`
- Verify Storage is enabled in Firebase Console

### Issue: Template not found

**Solution**:
- Verify `bionic_app` is in `INSTALLED_APPS` in settings.py
- Check templates are in `bionic_app/templates/`

### Issue: Static files not loading

**Solution**:
```bash
python manage.py collectstatic
```

### Issue: Module not found

**Solution**:
```bash
pip install -r requirements.txt
```

## Project Structure

```
Bionic_Hand_System/
│
├── bionic_site/              # Django project settings
│   ├── settings.py           # Main settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
│
├── bionic_app/               # Main application
│   ├── templates/            # HTML templates
│   ├── static/               # Static files
│   ├── firebase_config.py    # Firebase setup
│   ├── views.py              # View functions
│   ├── models.py             # Django models
│   ├── forms.py              # Django forms
│   ├── urls.py               # App URLs
│   └── admin.py              # Admin configuration
│
├── manage.py                 # Django management
├── requirements.txt          # Dependencies
├── .env                      # Environment variables (create this)
├── .env.example              # Environment template
├── serviceAccountKey.json    # Firebase credentials (add this)
├── README.md                 # Documentation
└── SETUP_GUIDE.md           # This file
```

## Next Steps

1. Customize the templates in `bionic_app/templates/`
2. Add your own components via the admin panel
3. Upload circuit diagrams to Firebase Storage
4. Add research files and documentation
5. Create project progress timeline entries

## Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Add your domain to `ALLOWED_HOSTS`
3. Use production Firebase security rules
4. Use a production database (PostgreSQL recommended)
5. Configure HTTPS
6. Use gunicorn or similar WSGI server

```bash
gunicorn bionic_site.wsgi:application --bind 0.0.0.0:8000
```

## Support

For issues or questions:
- Check the README.md
- Review Firebase Console for errors
- Check Django logs
- Use the Contact page on the website

## License

Educational project - modify as needed for your use case.
