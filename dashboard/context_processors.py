from .translations import get_all_translations

def language_context(request):
    """Add current language to template context - Karakalpak only"""
    lang = 'kaa'  # Faqat qoraqalpoqcha
    translations = get_all_translations(lang)
    
    return {
        'current_language': lang,
        'is_uzbek': False,
        'is_karakalpak': True,
        't': translations,  # All translations accessible via {{ t.key }}
    }

