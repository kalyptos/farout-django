"""Views for communications app."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm, InternalMessageForm
from .models import InternalMessage
import logging

logger = logging.getLogger(__name__)


def contact_submit(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save submission
            submission = form.save(commit=False)

            # Capture metadata
            submission.ip_address = get_client_ip(request)
            submission.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

            # Simple spam check (honeypot field in template)
            honeypot = request.POST.get('website', '')
            if honeypot:
                submission.is_spam = True
                submission.status = 'archived'

            submission.save()

            # Send email notification to admins (optional)
            try:
                send_admin_notification(submission)
            except Exception as e:
                logger.error(f"Failed to send admin notification: {e}")

            # Send auto-response to submitter (optional)
            try:
                send_auto_response(submission)
                submission.response_sent = True
                from django.utils import timezone
                submission.response_sent_at = timezone.now()
                submission.save(update_fields=['response_sent', 'response_sent_at'])
            except Exception as e:
                logger.error(f"Failed to send auto-response: {e}")

            messages.success(
                request,
                _('Thank you for your message! We will get back to you soon.')
            )
            return redirect('contact')
        else:
            messages.error(
                request,
                _('Please correct the errors below.')
            )
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


@login_required
def message_inbox(request):
    """Display user's inbox."""
    user_messages = InternalMessage.objects.filter(
        recipient_id=request.user.id,
        is_deleted_by_recipient=False
    ).order_by('-created_at')[:50]

    unread_count = user_messages.filter(is_read=False).count()

    return render(request, 'communications/inbox.html', {
        'messages': user_messages,
        'unread_count': unread_count,
    })


@login_required
def message_send(request):
    """Send a new message."""
    if request.method == 'POST':
        form = InternalMessageForm(request.POST, sender_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Message sent successfully.'))
            return redirect('communications:inbox')
    else:
        form = InternalMessageForm(sender_user=request.user)

    return render(request, 'communications/send_message.html', {
        'form': form,
    })


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_admin_notification(submission):
    """Send email notification to admins about new contact submission."""
    if not hasattr(settings, 'ADMINS') or not settings.ADMINS:
        return

    subject = f'New Contact Form: {submission.subject}'
    message = f"""
New contact form submission:

From: {submission.name} <{submission.email}>
Subject: {submission.subject}

Message:
{submission.message}

---
Submitted: {submission.created_at}
IP: {submission.ip_address}
"""

    admin_emails = [email for name, email in settings.ADMINS]
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        admin_emails,
        fail_silently=False,
    )


def send_auto_response(submission):
    """Send auto-response email to contact form submitter."""
    subject = f'Thank you for contacting Far Out Corporation'
    message = f"""
Hello {submission.name},

Thank you for reaching out to Far Out Corporation. We have received your message regarding: "{submission.subject}"

Our team will review your message and get back to you as soon as possible, typically within 24-48 hours.

For urgent matters, you can also reach us on Discord: https://discord.gg/farout

Best regards,
Far Out Corporation Team

---
This is an automated response. Please do not reply to this email.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [submission.email],
        fail_silently=False,
    )
