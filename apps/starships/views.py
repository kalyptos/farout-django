"""Starships views."""
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Ship, Manufacturer


class ShipListView(ListView):
    """Ship catalog with search and filters."""
    model = Ship
    template_name = 'starships/ship_list.html'
    context_object_name = 'ships'
    paginate_by = 50

    def get_queryset(self):
        queryset = Ship.objects.select_related('manufacturer').all()

        # Search
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(manufacturer__name__icontains=search) |
                Q(type__icontains=search)
            )

        # Filters
        manufacturer = self.request.GET.get('manufacturer')
        if manufacturer:
            queryset = queryset.filter(manufacturer__code=manufacturer)

        ship_type = self.request.GET.get('type')
        if ship_type:
            queryset = queryset.filter(type=ship_type)

        size = self.request.GET.get('size')
        if size:
            queryset = queryset.filter(size=size)

        status = self.request.GET.get('status')
        if status == 'flight_ready':
            queryset = queryset.filter(is_flight_ready=True)
        elif status == 'concept':
            queryset = queryset.filter(is_concept=True)

        return queryset.order_by('manufacturer__name', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturers'] = Manufacturer.objects.all()
        context['ship_types'] = Ship.objects.values_list('type', flat=True).distinct()
        context['ship_sizes'] = Ship.objects.values_list('size', flat=True).distinct()
        return context


class ShipDetailView(DetailView):
    """Ship detail page."""
    model = Ship
    template_name = 'starships/ship_detail.html'
    context_object_name = 'ship'

    def get_queryset(self):
        return Ship.objects.select_related('manufacturer').prefetch_related('components')
