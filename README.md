# Bionic Hand System - Django Web Application

A complete Django web application for documenting, simulating, and managing a bionic hand hardware project. This platform uses Firebase (Firestore + Storage) as the backend database.

## Features

- **Home Page**: Overview and introduction to the bionic hand system
- **About Page**: Detailed information about bionic hand technology
- **Components Page**: Dynamic component management with Firebase Firestore
- **Circuit & Working**: Circuit diagrams and working principles
- **Simulation Page**: Digital simulation of bionic hand movements
- **Research Library**: Upload and manage research files (PDFs, images)
- **Project Progress**: Timeline view of project milestones
- **Contact Page**: Contact form with Firebase storage
- **Admin Panel**: Django admin for managing all data

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Bootstrap Icons
- Responsive Design

### Backend
- Django 4.2+
- Python 3.10+
- Firebase Admin SDK

### Database
- Firebase Firestore (NoSQL)
- Firebase Storage (file uploads)

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Firebase project with Firestore and Storage enabled

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Bionic_Hand_System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing project
3. Enable Firestore Database
4. Enable Firebase Storage
5. Go to Project Settings > Service Accounts
6. Click "Generate New Private Key"
7. Save the downloaded JSON file as `serviceAccountKey.json` in the project root

### Step 5: Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your settings:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Firebase Firestore Collections

The application uses the following Firestore collections:

- `components/` - Bionic hand components
- `simulation_logs/` - Simulation action logs
- `research_files/` - Research file metadata
- `contact_messages/` - Contact form submissions
- `progress/` - Project timeline entries
- `circuit_diagrams/` - Circuit diagram metadata

## Firebase Storage Folders

- `components_images/` - Component images
- `research_files/` - Research PDFs and documents
- `circuit_diagrams/` - Circuit diagram images
- `progress_images/` - Progress timeline images

## Firestore Security Rules

Add these rules to your Firebase Firestore:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read access to all documents
    match /{document=**} {
      allow read: if true;
    }
    
    // Allow write access only to authenticated users
    match /{document=**} {
      allow write: if request.auth != null;
    }
  }
}
```

## Firebase Storage Rules

Add these rules to your Firebase Storage:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

## Project Structure

```
Bionic_Hand_System/
│
├── bionic_site/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── bionic_app/               # Main application
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── components.html
│   │   ├── circuit.html
│   │   ├── simulation.html
│   │   ├── research.html
│   │   ├── progress.html
│   │   └── contact.html
│   ├── static/               # Static files (CSS, JS, images)
│   ├── firebase_config.py    # Firebase configuration
│   ├── views.py              # View functions
│   ├── models.py             # Django models
│   ├── forms.py              # Django forms
│   ├── urls.py               # URL routing
│   └── admin.py              # Admin configuration
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example              # Environment variables template
├── serviceAccountKey.json    # Firebase credentials (add this)
└── README.md                 # This file
```

## Usage

### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/`

Use the superuser credentials you created to:
- Manage components
- View simulation logs
- View contact messages
- Manage research files
- Manage progress timeline

### Adding Components

1. Log in as admin
2. Go to Components page
3. Use the form to add new components with images
4. Data is automatically saved to Firebase Firestore

### Uploading Research Files

1. Go to Research Library page
2. Fill in the title and select a file
3. Click Upload - file is stored in Firebase Storage

### Running Simulations

1. Go to Simulation page
2. Click any action button (Open Hand, Close Hand, etc.)
3. Simulation logs are saved to Firestore

## Deployment

### Production Settings

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Add your domain to `ALLOWED_HOSTS`
3. Use a production-grade database if needed
4. Configure static files with WhiteNoise (already included)
5. Use gunicorn as WSGI server

### Deploy with Gunicorn

```bash
gunicorn bionic_site.wsgi:application --bind 0.0.0.0:8000
```

### Collect Static Files

```bash
python manage.py collectstatic
```

## Troubleshooting

### Firebase Connection Issues

- Verify `serviceAccountKey.json` is in the project root
- Check Firebase Storage Bucket name in `.env`
- Ensure Firestore and Storage are enabled in Firebase Console

### Template Not Found

- Verify `bionic_app` is in `INSTALLED_APPS`
- Check template files are in `bionic_app/templates/`

### Static Files Not Loading

- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Contact

For questions or support, use the Contact page on the website or reach out to the development team.

## Acknowledgments

- Django Framework
- Firebase Platform
- Bootstrap Framework
- Bootstrap Icons
