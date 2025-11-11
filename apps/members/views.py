"""
Member views for listing and viewing member profiles.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Member, ShipOwnership


@login_required
def member_list(request):
    """List all organization members."""
    # Get all members ordered by rank and name
    members_list = Member.objects.all().order_by('rank', 'display_name')

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        members_list = members_list.filter(display_name__icontains=search_query)

    # Filter by rank
    rank_filter = request.GET.get('rank', '')
    if rank_filter:
        members_list = members_list.filter(rank=rank_filter)

    # Pagination
    paginator = Paginator(members_list, 24)  # 24 members per page
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)

    context = {
        'members': members,
        'rank_choices': Member.RANK_CHOICES,
        'search_query': search_query,
        'rank_filter': rank_filter,
    }
    return render(request, 'members/member_list.html', context)


@login_required
def member_detail(request, member_id):
    """View detailed member profile."""
    member = get_object_or_404(Member, pk=member_id)

    # Get member's ships
    ship_ownerships = ShipOwnership.objects.filter(member=member).select_related('ship', 'ship__manufacturer')

    context = {
        'member': member,
        'ship_ownerships': ship_ownerships,
    }
    return render(request, 'members/member_detail.html', context)
