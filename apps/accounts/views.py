"""Views for accounts app."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import ProfilePictureUploadForm


@login_required
def upload_profile_picture(request):
    """Upload or update profile picture."""
    if request.method == 'POST':
        form = ProfilePictureUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile picture updated successfully!'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = ProfilePictureUploadForm(instance=request.user)

    return render(request, 'accounts/upload_profile_picture.html', {
        'form': form,
    })


@login_required
def remove_profile_picture(request):
    """Remove uploaded profile picture."""
    if request.method == 'POST':
        if request.user.profile_picture:
            request.user.profile_picture.delete()
            request.user.save(update_fields=['profile_picture'])
            messages.success(request, _('Profile picture removed.'))
        return redirect('dashboard')

    return render(request, 'accounts/confirm_remove_picture.html')
