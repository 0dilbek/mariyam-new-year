from .translations import get_all_translations

def language_context(request):
    """Add current language to template context"""
    lang = request.session.get('language', 'uz')
    translations = get_all_translations(lang)
    
    return {
        'current_language': lang,
        'is_uzbek': lang == 'uz',
        'is_karakalpak': lang == 'kaa',
        't': translations,  # All translations accessible via {{ t.key }}
    }

