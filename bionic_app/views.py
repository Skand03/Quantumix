"""
Views for Bionic Hand System
All data operations use Firebase Firestore and Storage
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import json

from .forms import ContactForm, ComponentForm, ResearchUploadForm
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


def edit_research_file(request, file_id):
    """Edit research file metadata"""
    # Get existing file data
    file_data = fb.get_document('research_files', file_id)
    
    if not file_data:
        messages.error(request, 'File not found.')
        return redirect('research')
    
    if request.method == 'POST':
        form = ResearchUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Update file data
            updated_data = {
                'title': form.cleaned_data['title'],
            }
            
            # Handle new file upload (optional)
            if 'file' in request.FILES:
                # Delete old file if exists
                old_file_path = file_data.get('path', '')
                if old_file_path:
                    import os
                    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), old_file_path)
                    if os.path.exists(full_path):
                        try:
                            os.remove(full_path)
                        except Exception as e:
                            print(f"Error deleting old file: {e}")
                
                # Save new file
                new_file = request.FILES['file']
                file_url = fb.save_file_locally(new_file, 'research_files')
                
                if file_url:
                    updated_data['filename'] = new_file.name
                    updated_data['file_url'] = file_url
                    updated_data['path'] = f'media/research_files/{new_file.name}'
                    updated_data['file_size'] = new_file.size
                    updated_data['content_type'] = new_file.content_type
            else:
                # Keep existing file
                for key in ['filename', 'file_url', 'path', 'file_size', 'content_type']:
                    if key in file_data:
                        updated_data[key] = file_data[key]
            
            # Update in Firestore
            if fb.update_document('research_files', file_id, updated_data):
                messages.success(request, 'File updated successfully!')
            else:
                messages.warning(request, 'File updated locally. Enable Firestore to sync to cloud.')
            
            return redirect('research')
    else:
        # Pre-fill form with existing data
        initial_data = {
            'title': file_data.get('title', ''),
        }
        form = ResearchUploadForm(initial=initial_data)
    
    context = {
        'page_title': 'Edit Research File - Bionic Hand System',
        'form': form,
        'file': file_data,
        'file_id': file_id,
        'is_edit': True
    }
    return render(request, 'edit_research_file.html', context)


def delete_research_file(request, file_id):
    """Delete a research file"""
    if request.method == 'POST':
        # Get file data from Firestore
        file_data = fb.get_document('research_files', file_id)
        
        if file_data:
            # Delete local file if it exists
            file_path = file_data.get('path', '')
            if file_path:
                import os
                full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)
                if os.path.exists(full_path):
                    try:
                        os.remove(full_path)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
            
            # Delete from Firestore
            if fb.delete_document('research_files', file_id):
                messages.success(request, 'File deleted successfully!')
            else:
                messages.warning(request, 'File deleted locally but could not remove from cloud.')
        else:
            messages.error(request, 'File not found.')
    
    return redirect('research')


def edit_component(request, component_id):
    """Edit a component"""
    # Get existing component data
    component_data = fb.get_document('components', component_id)
    
    if not component_data:
        messages.error(request, 'Component not found.')
        return redirect('components')
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            # Update component data
            updated_data = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'cost': float(form.cleaned_data['cost']) if form.cleaned_data.get('cost') else 0,
            }
            
            # Handle new image upload
            if 'image' in request.FILES:
                # Delete old image if exists
                old_image_path = component_data.get('image_path', '')
                if old_image_path:
                    import os
                    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), old_image_path)
                    if os.path.exists(full_path):
                        try:
                            os.remove(full_path)
                        except Exception as e:
                            print(f"Error deleting old image: {e}")
                
                # Save new image
                image_file = request.FILES['image']
                image_url = fb.save_file_locally(image_file, 'components_images')
                
                if image_url:
                    updated_data['image_url'] = image_url
                    updated_data['image_path'] = f'media/components_images/{image_file.name}'
            else:
                # Keep existing image
                if 'image_url' in component_data:
                    updated_data['image_url'] = component_data['image_url']
                if 'image_path' in component_data:
                    updated_data['image_path'] = component_data['image_path']
            
            # Update in Firestore
            if fb.update_document('components', component_id, updated_data):
                messages.success(request, 'Component updated successfully!')
            else:
                messages.warning(request, 'Component updated locally. Enable Firestore to sync to cloud.')
            
            return redirect('components')
    else:
        # Pre-fill form with existing data
        initial_data = {
            'name': component_data.get('name', ''),
            'description': component_data.get('description', ''),
            'cost': component_data.get('cost', ''),
        }
        form = ComponentForm(initial=initial_data)
    
    context = {
        'page_title': 'Edit Component - Bionic Hand System',
        'form': form,
        'component': component_data,
        'component_id': component_id,
        'is_edit': True
    }
    return render(request, 'edit_component.html', context)


def delete_component(request, component_id):
    """Delete a component"""
    if request.method == 'POST':
        # Get component data from Firestore
        component_data = fb.get_document('components', component_id)
        
        if component_data:
            # Delete local image if it exists
            image_path = component_data.get('image_path', '')
            if image_path:
                import os
                full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path)
                if os.path.exists(full_path):
                    try:
                        os.remove(full_path)
                    except Exception as e:
                        print(f"Error deleting image: {e}")
            
            # Delete from Firestore
            if fb.delete_document('components', component_id):
                messages.success(request, 'Component deleted successfully!')
            else:
                messages.warning(request, 'Component deleted locally but could not remove from cloud.')
        else:
            messages.error(request, 'Component not found.')
    
    return redirect('components')


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
