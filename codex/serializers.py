from rest_framework import serializers

from .models import Player, PriceSnapshot


class PriceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSnapshot
        fields = ['platform', 'min_price', 'max_price', 'average_price', 'timestamp']


class PlayerSerializer(serializers.ModelSerializer):
    latest_prices = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            'id',
            'name',
            'rating',
            'club',
            'nation',
            'league',
            'position',
            'card_type',
            'external_id',
            'latest_prices',
        ]

    def get_latest_prices(self, obj):
        snapshots = obj.latest_prices_by_platform()
        snapshots = sorted(snapshots, key=lambda snapshot: snapshot.timestamp, reverse=True)
        return PriceSnapshotSerializer(snapshots, many=True).data
