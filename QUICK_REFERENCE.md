# ⚡ Quick Reference Card

## 🚀 Essential Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Check Firebase status
python check_firebase.py

# Run migrations
python manage.py migrate

# Django shell
python manage.py shell
```

## 🌐 URLs

```
Home:       http://127.0.0.1:8000/
Admin:      http://127.0.0.1:8000/admin/
About:      http://127.0.0.1:8000/about/
Components: http://127.0.0.1:8000/components/
Circuit:    http://127.0.0.1:8000/circuit/
Simulation: http://127.0.0.1:8000/simulation/
Research:   http://127.0.0.1:8000/research/
Progress:   http://127.0.0.1:8000/progress/
Contact:    http://127.0.0.1:8000/contact/
```

## 📁 Key Files

```
serviceAccountKey.json  # Firebase credentials (add this)
.env                    # Environment config (create this)
bionic_app/views.py     # Page logic
bionic_app/models.py    # Data models
bionic_app/templates/   # HTML pages
bionic_site/settings.py # Django settings
```

## 🔥 Firebase Setup (3 Steps)

```bash
# 1. Create Firebase project
https://console.firebase.google.com/

# 2. Download serviceAccountKey.json
Project Settings → Service Accounts → Generate Key

# 3. Configure .env
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

## 📚 Documentation

```
START_HERE.md       → Quick start
FIREBASE_READY.md   → Firebase guide
INSTALLATION.md     → Full installation
INDEX.md            → Find anything
```

## 🧪 Test Firebase

```python
python manage.py shell

from bionic_app import firebase_config as fb
fb.add_document('test', {'hello': 'world'})
```

## 🐛 Troubleshooting

```bash
# Firebase not found
→ Add serviceAccountKey.json to project root

# Module not found
→ pip install -r requirements.txt

# Port in use
→ python manage.py runserver 8080

# Static files
→ python manage.py collectstatic
```

## ✅ Quick Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Migrations run
- [ ] Superuser created
- [ ] serviceAccountKey.json added (optional)
- [ ] .env configured (optional)
- [ ] Server running

## 🎯 Quick Start

```bash
# 1. Activate venv
venv\Scripts\activate

# 2. Start server
python manage.py runserver

# 3. Visit
http://127.0.0.1:8000/
```

**Done! 🎉**
