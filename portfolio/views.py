import threading
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactMessageForm


def index(request):
    """Renders your main portfolio page."""
    return render(request, 'index.html')


def send_email_in_background(message):
    """Sends email in a separate background thread so HTTP requests don't time out."""
    try:
        send_mail(
            subject=f"New Portfolio Message from {message.name}",
            message=(
                f"You received a new message from your portfolio contact form:\n\n"
                f"Name: {message.name}\n"
                f"Email: {message.email}\n\n"
                f"Message:\n{message.message}"
            ),
            from_email=None,
            recipient_list=['dassaumya13@gmail.com'],
            fail_silently=True,
        )
    except Exception as e:
        print("Email background sending failed:", e)


def send_message(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # 1. Saves directly into database (/admin/)
            message = form.save()

            # 2. Trigger email sending in background thread
            threading.Thread(target=send_email_in_background, args=(message,)).start()

            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your message has been sent successfully.'
            })
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)