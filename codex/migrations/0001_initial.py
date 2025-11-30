from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rating', models.PositiveIntegerField()),
                ('club', models.CharField(max_length=255)),
                ('nation', models.CharField(max_length=255)),
                ('league', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=50)),
                ('card_type', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze'), ('special', 'Special')], max_length=50)),
                ('external_id', models.CharField(max_length=100, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='PriceSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('pc', 'PC'), ('ps', 'PlayStation'), ('xbox', 'Xbox')], max_length=10)),
                ('min_price', models.PositiveIntegerField()),
                ('max_price', models.PositiveIntegerField()),
                ('average_price', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_snapshots', to='codex.player')),
            ],
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddIndex(
            model_name='pricesnapshot',
            index=models.Index(fields=['player', 'platform', '-timestamp'], name='codex_price_player__2b074d_idx'),
        ),
    ]
