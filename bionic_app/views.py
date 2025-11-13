"""
Views for Bionic Hand System
All data operations use Firebase Firestore and Storage
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import json

from .forms import ContactForm, ComponentForm, ResearchUploadForm, ProgressForm
from . import firebase_config as fb

def home(request):
    """Home page view"""
    context = {
        'page_title': 'Home - Bionic Hand System'
    }
    return render(request, 'home.html', context)

def about(request):
    """About bionic hand page"""
    context = {
        'page_title': 'About - Bionic Hand System'
    }
    return render(request, 'about.html', context)

def components(request):
    """Components page - displays all components from Firestore"""
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            # Prepare component data
            component_data = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'cost': float(form.cleaned_data['cost']) if form.cleaned_data.get('cost') else 0,
            }
            
            # Save image locally if provided
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                image_url = fb.save_file_locally(image_file, 'components_images')
                
                if image_url:
                    component_data['image_url'] = image_url
                    component_data['image_path'] = f'media/components_images/{image_file.name}'
            
            # Save metadata to Firestore
            doc_id = fb.add_document('components', component_data)
            if doc_id:
                messages.success(request, 'Component added successfully!')
            else:
                messages.warning(request, 'Component saved locally. Enable Firestore to save metadata to cloud.')
            
            return redirect('components')
    else:
        form = ComponentForm()
    
    # Get all components from Firestore
    components_list = fb.get_collection('components', order_by='created_at')
    
    context = {
        'page_title': 'Components - Bionic Hand System',
        'components': components_list,
        'form': form
    }
    return render(request, 'components.html', context)

def circuit(request):
    """Circuit and working page"""
    # Get circuit diagrams from Firestore
    diagrams = fb.get_collection('circuit_diagrams')
    
    context = {
        'page_title': 'Circuit & Working - Bionic Hand System',
        'diagrams': diagrams
    }
    return render(request, 'circuit.html', context)

def simulation(request):
    """Simulation page - simulates bionic hand actions"""
    if request.method == 'POST':
        action = request.POST.get('action', 'Unknown')
        
        # Create simulation log
        log_data = {
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'user': request.user.username if request.user.is_authenticated else 'guest'
        }
        
        # Save to Firestore
        doc_id = fb.add_document('simulation_logs', log_data)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'action': action,
                'message': f'Simulation: {action} executed successfully!'
            })
        
        messages.success(request, f'Simulation: {action} executed!')
        return redirect('simulation')
    
    # Get recent simulation logs
    logs = fb.get_collection('simulation_logs', order_by='created_at', limit=10)
    
    context = {
        'page_title': 'Simulation - Bionic Hand System',
        'logs': logs
    }
    return render(request, 'simulation.html', context)

def research(request):
    """Research library page - upload and view research files"""
    if request.method == 'POST':
        form = ResearchUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            file = request.FILES['file']
            
            # Save file locally (primary storage method)
            file_url = fb.save_file_locally(file, 'research_files')
            
            if file_url:
                # Save metadata to Firestore
                research_data = {
                    'title': title,
                    'filename': file.name,
                    'file_url': file_url,
                    'path': f'media/research_files/{file.name}',
                    'uploaded_on': datetime.now().isoformat(),
                    'file_size': file.size,
                    'content_type': file.content_type
                }
                
                doc_id = fb.add_document('research_files', research_data)
                if doc_id:
                    messages.success(request, f'File "{file.name}" uploaded successfully!')
                else:
                    messages.warning(request, 'File saved locally. Enable Firestore to save metadata to cloud.')
            else:
                messages.error(request, 'Failed to save file.')
            
            return redirect('research')
    else:
        form = ResearchUploadForm()
    
    # Get all research files from Firestore
    research_files = fb.get_collection('research_files', order_by='created_at')
    
    context = {
        'page_title': 'Research Library - Bionic Hand System',
        'research_files': research_files,
        'form': form
    }
    return render(request, 'research.html', context)

def progress(request):
    """Project progress timeline page"""
    if request.method == 'POST' and request.user.is_staff:
        form = ProgressForm(request.POST, request.FILES)
        if form.is_valid():
            progress_data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'date': form.cleaned_data['date'].isoformat(),
            }
            
            # Save image locally if provided
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                image_url = fb.save_file_locally(image_file, 'progress_images')
                
                if image_url:
                    progress_data['image_url'] = image_url
                    progress_data['image_path'] = f'media/progress_images/{image_file.name}'
            
            # Save metadata to Firestore
            doc_id = fb.add_document('progress', progress_data)
            if doc_id:
                messages.success(request, 'Progress entry added successfully!')
            else:
                messages.warning(request, 'Progress saved locally. Enable Firestore to save metadata to cloud.')
            
            return redirect('progress')
    else:
        form = ProgressForm()
    
    # Get all progress entries from Firestore
    progress_list = fb.get_collection('progress', order_by='date')
    
    context = {
        'page_title': 'Project Progress - Bionic Hand System',
        'progress_list': progress_list,
        'form': form
    }
    return render(request, 'progress.html', context)

def contact(request):
    """Contact page - save messages to Firestore"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Prepare contact message data
            message_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to Firestore
            doc_id = fb.add_document('contact_messages', message_data)
            if doc_id:
                messages.success(request, 'Your message has been sent successfully!')
            else:
                messages.error(request, 'Failed to send message. Please try again.')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'page_title': 'Contact - Bionic Hand System',
        'form': form
    }
    return render(request, 'contact.html', context)

def simulation_3d(request):
    """
    3D Interactive Simulation Page
    - 3D hand model with Three.js
    - 2D animation fallback
    - Multiple hand modes
    """
    # Get recent simulation logs
    logs = fb.get_collection('simulation_logs', order_by='created_at', limit=10)
    
    context = {
        'page_title': '3D Simulation - Bionic Hand System',
        'logs': logs
    }
    return render(request, 'simulation_3d.html', context)

def simulation_3d_advanced(request):
    """
    Advanced 3D Simulation with GLB Model Support
    - Loads GLB hand model
    - Fallback to geometric shapes
    - Full screen 3D experience
    """
    context = {
        'page_title': 'Advanced 3D Simulation - Bionic Hand System'
    }
    return render(request, 'simulation_3d_advanced.html', context)

def upload_pdf(request):
    """
    Dedicated PDF upload view
    - Saves PDF file locally to media/pdfs/
    - Stores metadata in Firestore
    """
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        
        # Validate file type
        if not pdf_file.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed!')
            return redirect('upload_pdf')
        
        # Save PDF locally
        file_url = fb.save_file_locally(pdf_file, 'pdfs')
        
        if file_url:
            # Prepare metadata for Firestore
            pdf_metadata = {
                'filename': pdf_file.name,
                'path': f'media/pdfs/{pdf_file.name}',
                'file_url': file_url,
                'uploaded_at': datetime.now().isoformat(),
                'file_size': pdf_file.size,
                'content_type': pdf_file.content_type
            }
            
            # Save metadata to Firestore
            doc_id = fb.add_document('pdf_files', pdf_metadata)
            
            if doc_id:
                messages.success(request, f'PDF "{pdf_file.name}" uploaded successfully!')
            else:
                messages.warning(request, 'PDF saved locally. Enable Firestore to save metadata.')
        else:
            messages.error(request, 'Failed to save PDF file.')
        
        return redirect('upload_pdf')
    
    # Get all PDFs from Firestore
    pdf_list = fb.get_collection('pdf_files', order_by='uploaded_at')
    
    context = {
        'page_title': 'PDF Upload - Bionic Hand System',
        'pdf_list': pdf_list
    }
    return render(request, 'upload_pdf.html', context)
