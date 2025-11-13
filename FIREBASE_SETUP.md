# Firebase Setup Instructions

## Complete Firebase Configuration Guide

### Step 1: Create Firebase Project

1. Visit https://console.firebase.google.com/
2. Click "Add project" (or "Create a project")
3. Enter project name: `bionic-hand-system` (or your preferred name)
4. Click "Continue"
5. Disable Google Analytics (optional for this project)
6. Click "Create project"
7. Wait for project creation to complete
8. Click "Continue"

### Step 2: Enable Firestore Database

1. In the left sidebar, click "Firestore Database"
2. Click "Create database"
3. Select "Start in test mode" (for development)
4. Click "Next"
5. Choose a Cloud Firestore location (select closest to you)
6. Click "Enable"
7. Wait for database creation

### Step 3: Enable Firebase Storage

1. In the left sidebar, click "Storage"
2. Click "Get started"
3. Review security rules (default is fine for development)
4. Click "Next"
5. Choose a location (same as Firestore)
6. Click "Done"

### Step 4: Get Service Account Key

1. Click the gear icon (⚙️) next to "Project Overview"
2. Click "Project settings"
3. Go to "Service accounts" tab
4. Click "Generate new private key"
5. A dialog will appear - click "Generate key"
6. A JSON file will download automatically
7. Rename this file to `serviceAccountKey.json`
8. Move it to your Django project root directory

**File location**: Place `serviceAccountKey.json` in the same directory as `manage.py`

### Step 5: Get Storage Bucket Name

1. Go to Storage in Firebase Console
2. Look at the top - you'll see "gs://your-project-id.appspot.com"
3. Copy the bucket name: `your-project-id.appspot.com`
4. Add this to your `.env` file:

```env
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

### Step 6: Configure Firestore Collections

The application will automatically create these collections when you use the features:

- `components/` - Component data
- `simulation_logs/` - Simulation logs
- `research_files/` - Research file metadata
- `contact_messages/` - Contact form submissions
- `progress/` - Timeline entries
- `circuit_diagrams/` - Circuit diagram metadata

You don't need to create them manually - they'll be created on first write.

### Step 7: Set Firestore Security Rules

For development, use these permissive rules:

1. Go to Firestore Database
2. Click "Rules" tab
3. Replace with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read access to all
    match /{document=**} {
      allow read: if true;
    }
    
    // Allow write access to all (development only)
    match /{document=**} {
      allow write: if true;
    }
  }
}
```

4. Click "Publish"

**For Production**, use these stricter rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read access
    match /{document=**} {
      allow read: if true;
    }
    
    // Authenticated write access
    match /components/{componentId} {
      allow write: if request.auth != null;
    }
    
    match /simulation_logs/{logId} {
      allow write: if true;
    }
    
    match /research_files/{fileId} {
      allow write: if request.auth != null;
    }
    
    match /contact_messages/{messageId} {
      allow write: if true;
    }
    
    match /progress/{progressId} {
      allow write: if request.auth != null;
    }
  }
}
```

### Step 8: Set Storage Security Rules

For development:

1. Go to Storage
2. Click "Rules" tab
3. Replace with:

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

4. Click "Publish"

**For Production**:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Public read
    match /{allPaths=**} {
      allow read: if true;
    }
    
    // Authenticated write with size limit
    match /{allPaths=**} {
      allow write: if request.auth != null 
                   && request.resource.size < 10 * 1024 * 1024; // 10MB limit
    }
  }
}
```

### Step 9: Verify Setup

Test your Firebase connection:

```python
# Run Python shell
python manage.py shell

# Test Firebase
from bionic_app import firebase_config as fb

# Test Firestore
test_data = {'test': 'Hello Firebase'}
doc_id = fb.add_document('test_collection', test_data)
print(f"Document created with ID: {doc_id}")

# Verify in Firebase Console
```

### Step 10: Create Storage Folders

Firebase Storage folders are created automatically when you upload files. The app uses:

- `components_images/`
- `research_files/`
- `circuit_diagrams/`
- `progress_images/`

These will be created when you first upload files to each category.

## Troubleshooting

### Error: "Could not load credentials"

**Solution**: 
- Check `serviceAccountKey.json` is in project root
- Verify file name is exactly `serviceAccountKey.json`
- Check file is valid JSON

### Error: "Storage bucket not found"

**Solution**:
- Verify `FIREBASE_STORAGE_BUCKET` in `.env`
- Format: `project-id.appspot.com` (no `gs://` prefix)
- Check Storage is enabled in Firebase Console

### Error: "Permission denied"

**Solution**:
- Check Firestore/Storage security rules
- For development, use permissive rules shown above
- Verify rules are published

### Error: "Firebase app already initialized"

**Solution**:
- This is normal - Firebase initializes once
- Restart Django server if needed

## Firebase Console URLs

- **Main Console**: https://console.firebase.google.com/
- **Firestore**: https://console.firebase.google.com/project/YOUR_PROJECT/firestore
- **Storage**: https://console.firebase.google.com/project/YOUR_PROJECT/storage
- **Settings**: https://console.firebase.google.com/project/YOUR_PROJECT/settings/general

Replace `YOUR_PROJECT` with your actual project ID.

## Cost Considerations

Firebase Free Tier (Spark Plan) includes:

- **Firestore**: 1GB storage, 50K reads/day, 20K writes/day
- **Storage**: 5GB storage, 1GB/day downloads
- **Authentication**: Unlimited

This is sufficient for development and small projects.

## Security Best Practices

1. **Never commit** `serviceAccountKey.json` to version control
2. Add it to `.gitignore` (already done)
3. Use environment variables for sensitive data
4. Implement proper authentication for production
5. Use strict security rules in production
6. Monitor Firebase usage in Console
7. Set up billing alerts

## Next Steps

After Firebase setup:

1. Run Django migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Start server: `python manage.py runserver`
4. Test by adding a component or running simulation
5. Check Firebase Console to see data

## Support Resources

- Firebase Documentation: https://firebase.google.com/docs
- Firestore Guide: https://firebase.google.com/docs/firestore
- Storage Guide: https://firebase.google.com/docs/storage
- Python Admin SDK: https://firebase.google.com/docs/admin/setup
