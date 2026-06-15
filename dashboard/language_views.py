from django.shortcuts import redirect

def set_language(request):
    """Simple language switcher"""
    if request.method == 'POST':
        lang = request.POST.get('language', 'ru')
        if lang in ['ru']:
            request.session['language'] = lang
    
    next_url = request.POST.get('next', '/')
    return redirect(next_url)
