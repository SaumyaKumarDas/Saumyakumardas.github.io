from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactMessageForm


def index(request):
    """Renders your main portfolio page."""
    return render(request, 'index.html')


def send_message(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # 1. Saves directly into your database (viewable in /admin/)
            message = form.save()

            # 2. Sends an email notification directly to your inbox
            try:
                # Adjust 'recipient_list' below to your personal receiving email address
                send_mail(
                    subject=f"New Portfolio Message from {message.name}",
                    message=(
                        f"You received a new message from your portfolio contact form:\n\n"
                        f"Name: {message.name}\n"
                        f"Email: {message.email}\n\n"
                        f"Message:\n{message.message}"
                    ),
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL set in settings.py
                    recipient_list=['dassaumya13@gmail.com'],  # <-- Replace with your personal email address
                    fail_silently=True,  # Prevents crashing the user response if SMTP is temporarily down
                )
            except Exception as e:
                print("Email failed to send:", e)

            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your message has been sent successfully.'
            })
        else:
            # Prints form errors to browser console / Network tab
            print("Form errors:", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)