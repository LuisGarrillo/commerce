# Generated by Django 5.0.3 on 2024-04-07 16:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_auction_winner"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
