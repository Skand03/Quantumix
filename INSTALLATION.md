# Complete Installation Instructions

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)
- Firebase account (free)

## Installation Steps

### Step 1: Download/Clone Project

If using Git:
```bash
git clone <repository-url>
cd Bionic_Hand_System
```

Or download and extract the ZIP file.

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2+
- Firebase Admin SDK
- python-dotenv
- gunicorn
- Pillow
- requests
- whitenoise

### Step 4: Firebase Configuration

#### 4.1 Create Firebase Project

1. Visit https://console.firebase.google.com/
2. Click "Add project"
3. Enter project name (e.g., "bionic-hand-system")
4. Disable Google Analytics (optional)
5. Click "Create project"

#### 4.2 Enable Firestore

1. In Firebase Console, click "Firestore Database"
2. Click "Create database"
3. Select "Start in test mode"
4. Choose a location (closest to you)
5. Click "Enable"

#### 4.3 Enable Storage

1. Click "Storage" in sidebar
2. Click "Get started"
3. Accept default rules
4. Choose same location as Firestore
5. Click "Done"

#### 4.4 Get Service Account Key

1. Click gear icon ⚙️ > "Project settings"
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Click "Generate key"
5. Save the downloaded JSON file as `serviceAccountKey.json`
6. **Place it in the project root** (same directory as manage.py)

**CRITICAL**: Never commit this file to Git! It's already in .gitignore.

#### 4.5 Get Storage Bucket Name

1. In Firebase Console, go to Storage
2. Look for the bucket URL: `gs://your-project-id.appspot.com`
3. Copy the bucket name: `your-project-id.appspot.com`

### Step 5: Environment Configuration

Create `.env` file:

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Edit `.env` file:

```env
SECRET_KEY=your-generated-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

Generate a SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your SECRET_KEY.

### Step 6: Database Setup

```bash
# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### Step 7: Firebase Security Rules

#### Firestore Rules

1. Go to Firebase Console > Firestore Database > Rules
2. Paste this code:

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

3. Click "Publish"

#### Storage Rules

1. Go to Firebase Console > Storage > Rules
2. Paste this code:

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

3. Click "Publish"

**Note**: These are development rules. For production, implement authentication.

### Step 8: Run the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 9: Access the Application

Open your browser and visit:

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

Login to admin with the superuser credentials you created.

## Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Firebase project created
- [ ] Firestore enabled
- [ ] Storage enabled
- [ ] serviceAccountKey.json in project root
- [ ] .env file configured
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Server running without errors
- [ ] Can access home page
- [ ] Can login to admin panel

## Testing the Setup

### Test 1: Home Page
Visit http://127.0.0.1:8000/ - should see the bionic hand home page

### Test 2: Admin Access
1. Visit http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Should see Django admin dashboard

### Test 3: Firebase Connection
1. Go to Components page
2. Login as admin
3. Add a test component
4. Check Firebase Console > Firestore
5. Should see "components" collection with your data

### Test 4: Simulation
1. Go to Simulation page
2. Click "Open Hand" button
3. Check Firebase Console > Firestore
4. Should see "simulation_logs" collection

### Test 5: File Upload
1. Go to Research Library
2. Upload a test PDF or image
3. Check Firebase Console > Storage
4. Should see file in "research_files" folder

## Common Issues & Solutions

### Issue: "serviceAccountKey.json not found"

**Solution**: 
- Verify file is in project root (same level as manage.py)
- Check file name is exactly `serviceAccountKey.json`
- Verify it's valid JSON

### Issue: "Storage bucket not found"

**Solution**:
- Check FIREBASE_STORAGE_BUCKET in .env
- Format: `project-id.appspot.com` (no gs:// prefix)
- Verify Storage is enabled in Firebase Console

### Issue: "Permission denied" in Firebase

**Solution**:
- Check Firestore/Storage security rules
- Make sure rules are published
- For development, use permissive rules shown above

### Issue: "Module not found"

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Static files not loading

**Solution**:
```bash
python manage.py collectstatic --noinput
```

### Issue: Port already in use

**Solution**:
```bash
# Use different port
python manage.py runserver 8080
```

### Issue: Virtual environment not activating

**Windows PowerShell**:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

## File Structure Verification

Your project should look like this:

```
Bionic_Hand_System/
├── bionic_site/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── bionic_app/
│   ├── templates/
│   ├── static/
│   ├── migrations/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── firebase_config.py
├── venv/                      # Virtual environment
├── manage.py
├── requirements.txt
├── .env                       # Your environment file
├── .env.example
├── serviceAccountKey.json     # Your Firebase key
├── serviceAccountKey.json.example
├── db.sqlite3                 # Created after migrate
├── README.md
├── SETUP_GUIDE.md
├── FIREBASE_SETUP.md
└── INSTALLATION.md           # This file
```

## Next Steps

After successful installation:

1. **Explore the Application**
   - Visit all pages (Home, About, Components, etc.)
   - Test navigation
   - Try the simulation

2. **Add Content**
   - Add components via admin panel
   - Upload research files
   - Create progress timeline entries

3. **Customize**
   - Modify templates in `bionic_app/templates/`
   - Update styles in `bionic_app/static/css/`
   - Add your own images and content

4. **Deploy** (Optional)
   - See README.md for deployment instructions
   - Configure production settings
   - Use production Firebase rules

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review SETUP_GUIDE.md
3. Check FIREBASE_SETUP.md for Firebase-specific issues
4. Review Django logs in terminal
5. Check Firebase Console for errors
6. Verify all files are in correct locations

## Security Reminders

- ✅ Never commit `serviceAccountKey.json`
- ✅ Never commit `.env` file
- ✅ Use strong SECRET_KEY
- ✅ Change DEBUG to False in production
- ✅ Implement proper authentication for production
- ✅ Use strict Firebase rules in production

## Success!

If you can:
- Access the home page
- Login to admin
- Add a component
- Run a simulation
- See data in Firebase Console

Then your installation is complete! 🎉

Start building your bionic hand documentation platform!
