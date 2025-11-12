"""Forms for communications app."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactSubmission, InternalMessage


class ContactForm(forms.ModelForm):
    """Contact form for public submissions."""

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 6,
            }),
        }

    def clean_message(self):
        """Validate message length."""
        message = self.cleaned_data.get('message', '')
        if len(message) < 10:
            raise forms.ValidationError(_('Message must be at least 10 characters long.'))
        return message


class InternalMessageForm(forms.ModelForm):
    """Form for sending internal messages between members."""

    class Meta:
        model = InternalMessage
        fields = ['recipient_id', 'subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message...',
                'rows': 8,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.sender_user = kwargs.pop('sender_user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save message with sender information."""
        instance = super().save(commit=False)
        if self.sender_user:
            instance.sender_id = self.sender_user.id
            instance.sender_name = self.sender_user.username
        if commit:
            instance.save()
        return instance
