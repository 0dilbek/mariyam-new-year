from .translations import get_all_translations

def language_context(request):
    """Add current language and translations to template context."""
    lang = 'ru'
    translations = get_all_translations(lang)
    
    return {
        'current_language': lang,
        'is_russian': True,
        't': translations,  # All translations accessible via {{ t.key }}
    }
