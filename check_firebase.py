#!/usr/bin/env python
"""
Firebase Status Checker
Run this script to check if Firebase is properly configured
"""

import os
import sys

def check_firebase_setup():
    """Check Firebase configuration status"""
    print("=" * 60)
    print("🔥 Firebase Configuration Status Check")
    print("=" * 60)
    print()
    
    issues = []
    warnings = []
    success = []
    
    # Check 1: serviceAccountKey.json
    print("1. Checking serviceAccountKey.json...")
    if os.path.exists('serviceAccountKey.json'):
        print("   ✅ serviceAccountKey.json found")
        success.append("Service account key exists")
        
        # Check if it's valid JSON
        try:
            import json
            with open('serviceAccountKey.json', 'r') as f:
                data = json.load(f)
                if 'project_id' in data:
                    print(f"   ✅ Project ID: {data['project_id']}")
                    success.append(f"Project ID: {data['project_id']}")
                else:
                    print("   ⚠️  No project_id found in key file")
                    warnings.append("Service account key missing project_id")
        except Exception as e:
            print(f"   ❌ Invalid JSON: {e}")
            issues.append("Service account key is not valid JSON")
    else:
        print("   ❌ serviceAccountKey.json NOT found")
        issues.append("Missing serviceAccountKey.json")
        print("   → Download from Firebase Console > Project Settings > Service Accounts")
    print()
    
    # Check 2: .env file
    print("2. Checking .env file...")
    if os.path.exists('.env'):
        print("   ✅ .env file found")
        success.append(".env file exists")
        
        # Check for Firebase bucket
        with open('.env', 'r') as f:
            content = f.read()
            if 'FIREBASE_STORAGE_BUCKET' in content:
                # Extract bucket name
                for line in content.split('\n'):
                    if 'FIREBASE_STORAGE_BUCKET' in line and '=' in line:
                        bucket = line.split('=')[1].strip()
                        if bucket and bucket != 'your-project-id.appspot.com':
                            print(f"   ✅ Storage bucket configured: {bucket}")
                            success.append(f"Storage bucket: {bucket}")
                        else:
                            print("   ⚠️  Storage bucket not configured")
                            warnings.append("Update FIREBASE_STORAGE_BUCKET in .env")
            else:
                print("   ⚠️  FIREBASE_STORAGE_BUCKET not found in .env")
                warnings.append("Add FIREBASE_STORAGE_BUCKET to .env")
    else:
        print("   ⚠️  .env file NOT found")
        warnings.append("Missing .env file")
        print("   → Copy .env.example to .env and configure")
    print()
    
    # Check 3: Firebase Admin SDK
    print("3. Checking Firebase Admin SDK...")
    try:
        import firebase_admin
        print("   ✅ firebase-admin package installed")
        success.append("Firebase Admin SDK installed")
    except ImportError:
        print("   ❌ firebase-admin package NOT installed")
        issues.append("Firebase Admin SDK not installed")
        print("   → Run: pip install firebase-admin")
    print()
    
    # Check 4: Django app
    print("4. Checking Django configuration...")
    try:
        import django
        print("   ✅ Django installed")
        success.append("Django installed")
        
        # Check if bionic_app exists
        if os.path.exists('bionic_app'):
            print("   ✅ bionic_app directory found")
            success.append("bionic_app exists")
            
            # Check firebase_config.py
            if os.path.exists('bionic_app/firebase_config.py'):
                print("   ✅ firebase_config.py found")
                success.append("Firebase config file exists")
            else:
                print("   ❌ firebase_config.py NOT found")
                issues.append("Missing firebase_config.py")
        else:
            print("   ❌ bionic_app directory NOT found")
            issues.append("Missing bionic_app directory")
    except ImportError:
        print("   ❌ Django NOT installed")
        issues.append("Django not installed")
        print("   → Run: pip install -r requirements.txt")
    print()
    
    # Check 5: Try to initialize Firebase
    print("5. Testing Firebase initialization...")
    if not issues:
        try:
            # Set up Django settings
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bionic_site.settings')
            import django
            django.setup()
            
            from bionic_app import firebase_config as fb
            
            # Check if Firebase initialized
            if firebase_admin._apps:
                print("   ✅ Firebase initialized successfully!")
                success.append("Firebase initialized")
                
                # Try to get Firestore client
                db = fb.get_firestore_client()
                if db:
                    print("   ✅ Firestore client connected")
                    success.append("Firestore connected")
                else:
                    print("   ⚠️  Could not get Firestore client")
                    warnings.append("Firestore client issue")
                
                # Try to get Storage bucket
                bucket = fb.get_storage_bucket()
                if bucket:
                    print("   ✅ Storage bucket connected")
                    success.append("Storage connected")
                else:
                    print("   ⚠️  Could not get Storage bucket")
                    warnings.append("Storage bucket issue")
            else:
                print("   ⚠️  Firebase not initialized")
                warnings.append("Firebase not initialized")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            issues.append(f"Firebase initialization error: {e}")
    else:
        print("   ⏭️  Skipped (fix issues above first)")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print()
    
    if success:
        print(f"✅ Success ({len(success)}):")
        for item in success:
            print(f"   • {item}")
        print()
    
    if warnings:
        print(f"⚠️  Warnings ({len(warnings)}):")
        for item in warnings:
            print(f"   • {item}")
        print()
    
    if issues:
        print(f"❌ Issues ({len(issues)}):")
        for item in issues:
            print(f"   • {item}")
        print()
    
    # Final status
    print("=" * 60)
    if not issues and not warnings:
        print("🎉 Firebase is fully configured and ready to use!")
        print()
        print("Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/")
        print("3. Test features (components, simulation, etc.)")
        return 0
    elif not issues:
        print("⚠️  Firebase is partially configured")
        print()
        print("Fix the warnings above for full functionality")
        print("See TEST_FIREBASE.md for detailed instructions")
        return 1
    else:
        print("❌ Firebase is not configured")
        print()
        print("Fix the issues above to enable Firebase")
        print("See TEST_FIREBASE.md for step-by-step guide")
        return 2

if __name__ == '__main__':
    try:
        exit_code = check_firebase_setup()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nCheck cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
