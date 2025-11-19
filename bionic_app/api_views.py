"""
API Views for PDF Processing Features
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .pdf_utils import PDFProcessor, TextTranslator, SimpleChatbot, AIChat
from .models import ResearchFile

# Initialize processors
pdf_processor = PDFProcessor()
translator = TextTranslator()

# Initialize AI Chat (set your OpenAI API key in settings if available)
ai_chat = AIChat(api_key=os.getenv('OPENAI_API_KEY'))

# Store extracted texts in memory (in production, use database or cache)
extracted_texts = {}


@require_http_methods(["GET"])
def extract_pdf_text(request, file_id):
    """Extract text from uploaded PDF"""
    try:
        # Get file from database
        research_file = ResearchFile.objects.get(id=file_id)
        
        # Check if already extracted
        if file_id in extracted_texts:
            return JsonResponse({
                'success': True,
                'text': extracted_texts[file_id],
                'cached': True
            })
        
        # Download file from Firebase Storage if needed
        # For now, assume file_url points to accessible PDF
        file_url = research_file.file_url
        
        # If file is local, extract directly
        # If file is remote (Firebase), download first
        if file_url.startswith('http'):
            import requests
            import tempfile
            
            # Download PDF to temp file
            response = requests.get(file_url)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name
            
            # Extract text
            text = pdf_processor.extract_text(tmp_path)
            
            # Clean up temp file
            os.unlink(tmp_path)
        else:
            # Local file
            text = pdf_processor.extract_text(file_url)
        
        # Cache extracted text
        extracted_texts[file_id] = text
        
        return JsonResponse({
            'success': True,
            'text': text,
            'length': len(text),
            'cached': False
        })
    
    except ResearchFile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'File not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
def translate_text(request):
    """Translate extracted text to target language"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return JsonResponse({
                'success': False,
                'error': 'No text provided'
            }, status=400)
        
        # Translate text
        translated_text = translator.translate(text, target_lang=target_lang)
        
        return JsonResponse({
            'success': True,
            'translated_text': translated_text,
            'target_lang': target_lang,
            'original_length': len(text),
            'translated_length': len(translated_text)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
def chat_with_pdf(request):
    """Chat with AI about PDF content"""
    try:
        data = json.loads(request.body)
        file_id = data.get('file_id')
        message = data.get('message', '')
        context = data.get('context', '')
        
        if not message:
            return JsonResponse({
                'success': False,
                'error': 'No message provided'
            }, status=400)
        
        # Get context from cache if not provided
        if not context and file_id in extracted_texts:
            context = extracted_texts[file_id]
        
        # Generate response using AI or simple chatbot
        if ai_chat.enabled:
            response = ai_chat.chat(message, context)
        else:
            response = SimpleChatbot.generate_response(message, context)
        
        return JsonResponse({
            'success': True,
            'response': response,
            'ai_enabled': ai_chat.enabled
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_pdf_summary(request, file_id):
    """Get AI-generated summary of PDF"""
    try:
        # Get extracted text
        if file_id not in extracted_texts:
            return JsonResponse({
                'success': False,
                'error': 'Please extract text first'
            }, status=400)
        
        context = extracted_texts[file_id]
        
        # Generate summary
        summary_question = "Please provide a comprehensive summary of this document."
        
        if ai_chat.enabled:
            summary = ai_chat.chat(summary_question, context)
        else:
            # Simple summary: first 500 words
            words = context.split()[:500]
            summary = ' '.join(words) + '...'
        
        return JsonResponse({
            'success': True,
            'summary': summary
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_supported_languages(request):
    """Get list of supported translation languages"""
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'pa': 'Punjabi',
        'te': 'Telugu',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'ur': 'Urdu',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'th': 'Thai',
        'vi': 'Vietnamese',
        'id': 'Indonesian',
        'ms': 'Malay',
        'fil': 'Filipino',
        'nl': 'Dutch',
        'pl': 'Polish',
        'tr': 'Turkish',
        'sv': 'Swedish',
        'no': 'Norwegian',
        'da': 'Danish',
        'fi': 'Finnish',
        'el': 'Greek',
        'cs': 'Czech',
        'ro': 'Romanian',
        'hu': 'Hungarian',
        'uk': 'Ukrainian',
        'he': 'Hebrew',
        'fa': 'Persian',
        'sw': 'Swahili',
        'am': 'Amharic',
    }
    
    return JsonResponse({
        'success': True,
        'languages': languages
    })
