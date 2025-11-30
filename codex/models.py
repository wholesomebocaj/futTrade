from django.db import connection, models
from django.utils import timezone


class Player(models.Model):
    CARD_TYPE_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('special', 'Special'),
    ]

    name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField()
    club = models.CharField(max_length=255)
    nation = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    position = models.CharField(max_length=50)
    card_type = models.CharField(max_length=50, choices=CARD_TYPE_CHOICES)
    external_id = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.position})"

    def latest_prices_by_platform(self):
        snapshots = self.price_snapshots.order_by('platform', '-timestamp')
        if getattr(connection.features, 'supports_distinct_on_fields', False):
            snapshots = snapshots.distinct('platform')
        return list(snapshots)


class PriceSnapshot(models.Model):
    PLATFORM_PC = 'pc'
    PLATFORM_PS = 'ps'
    PLATFORM_XBOX = 'xbox'
    PLATFORM_CHOICES = [
        (PLATFORM_PC, 'PC'),
        (PLATFORM_PS, 'PlayStation'),
        (PLATFORM_XBOX, 'Xbox'),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='price_snapshots')
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    min_price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    average_price = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['player', 'platform', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.player.name} - {self.platform} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
