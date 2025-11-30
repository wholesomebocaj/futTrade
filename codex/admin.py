from django.contrib import admin

from .models import Player, PriceSnapshot


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'club', 'nation', 'league', 'card_type', 'rating')
    search_fields = ('name', 'club', 'nation', 'league', 'position', 'card_type')


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('player', 'platform', 'average_price', 'min_price', 'max_price', 'timestamp')
    list_filter = ('platform',)
    search_fields = ('player__name',)
    ordering = ('-timestamp',)
