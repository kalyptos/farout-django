"""
Core views for Farout application.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.members.models import Member
from apps.blog.models import BlogPost


def health_check(request):
    """Health check endpoint for Docker and monitoring."""
    return JsonResponse({
        'status': 'ok',
        'service': 'farout-django',
        'version': '1.0.0'
    })


def home(request):
    """Home/landing page."""
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]

    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """Main dashboard for authenticated users."""
    from apps.members.models import ShipOwnership
    from django.db.models import Sum, Count

    # Get organization stats
    total_members = Member.objects.count()
    recent_members = Member.objects.order_by('-created_at')[:5]
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:5]

    # Get user-specific data
    user = request.user
    try:
        member = Member.objects.get(discord_id=user.discord_id)

        # Get member's ships with aggregation
        ship_ownerships = ShipOwnership.objects.filter(member=member).select_related('ship', 'ship__manufacturer')

        # Calculate ship statistics
        total_ships = ship_ownerships.aggregate(total=Sum('quantity'))['total'] or 0
        unique_ships = ship_ownerships.count()

        # Get dummy data for unimplemented features
        unread_messages = 3  # Dummy data

    except Member.DoesNotExist:
        member = None
        ship_ownerships = []
        total_ships = 0
        unique_ships = 0
        unread_messages = 0

    context = {
        'total_members': total_members,
        'recent_members': recent_members,
        'recent_posts': recent_posts,
        'member': member,
        'user': user,
        'ship_ownerships': ship_ownerships,
        'total_ships': total_ships,
        'unique_ships': unique_ships,
        'unread_messages': unread_messages,
    }
    return render(request, 'dashboard.html', context)


def about(request):
    """About us page."""
    context = {
        'total_members': Member.objects.count(),
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page."""
    if request.method == 'POST':
        # Process contact form (to be implemented with email system)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # For now, just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')

    return render(request, 'contact.html')
