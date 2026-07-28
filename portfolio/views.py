# portfolio/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactMessageForm

def index(request):
    """Renders your main portfolio page."""
    return render(request, 'index.html')

def send_message(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()  # Saves directly into db.sqlite3
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent successfully.'})
        else:
            # Prints form errors to browser console / Network tab
            print("Form errors:", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)