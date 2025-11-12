"""
Views for organization app.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models
from .models import OrganizationMember


class MemberListView(ListView):
    """Display list of organization members."""
    model = OrganizationMember
    template_name = 'organization/member_list.html'
    context_object_name = 'members'
    paginate_by = 12

    def get_queryset(self):
        """Filter members based on search query."""
        queryset = OrganizationMember.objects.all()

        # Search by handle or display name
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                models.Q(handle__icontains=search_query) |
                models.Q(display_name__icontains=search_query)
            )

        # Filter by rank
        rank = self.request.GET.get('rank', '')
        if rank:
            queryset = queryset.filter(rank__icontains=rank)

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context."""
        context = super().get_context_data(**kwargs)

        # Get unique ranks for filter dropdown
        context['ranks'] = OrganizationMember.objects.values_list('rank', flat=True).distinct().order_by('rank')

        return context


class MemberDetailView(DetailView):
    """Display detailed view of a member."""
    model = OrganizationMember
    template_name = 'organization/member_detail.html'
    context_object_name = 'member'
    slug_field = 'handle'
    slug_url_kwarg = 'handle'

    def get_context_data(self, **kwargs):
        """Add additional context."""
        context = super().get_context_data(**kwargs)

        # Get member's ships if FleetShip model exists
        try:
            from apps.fleet.models import FleetShip
            from django.contrib.auth import get_user_model
            User = get_user_model()

            # Try to find user by handle
            try:
                user = User.objects.get(username=self.object.handle)
                context['user_ships'] = FleetShip.objects.filter(owner=user).select_related('ship', 'ship__manufacturer')
            except User.DoesNotExist:
                context['user_ships'] = []
        except ImportError:
            context['user_ships'] = []

        return context
