"""Views for squadron app."""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Squadron, SquadronMember


def squadron_list(request):
    """Display list of all active squadrons."""
    squadrons = Squadron.objects.filter(is_active=True).select_related('commander')

    # Annotate with member counts
    for squadron in squadrons:
        squadron.current_members = squadron.get_member_count()

    return render(request, 'squadron/squadron_list.html', {
        'squadrons': squadrons,
    })


def squadron_detail(request, slug):
    """Display squadron details and members."""
    squadron = get_object_or_404(
        Squadron.objects.select_related('commander'),
        slug=slug,
        is_active=True
    )

    members = SquadronMember.objects.filter(
        squadron=squadron,
        is_active=True
    ).select_related('user').order_by('role', 'joined_at')

    return render(request, 'squadron/squadron_detail.html', {
        'squadron': squadron,
        'members': members,
        'member_count': squadron.get_member_count(),
        'can_join': squadron.can_accept_members(),
    })


@login_required
def my_squadron(request):
    """Display user's current squadron."""
    membership = SquadronMember.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('squadron', 'squadron__commander').first()

    if not membership:
        # User not in a squadron, show available squadrons
        available_squadrons = Squadron.objects.filter(
            is_active=True,
            is_recruiting=True
        ).select_related('commander')

        return render(request, 'squadron/no_squadron.html', {
            'available_squadrons': available_squadrons,
        })

    # Get squadron mates
    squadron_mates = SquadronMember.objects.filter(
        squadron=membership.squadron,
        is_active=True
    ).exclude(user=request.user).select_related('user')[:20]

    return render(request, 'squadron/my_squadron.html', {
        'membership': membership,
        'squadron': membership.squadron,
        'squadron_mates': squadron_mates,
    })
