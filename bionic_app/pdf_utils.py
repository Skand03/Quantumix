"""
PDF Processing Utilities
Handles PDF text extraction, translation, and AI chat features
"""

import PyPDF2
import pdfplumber
from googletrans import Translator
from langdetect import detect
import re

class PDFProcessor:
    """Handle PDF text extraction and processing"""
    
    @staticmethod
    def extract_text_pypdf2(pdf_path):
        """Extract text using PyPDF2"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            print(f"PyPDF2 extraction error: {e}")
            return None
    
    @staticmethod
    def extract_text_pdfplumber(pdf_path):
        """Extract text using pdfplumber (more accurate)"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text.strip()
        except Exception as e:
            print(f"pdfplumber extraction error: {e}")
            return None
    
    @staticmethod
    def extract_text(pdf_path):
        """Extract text using best available method"""
        # Try pdfplumber first (more accurate)
        text = PDFProcessor.extract_text_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2
        if not text or len(text) < 100:
            text = PDFProcessor.extract_text_pypdf2(pdf_path)
        
        if text:
            # Clean up text
            text = PDFProcessor.clean_text(text)
            return text
        
        return "Unable to extract text from PDF. The file might be scanned or encrypted."
    
    @staticmethod
    def clean_text(text):
        """Clean and format extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove page numbers (common patterns)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Fix common OCR errors
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬂ', 'fl')
        
        return text.strip()


class TextTranslator:
    """Handle text translation to multiple languages"""
    
    def __init__(self):
        self.translator = Translator()
    
    def translate(self, text, target_lang='en', source_lang='auto'):
        """Translate text to target language"""
        try:
            # Detect source language if auto
            if source_lang == 'auto':
                try:
                    source_lang = detect(text)
                except:
                    source_lang = 'en'
            
            # Don't translate if already in target language
            if source_lang == target_lang:
                return text
            
            # Split long text into chunks (Google Translate has limits)
            max_length = 5000
            if len(text) > max_length:
                chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
                translated_chunks = []
                
                for chunk in chunks:
                    result = self.translator.translate(chunk, dest=target_lang, src=source_lang)
                    translated_chunks.append(result.text)
                
                return ' '.join(translated_chunks)
            else:
                result = self.translator.translate(text, dest=target_lang, src=source_lang)
                return result.text
        
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails


class SimpleChatbot:
    """Simple rule-based chatbot for PDF Q&A"""
    
    @staticmethod
    def generate_response(question, context):
        """Generate response based on question and PDF context"""
        question_lower = question.lower()
        
        # Extract relevant sentences from context
        sentences = context.split('.')
        relevant_sentences = []
        
        # Simple keyword matching
        keywords = question_lower.split()
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords if len(keyword) > 3):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            # Return top 3 most relevant sentences
            response = '. '.join(relevant_sentences[:3])
            if response:
                return response + '.'
        
        # Fallback responses
        if 'summary' in question_lower or 'summarize' in question_lower:
            # Return first few sentences as summary
            summary_sentences = sentences[:5]
            return '. '.join(s.strip() for s in summary_sentences if s.strip()) + '.'
        
        elif 'what' in question_lower or 'how' in question_lower or 'why' in question_lower:
            return "Based on the document, I found relevant information. Please refer to the extracted text for detailed information."
        
        else:
            return "I'm analyzing the document. Could you please rephrase your question or be more specific?"


# Optional: OpenAI Integration (requires API key)
class AIChat:
    """Advanced AI chatbot using OpenAI (optional)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                self.client = openai
                self.enabled = True
            except ImportError:
                print("OpenAI package not installed")
                self.enabled = False
        else:
            self.enabled = False
    
    def chat(self, question, context):
        """Chat using OpenAI GPT"""
        if not self.enabled:
            # Fallback to simple chatbot
            return SimpleChatbot.generate_response(question, context)
        
        try:
            # Truncate context if too long
            max_context = 3000
            if len(context) > max_context:
                context = context[:max_context] + "..."
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Answer questions based on the provided document context."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"OpenAI error: {e}")
            # Fallback to simple chatbot
            return SimpleChatbot.generate_response(question, context)
