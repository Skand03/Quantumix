"""
Firebase Configuration and Helper Functions
Handles Firestore and Firebase Storage operations
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
from django.conf import settings

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase with service account key"""
    if not firebase_admin._apps:
        try:
            # Path to service account key
            cred_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
            
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', 'your-project-id.appspot.com')
                })
                print("✅ Firebase initialized successfully")
            else:
                print("⚠️ serviceAccountKey.json not found. Firebase features disabled.")
                return None
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            return None
    
    return firebase_admin.get_app()

# Initialize on import
initialize_firebase()

# Firestore client
def get_firestore_client():
    """Get Firestore database client"""
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

# Storage client
def get_storage_bucket():
    """Get Firebase Storage bucket"""
    try:
        return storage.bucket()
    except Exception as e:
        print(f"Error getting Storage bucket: {e}")
        return None

# Firestore Helper Functions
def add_document(collection_name, data):
    """Add a new document to a Firestore collection"""
    try:
        db = get_firestore_client()
        if db:
            data['created_at'] = datetime.now()
            doc_ref = db.collection(collection_name).add(data)
            return doc_ref[1].id
        return None
    except Exception as e:
        print(f"Error adding document: {e}")
        return None

def set_document(collection_name, document_id, data):
    """Set/Update a document in Firestore"""
    try:
        db = get_firestore_client()
        if db:
            data['updated_at'] = datetime.now()
            db.collection(collection_name).document(document_id).set(data, merge=True)
            return True
        return False
    except Exception as e:
        print(f"Error setting document: {e}")
        return False

def get_document(collection_name, document_id):
    """Get a single document from Firestore"""
    try:
        db = get_firestore_client()
        if db:
            doc = db.collection(collection_name).document(document_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
        return None
    except Exception as e:
        print(f"Error getting document: {e}")
        return None

def get_collection(collection_name, order_by=None, limit=None):
    """Get all documents from a Firestore collection"""
    try:
        db = get_firestore_client()
        if db:
            query = db.collection(collection_name)
            
            if order_by:
                query = query.order_by(order_by)
            
            if limit:
                query = query.limit(limit)
            
            docs = query.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            return results
        return []
    except Exception as e:
        print(f"Error getting collection: {e}")
        return []

def delete_document(collection_name, document_id):
    """Delete a document from Firestore"""
    try:
        db = get_firestore_client()
        if db:
            db.collection(collection_name).document(document_id).delete()
            return True
        return False
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False

# Firebase Storage Helper Functions
def upload_file(file, folder_name, filename=None):
    """
    Try to upload file to Firebase Storage.
    If Firebase Storage is not available, returns None (caller should save locally)
    """
    try:
        bucket = get_storage_bucket()
        if bucket:
            if filename is None:
                filename = file.name
            
            # Create blob path
            blob_path = f"{folder_name}/{filename}"
            blob = bucket.blob(blob_path)
            
            # Upload file
            blob.upload_from_file(file, content_type=file.content_type)
            
            # Make public and get URL
            blob.make_public()
            return blob.public_url
        return None
    except Exception as e:
        print(f"Firebase Storage not available: {e}")
        return None

def save_file_locally(file, folder_name):
    """
    Save file to local media storage
    Returns the local file path
    """
    try:
        from django.core.files.storage import default_storage
        from django.conf import settings
        import os
        
        # Create folder if it doesn't exist
        folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Save file
        file_path = os.path.join(folder_name, file.name)
        saved_path = default_storage.save(file_path, file)
        
        # Return URL path
        return f'{settings.MEDIA_URL}{saved_path}'
    except Exception as e:
        print(f"Error saving file locally: {e}")
        return None

def delete_file(file_path):
    """Delete a file from Firebase Storage"""
    try:
        bucket = get_storage_bucket()
        if bucket:
            blob = bucket.blob(file_path)
            blob.delete()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
