"""
URL Configuration for Bionic Hand System App
"""
from django.urls import path
from . import views
from . import chatbot_views
# from . import api_views  # Commented out until PDF packages are installed

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('components/', views.components, name='components'),
    path('edit-component/<str:component_id>/', views.edit_component, name='edit_component'),
    path('delete-component/<str:component_id>/', views.delete_component, name='delete_component'),
    path('circuit/', views.circuit, name='circuit'),
    path('simulation/', views.simulation, name='simulation'),
    path('simulation-3d/', views.simulation_3d, name='simulation_3d'),
    path('simulation-3d-advanced/', views.simulation_3d_advanced, name='simulation_3d_advanced'),
    path('research/', views.research, name='research'),
    path('edit-research/<str:file_id>/', views.edit_research_file, name='edit_research_file'),
    path('delete-research/<str:file_id>/', views.delete_research_file, name='delete_research_file'),
    # path('research-enhanced/', views.research_enhanced, name='research_enhanced'),  # Available after installing packages
    path('contact/', views.contact, name='contact'),
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    
    # Chatbot API (Works without external packages)
    path('api/chat/', chatbot_views.chat_api, name='api_chat'),
    path('api/chatbot-status/', chatbot_views.chatbot_status, name='api_chatbot_status'),
    
    # API Endpoints for PDF Processing (Available after installing packages)
    # path('api/extract-pdf-text/<int:file_id>/', api_views.extract_pdf_text, name='api_extract_pdf_text'),
    # path('api/translate-text/', api_views.translate_text, name='api_translate_text'),
    # path('api/chat-with-pdf/', api_views.chat_with_pdf, name='api_chat_with_pdf'),
    # path('api/get-pdf-summary/<int:file_id>/', api_views.get_pdf_summary, name='api_get_pdf_summary'),
    # path('api/supported-languages/', api_views.get_supported_languages, name='api_supported_languages'),
]
