"""Forms for accounts app."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User


class ProfilePictureUploadForm(forms.ModelForm):
    """Form for uploading profile picture."""

    class Meta:
        model = User
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }
        help_texts = {
            'profile_picture': _('Upload a profile picture (JPG, PNG, GIF). Max size: 5MB.')
        }

    def clean_profile_picture(self):
        """Validate uploaded image."""
        picture = self.cleaned_data.get('profile_picture')

        if picture:
            # Check file size (5MB limit)
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_('Image file too large (max 5MB).'))

            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(picture, 'content_type') and picture.content_type not in allowed_types:
                raise forms.ValidationError(_('Unsupported file type. Please upload JPG, PNG, GIF, or WebP.'))

        return picture
