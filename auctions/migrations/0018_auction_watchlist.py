# Generated by Django 5.0.3 on 2024-04-14 16:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0017_alter_auction_cover"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watched_listings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
