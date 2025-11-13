<div align="center">

# 🤖 Quantumix - Bionic Hand System

### *Advanced Django Web Platform for Bionic Hand Research & Simulation*

[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange.svg)](https://firebase.google.com/)
[![Three.js](https://img.shields.io/badge/Three.js-r128-black.svg)](https://threejs.org/)
[![License](https://img.shields.io/badge/License-Educational-purple.svg)](LICENSE)

[Features](#-features) • [Demo](#-live-demo) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## 📖 Overview

**Quantumix** is a comprehensive Django-powered web application designed for documenting, simulating, and managing bionic hand hardware projects. It combines cutting-edge 3D visualization with Firebase cloud storage to create an immersive research and development platform.

### 🎯 Project Goals

- **Document** bionic hand components and research
- **Simulate** realistic hand movements in 3D
- **Track** project progress and milestones
- **Store** research files and circuit diagrams
- **Collaborate** with team members and researchers

---

## ✨ Features

### 🏠 **Core Pages**

| Page | Description | Technology |
|------|-------------|------------|
| **Home** | Interactive landing page with project overview | HTML5, CSS3, Bootstrap 5 |
| **About** | Detailed bionic hand technology information | Responsive Design |
| **Components** | Dynamic component management system | Firebase Firestore |
| **Circuit & Working** | Circuit diagrams and working principles | Image Gallery |
| **Simulation** | Real-time hand movement simulation | JavaScript, Canvas API |
| **3D Simulation** | Interactive 3D hand model | Three.js, WebGL |
| **Advanced 3D** | Anatomically accurate hand with finger control | Three.js, OrbitControls |
| **Research Library** | Upload and manage research files | Firebase Storage |
| **Progress Timeline** | Visual project milestone tracker | Timeline UI |
| **Contact** | Contact form with Firebase integration | Form Validation |

### 🎮 **3D Simulation Features**

<div align="center">

#### **Realistic Hand Model**
- ✅ Anatomically accurate palm structure
- ✅ 5 fully articulated fingers (thumb, index, middle, ring, pinky)
- ✅ Multiple segments per finger (2-3 phalanges)
- ✅ Realistic skin materials and textures
- ✅ Joint knuckles and crease lines
- ✅ Fingernails with cuticles
- ✅ Fingerprint pads and ridges

#### **Animation Modes**
- 🖐️ **Open Hand** - All fingers extended
- ✊ **Close Hand** - Full fist position
- 🤜 **Grip Mode** - Power grip position
- 🤏 **Pinch Grip** - Thumb and index finger
- 👆 **Point Mode** - Index finger extended

#### **Interactive Controls**
- 🔄 **Rotate** - Click and drag to rotate 360°
- 🔍 **Zoom** - Mouse wheel to zoom in/out
- 🖱️ **Pan** - Right-click and drag to pan
- 🎨 **Lighting** - Professional multi-light setup
- 🌫️ **Shadows** - Real-time shadow rendering

</div>

### 🔥 **Firebase Integration**

#### **Firestore Collections**
```
📦 Firestore Database
├── 📁 components/          # Bionic hand components
├── 📁 simulation_logs/     # Simulation action logs
├── 📁 research_files/      # Research file metadata
├── 📁 contact_messages/    # Contact form submissions
├── 📁 progress/            # Project timeline entries
└── 📁 circuit_diagrams/    # Circuit diagram metadata
```

#### **Storage Buckets**
```
🗄️ Firebase Storage
├── 📂 components_images/   # Component photos
├── 📂 research_files/      # PDFs and documents
├── 📂 circuit_diagrams/    # Circuit images
└── 📂 progress_images/     # Timeline photos
```

---

## 🛠️ Technology Stack

<div align="center">

### **Frontend**
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)

### **Backend**
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

### **Database & Storage**
![Firestore](https://img.shields.io/badge/Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Firebase Storage](https://img.shields.io/badge/Storage-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

</div>

---

## 🚀 Installation

### **Prerequisites**

Before you begin, ensure you have:
- ✅ Python 3.10 or higher
- ✅ pip (Python package manager)
- ✅ Git
- ✅ Firebase account (free tier works!)

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/Skand03/Quantumix.git
cd Quantumix
```

### **Step 2: Create Virtual Environment**

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

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Required Packages:**
- Django 5.0.6
- firebase-admin 6.5.0
- python-dotenv 1.0.1
- Pillow 10.3.0
- whitenoise 6.6.0

### **Step 4: Firebase Setup**

#### **4.1 Create Firebase Project**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add Project"**
3. Enter project name: `quantumix-bionic-hand`
4. Disable Google Analytics (optional)
5. Click **"Create Project"**

#### **4.2 Enable Firestore Database**

1. In Firebase Console, go to **Build → Firestore Database**
2. Click **"Create Database"**
3. Select **"Start in test mode"**
4. Choose your region
5. Click **"Enable"**

#### **4.3 Enable Firebase Storage**

1. Go to **Build → Storage**
2. Click **"Get Started"**
3. Use default security rules
4. Click **"Done"**

#### **4.4 Get Service Account Key**

1. Go to **Project Settings** (⚙️ icon)
2. Navigate to **"Service Accounts"** tab
3. Click **"Generate New Private Key"**
4. Save the downloaded JSON file as `serviceAccountKey.json`
5. Place it in your project root directory

⚠️ **Important:** Add `serviceAccountKey.json` to `.gitignore` to keep it secure!

### **Step 5: Configure Environment**

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Firebase Settings
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

**Generate a Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Step 6: Run Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **Step 7: Create Superuser**

```bash
python manage.py createsuperuser
```

Enter your desired:
- Username
- Email
- Password

### **Step 8: Start Development Server**

```bash
python manage.py runserver
```

🎉 **Success!** Visit http://127.0.0.1:8000/ in your browser.

---

## 📂 Project Structure

```
Quantumix/
│
├── 📁 bionic_site/                 # Django project configuration
│   ├── settings.py                 # Main settings
│   ├── urls.py                     # Root URL configuration
│   └── wsgi.py                     # WSGI configuration
│
├── 📁 bionic_app/                  # Main application
│   │
│   ├── 📁 templates/               # HTML templates
│   │   ├── base.html               # Base template with navbar
│   │   ├── home.html               # Landing page
│   │   ├── about.html              # About bionic hand
│   │   ├── components.html         # Component management
│   │   ├── circuit.html            # Circuit diagrams
│   │   ├── simulation.html         # 2D simulation
│   │   ├── simulation_3d.html      # 3D hand model
│   │   ├── simulation_3d_advanced.html  # Advanced 3D
│   │   ├── research.html           # Research library
│   │   ├── progress.html           # Timeline
│   │   ├── contact.html            # Contact form
│   │   └── upload_pdf.html         # File upload
│   │
│   ├── 📁 static/                  # Static files
│   │   ├── 📁 css/
│   │   │   └── style.css           # Custom styles
│   │   ├── 📁 js/
│   │   │   └── main.js             # JavaScript functions
│   │   └── 📁 models/
│   │       └── README.md           # 3D model instructions
│   │
│   ├── firebase_config.py          # Firebase initialization
│   ├── views.py                    # View functions
│   ├── models.py                   # Django models
│   ├── forms.py                    # Django forms
│   ├── urls.py                     # App URL routing
│   └── admin.py                    # Admin configuration
│
├── 📁 Documentation/               # Project documentation
│   ├── FIREBASE_SETUP.md           # Firebase setup guide
│   ├── 3D_FEATURES_COMPLETE.md     # 3D features documentation
│   ├── HOW_TO_ADD_3D_HAND_MODEL.md # GLB model guide
│   └── PROJECT_SUMMARY.md          # Project overview
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create this)
├── .gitignore                      # Git ignore rules
├── serviceAccountKey.json          # Firebase credentials (add this)
├── quick_start.bat                 # Windows quick start script
└── README.md                       # This file
```

---

## 🎨 Usage Guide

### **Admin Panel**

Access the admin panel at: http://127.0.0.1:8000/admin/

**Features:**
- 👥 User management
- 📦 Component CRUD operations
- 📊 View simulation logs
- 📧 Read contact messages
- 📁 Manage research files
- 📅 Update progress timeline

### **Adding Components**

1. Navigate to **Components** page
2. Click **"Add Component"** button
3. Fill in the form:
   - Component name
   - Description
   - Upload image
4. Click **"Submit"**
5. Data automatically syncs to Firebase Firestore

### **Running 3D Simulations**

#### **Basic 3D Simulation**
1. Go to **3D Simulation** page
2. Use mouse to rotate the hand
3. Scroll to zoom in/out
4. Click mode buttons:
   - Open Hand
   - Close Hand
   - Grip Mode
   - Pinch Grip
   - Point Mode
5. Watch realistic finger animations

#### **Advanced 3D Simulation**
1. Navigate to **Advanced 3D** page
2. Full-screen immersive experience
3. Enhanced controls:
   - Left-click + drag: Rotate
   - Right-click + drag: Pan
   - Mouse wheel: Zoom
4. All 5 fingers with anatomical accuracy
5. Real-time shadow rendering

### **Uploading Research Files**

1. Go to **Research Library** page
2. Click **"Upload File"**
3. Enter file title
4. Select PDF or image file
5. Click **"Upload"**
6. File stored in Firebase Storage
7. Metadata saved to Firestore

### **Tracking Progress**

1. Visit **Progress Timeline** page
2. View chronological milestones
3. Add new entries via admin panel
4. Upload progress photos
5. Track project evolution

---

## 🔒 Firebase Security Rules

### **Firestore Rules**

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read access
    match /{document=**} {
      allow read: if true;
    }
    
    // Authenticated write access
    match /{document=**} {
      allow write: if request.auth != null;
    }
    
    // Specific collection rules
    match /simulation_logs/{logId} {
      allow create: if true;  // Allow simulation logging
    }
    
    match /contact_messages/{messageId} {
      allow create: if true;  // Allow contact form submissions
    }
  }
}
```

### **Storage Rules**

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Public read access
    match /{allPaths=**} {
      allow read: if true;
    }
    
    // Authenticated write access
    match /{allPaths=**} {
      allow write: if request.auth != null;
    }
    
    // File size limits
    match /research_files/{fileName} {
      allow write: if request.resource.size < 10 * 1024 * 1024;  // 10MB limit
    }
  }
}
```

---

## 🧪 Testing

### **Run All Tests**

```bash
python manage.py test
```

### **Test Specific Components**

```bash
# Test Firebase connection
python check_firebase.py

# Test file uploads
python test_file_uploads.py

# Test all pages
python test_pages.py
```

### **Manual Testing Checklist**

- [ ] Home page loads correctly
- [ ] Navigation menu works
- [ ] Components can be added/viewed
- [ ] Circuit diagrams display
- [ ] 2D simulation responds to clicks
- [ ] 3D hand model renders
- [ ] Advanced 3D controls work
- [ ] Files upload to Firebase
- [ ] Progress timeline displays
- [ ] Contact form submits
- [ ] Admin panel accessible

---

## 🚢 Deployment

### **Production Checklist**

1. **Environment Variables**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   SECRET_KEY=your-production-secret-key
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Security Settings**
   - Enable HTTPS
   - Set secure cookies
   - Configure CORS
   - Update Firebase rules

### **Deploy with Gunicorn**

```bash
pip install gunicorn
gunicorn bionic_site.wsgi:application --bind 0.0.0.0:8000
```

### **Deploy to Heroku**

```bash
# Install Heroku CLI
heroku login
heroku create quantumix-bionic-hand

# Add buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### **Deploy to PythonAnywhere**

1. Upload code to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Set environment variables
6. Reload web app

---

## 🐛 Troubleshooting

### **Common Issues**

#### **Firebase Connection Error**
```
Error: Could not connect to Firebase
```
**Solution:**
- Verify `serviceAccountKey.json` exists in project root
- Check Firebase Storage Bucket name in `.env`
- Ensure Firestore and Storage are enabled in Firebase Console

#### **Template Not Found**
```
TemplateDoesNotExist at /
```
**Solution:**
- Verify `bionic_app` is in `INSTALLED_APPS` in `settings.py`
- Check template files are in `bionic_app/templates/`
- Run `python manage.py collectstatic`

#### **Static Files Not Loading**
```
404 Error for CSS/JS files
```
**Solution:**
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in `settings.py`
- Verify `whitenoise` is in `MIDDLEWARE`

#### **3D Model Not Showing**
```
Black screen in 3D simulation
```
**Solution:**
- Open browser console (F12) to check for errors
- Verify Three.js CDN is loading
- Check WebGL support in browser
- Try different browser (Chrome recommended)

#### **File Upload Fails**
```
Error uploading file to Firebase
```
**Solution:**
- Check Firebase Storage rules
- Verify file size is under 10MB
- Ensure Storage Bucket name is correct
- Check internet connection

---

## 📚 Documentation

### **Additional Resources**

- 📖 [Django Documentation](https://docs.djangoproject.com/)
- 🔥 [Firebase Documentation](https://firebase.google.com/docs)
- 🎨 [Three.js Documentation](https://threejs.org/docs/)
- 🅱️ [Bootstrap Documentation](https://getbootstrap.com/docs/)

### **Project Documentation**

- [Firebase Setup Guide](FIREBASE_SETUP.md)
- [3D Features Documentation](3D_FEATURES_COMPLETE.md)
- [Adding 3D Models](HOW_TO_ADD_3D_HAND_MODEL.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **How to Contribute**

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Skand03/Quantumix.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow PEP 8 style guide
   - Add tests if applicable

4. **Commit Your Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

### **Contribution Guidelines**

- ✅ Follow existing code style
- ✅ Write meaningful commit messages
- ✅ Update documentation
- ✅ Add tests for new features
- ✅ Ensure all tests pass
- ✅ Be respectful and collaborative

---

## 📜 License

This project is licensed under the **Educational License** - see the [LICENSE](LICENSE) file for details.

**Usage Terms:**
- ✅ Free for educational purposes
- ✅ Free for research projects
- ✅ Free for personal learning
- ❌ Commercial use requires permission

---

## 👥 Team

### **Project Lead**
- **Skand** - *Full Stack Developer* - [GitHub](https://github.com/Skand03)

### **Contributors**
- Your name could be here! See [Contributing](#-contributing)

---

## 🙏 Acknowledgments

Special thanks to:

- **Django Software Foundation** - For the amazing web framework
- **Google Firebase** - For cloud infrastructure
- **Three.js Team** - For 3D graphics library
- **Bootstrap Team** - For responsive UI components
- **Open Source Community** - For inspiration and support

---

## 📞 Contact & Support

### **Get Help**

- 📧 **Email:** Use the contact form on the website
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/Skand03/Quantumix/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Skand03/Quantumix/discussions)
- 📖 **Documentation:** Check the `/Documentation` folder

### **Stay Updated**

- ⭐ Star this repository
- 👀 Watch for updates
- 🔔 Enable notifications

---

## 🎯 Roadmap

### **Upcoming Features**

- [ ] Real-time multiplayer simulation
- [ ] Machine learning hand gesture recognition
- [ ] Mobile app (React Native)
- [ ] VR/AR integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API for external integrations
- [ ] Collaborative research tools

---

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/Skand03/Quantumix)
![GitHub stars](https://img.shields.io/github/stars/Skand03/Quantumix?style=social)
![GitHub forks](https://img.shields.io/github/forks/Skand03/Quantumix?style=social)
![GitHub issues](https://img.shields.io/github/issues/Skand03/Quantumix)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Skand03/Quantumix)

---

<div align="center">

### **Made with ❤️ by the Quantumix Team**

**[⬆ Back to Top](#-quantumix---bionic-hand-system)**

---

*If you found this project helpful, please consider giving it a ⭐!*

</div>
