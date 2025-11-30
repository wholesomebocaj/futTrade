from django.db import connection
from django.db.models import Prefetch, Q
from django.views.generic import ListView
from rest_framework import viewsets

from .models import Player, PriceSnapshot
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerSerializer
    search_fields = ['name', 'club', 'nation', 'card_type']
    ordering_fields = ['name', 'rating']
    ordering = ['name']

    def get_queryset(self):
        price_queryset = PriceSnapshot.objects.order_by('platform', '-timestamp')
        if getattr(connection.features, 'supports_distinct_on_fields', False):
            price_queryset = price_queryset.distinct('platform')

        return (
            Player.objects.all()
            .prefetch_related(Prefetch('price_snapshots', queryset=price_queryset))
            .order_by('name')
        )


class PlayerSearchView(ListView):
    template_name = 'codex/player_search.html'
    model = Player
    context_object_name = 'players'

    def get_queryset(self):
        price_queryset = PriceSnapshot.objects.order_by('platform', '-timestamp')
        if getattr(connection.features, 'supports_distinct_on_fields', False):
            price_queryset = price_queryset.distinct('platform')

        queryset = (
            Player.objects.all()
            .prefetch_related(Prefetch('price_snapshots', queryset=price_queryset))
            .order_by('name')
        )

        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(club__icontains=query)
                | Q(nation__icontains=query)
                | Q(card_type__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context
