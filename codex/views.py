from django.db.models import Prefetch
from django.db import connection
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
        if connection.features.supports_distinct_on_fields:
            price_queryset = price_queryset.distinct('platform')

        return (
            Player.objects.all()
            .prefetch_related(Prefetch('price_snapshots', queryset=price_queryset))
            .order_by('name')
        )
