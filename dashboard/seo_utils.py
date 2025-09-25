# SEO utilities for bionic hand dashboard
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
import json

def generate_sitemap(request):
    """Generate XML sitemap for better SEO"""
    
    # Define all pages with their priority and change frequency
    pages = [
        {
            'url': reverse('dashboard'),
            'priority': '1.0',
            'changefreq': 'daily',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('model_testing'),
            'priority': '0.9',
            'changefreq': 'weekly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('analytics'),
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('control'),
            'priority': '0.8',
            'changefreq': 'daily',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('medical_dashboard'),
            'priority': '0.9',
            'changefreq': 'weekly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('doctor_panel'),
            'priority': '0.7',
            'changefreq': 'monthly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('settings'),
            'priority': '0.6',
            'changefreq': 'monthly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('about'),
            'priority': '0.5',
            'changefreq': 'monthly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('future_scope'),
            'priority': '0.6',
            'changefreq': 'monthly',
            'lastmod': timezone.now().date()
        },
        {
            'url': reverse('impact'),
            'priority': '0.6',
            'changefreq': 'monthly',
            'lastmod': timezone.now().date()
        }
    ]
    
    # Build absolute URLs
    base_url = request.build_absolute_uri('/').rstrip('/')
    for page in pages:
        page['url'] = base_url + page['url']
    
    # Generate XML sitemap
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    
    for page in pages:
        xml_content += f"""
    <url>
        <loc>{page['url']}</loc>
        <lastmod>{page['lastmod']}</lastmod>
        <changefreq>{page['changefreq']}</changefreq>
        <priority>{page['priority']}</priority>
    </url>"""
    
    xml_content += "\n</urlset>"
    
    response = HttpResponse(xml_content, content_type='application/xml')
    return response

def generate_robots_txt(request):
    """Generate robots.txt for search engine crawlers"""
    
    base_url = request.build_absolute_uri('/').rstrip('/')
    sitemap_url = f"{base_url}/sitemap.xml"
    
    robots_content = f"""User-agent: *
Allow: /dashboard/
Allow: /static/
Disallow: /api/
Disallow: /admin/
Disallow: /accounts/

# Sitemap location
Sitemap: {sitemap_url}

# Crawl delay (be nice to the server)
Crawl-delay: 1
"""
    
    response = HttpResponse(robots_content, content_type='text/plain')
    return response

def generate_manifest_json(request):
    """Generate web app manifest for PWA functionality"""
    
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    manifest = {
        "name": "Bionic Hand IoT Dashboard",
        "short_name": "BionicHand",
        "description": "Advanced bionic hand monitoring and control system",
        "start_url": "/dashboard/",
        "display": "standalone",
        "background_color": "#1a1a1a",
        "theme_color": "#4a90e2",
        "orientation": "portrait-primary",
        "categories": ["medical", "health", "productivity"],
        "icons": [
            {
                "src": f"{base_url}/static/dashboard/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "maskable"
            },
            {
                "src": f"{base_url}/static/dashboard/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            }
        ],
        "screenshots": [
            {
                "src": f"{base_url}/static/dashboard/images/screenshot-desktop.png",
                "sizes": "1280x720",
                "type": "image/png",
                "form_factor": "wide"
            },
            {
                "src": f"{base_url}/static/dashboard/images/screenshot-mobile.png",
                "sizes": "375x812",
                "type": "image/png",
                "form_factor": "narrow"
            }
        ]
    }
    
    response = HttpResponse(json.dumps(manifest, indent=2), content_type='application/json')
    return response

def generate_structured_data():
    """Generate structured data for rich snippets"""
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Bionic Hand IoT Dashboard",
        "description": "Professional bionic hand prosthetic monitoring and control system with machine learning integration",
        "applicationCategory": "Medical Device Software",
        "operatingSystem": "Web-based",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "creator": {
            "@type": "Organization",
            "name": "Quantumix Technologies"
        },
        "featureList": [
            "Real-time EMG signal monitoring",
            "Grip force measurement and analysis",
            "Temperature monitoring and alerts",
            "Machine learning image analysis",
            "Advanced data analytics and reporting",
            "Medical professional integration",
            "IoT device connectivity",
            "Mobile responsive design"
        ],
        "screenshot": [
            "https://example.com/static/dashboard/images/dashboard-screenshot.png",
            "https://example.com/static/dashboard/images/analytics-screenshot.png"
        ]
    }
    
    return structured_data

def optimize_meta_tags(page_name, request):
    """Generate optimized meta tags for specific pages"""
    
    base_descriptions = {
        'dashboard': {
            'title': 'Bionic Hand IoT Dashboard - Real-time Monitoring & Control',
            'description': 'Monitor your bionic hand prosthetic in real-time with advanced IoT sensors, EMG signals, grip force analysis, and comprehensive health metrics.',
            'keywords': 'bionic hand dashboard, prosthetic monitoring, EMG signals, grip force, real-time analytics'
        },
        'model_testing': {
            'title': 'ML Model Testing - Bionic Hand Image Analysis',
            'description': 'Test machine learning models for bionic hand detection and analysis. Upload images for AI-powered prosthetic evaluation and medical insights.',
            'keywords': 'machine learning, bionic hand detection, image analysis, AI prosthetics, medical ML'
        },
        'analytics': {
            'title': 'Bionic Hand Analytics - Performance & Health Reports',
            'description': 'Comprehensive analytics and performance reports for your bionic hand. Track usage patterns, health metrics, and optimization recommendations.',
            'keywords': 'bionic hand analytics, performance reports, health metrics, usage statistics'
        },
        'medical_dashboard': {
            'title': 'Medical Dashboard - Professional Bionic Hand Management',
            'description': 'Professional medical dashboard for healthcare providers managing bionic hand patients. Clinical data, reports, and patient monitoring tools.',
            'keywords': 'medical dashboard, healthcare providers, clinical data, patient monitoring, prosthetic management'
        },
        'control': {
            'title': 'Bionic Hand Control Panel - Device Management',
            'description': 'Control panel for bionic hand device management. Start/stop operations, emergency controls, and real-time device configuration.',
            'keywords': 'bionic hand control, device management, emergency stop, prosthetic controls'
        }
    }
    
    page_meta = base_descriptions.get(page_name, {
        'title': 'Bionic Hand IoT Dashboard - Quantumix Technologies',
        'description': 'Advanced bionic hand prosthetic technology with IoT monitoring and machine learning analysis.',
        'keywords': 'bionic hand, prosthetic limb, IoT, machine learning'
    })
    
    # Add common keywords
    common_keywords = 'assistive technology, medical devices, rehabilitation, disability support, prosthetics'
    page_meta['keywords'] = f"{page_meta['keywords']}, {common_keywords}"
    
    return page_meta

def generate_breadcrumb_schema(page_hierarchy):
    """Generate breadcrumb structured data"""
    
    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    for i, (name, url) in enumerate(page_hierarchy, 1):
        breadcrumb_list["itemListElement"].append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    
    return breadcrumb_list