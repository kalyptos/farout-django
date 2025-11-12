"""
Core views for Farout application.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
    from apps.starships.models import Ship
    from apps.organization.models import OrganizationMember

    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]
    featured_ships = Ship.objects.filter(is_flight_ready=True).select_related('manufacturer').order_by('?')[:6]

    # Stats
    total_ships = Ship.objects.count()
    total_members = OrganizationMember.objects.count()
    flight_ready_ships = Ship.objects.filter(is_flight_ready=True).count()

    context = {
        'recent_posts': recent_posts,
        'featured_ships': featured_ships,
        'total_ships': total_ships,
        'total_members': total_members,
        'flight_ready_ships': flight_ready_ships,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """Main dashboard for authenticated users."""
    from apps.starships.models import Ship
    from apps.organization.models import OrganizationMember
    from apps.fleet.models import FleetShip

    # Get organization stats
    total_members = OrganizationMember.objects.count()
    recent_members = OrganizationMember.objects.order_by('-created_at')[:5]
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]

    # Get user-specific data
    user = request.user

    # Try to get organization member data
    try:
        org_member = OrganizationMember.objects.get(handle=user.username)
    except OrganizationMember.DoesNotExist:
        org_member = None

    # Determine user rank (default to Member if not in org)
    rank = org_member.rank if org_member else 'Member'
    rank_slug = rank.lower().replace(' ', '-') if rank else 'member'

    # Determine user role
    if user.is_superuser:
        role = 'CEO'
    elif user.is_staff:
        role = 'Admin'
    else:
        role = 'Member'

    # Get user's fleet ships
    user_ships = FleetShip.objects.filter(owner=user).select_related('ship', 'ship__manufacturer')

    # Count ships by type
    from collections import Counter
    ship_counts = Counter([fleet_ship.ship.name for fleet_ship in user_ships])

    # Get squadron membership
    from apps.squadron.models import SquadronMember
    squadron_membership = SquadronMember.objects.filter(
        user=user,
        is_active=True
    ).select_related('squadron').first()

    squadron = squadron_membership.squadron if squadron_membership else None

    # Get unread messages count (from communications DB)
    from apps.communications.models import InternalMessage
    unread_messages = InternalMessage.objects.filter(
        recipient_id=user.id,
        is_read=False,
        is_deleted_by_recipient=False
    ).count()

    # Dummy data for features not yet implemented
    missions_completed = 0  # Placeholder
    training_completed = 0  # Placeholder

    # Stats for dashboard cards
    total_ships_owned = user_ships.count()
    total_org_ships = Ship.objects.count()

    context = {
        'total_members': total_members,
        'recent_members': recent_members,
        'recent_posts': recent_posts,
        'org_member': org_member,
        'user': user,
        'rank': rank,
        'rank_slug': rank_slug,
        'role': role,
        'user_ships': user_ships,
        'ship_counts': dict(ship_counts),
        'missions_completed': missions_completed,
        'training_completed': training_completed,
        'unread_messages': unread_messages,
        'squadron': squadron,
        'total_ships_owned': total_ships_owned,
        'total_org_ships': total_org_ships,
    }
    return render(request, 'dashboard.html', context)


def about(request):
    """About Us page."""
    from apps.organization.models import Organization, OrganizationMember
    from apps.starships.models import Ship

    # Get organization stats
    try:
        org = Organization.objects.first()
    except Organization.DoesNotExist:
        org = None

    total_members = OrganizationMember.objects.count()
    total_ships = Ship.objects.count()

    context = {
        'organization': org,
        'total_members': total_members,
        'total_ships': total_ships,
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page."""
    from apps.organization.models import Organization

    # Get organization info
    try:
        org = Organization.objects.first()
    except Organization.DoesNotExist:
        org = None

    context = {
        'organization': org,
    }
    return render(request, 'contact.html', context)
