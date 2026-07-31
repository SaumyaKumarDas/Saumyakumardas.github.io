import os
import threading
import resend
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactMessageForm


def index(request):
    return render(request, 'index.html')


def send_email_in_background(message):
    """Sends email reliably via HTTP API (Resend) - immune to Render SMTP port blocks."""
    try:
        resend.api_key = os.environ.get('RESEND_API_KEY')
        
        resend.Emails.send({
            "from": "Portfolio Contact <onboarding@resend.dev>",
            "to": ["dassaumya13@gmail.com"],
            "subject": f"New Portfolio Message from {message.name}",
            "html": f"""
                <h3>You received a new message from your portfolio:</h3>
                <p><strong>Name:</strong> {message.name}</p>
                <p><strong>Email:</strong> {message.email}</p>
                <p><strong>Message:</strong></p>
                <p>{message.message}</p>
            """
        })
        print("Email sent successfully via Resend API!")
    except Exception as e:
        print("Resend email failed:", e)


def send_message(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            threading.Thread(target=send_email_in_background, args=(message,)).start()
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your message has been sent successfully.'
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)