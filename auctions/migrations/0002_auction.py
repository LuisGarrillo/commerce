# Generated by Django 5.0.3 on 2024-04-07 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=500)),
                ("cover", models.ImageField(upload_to="")),
                ("initial_bid", models.DecimalField(decimal_places=2, max_digits=11)),
                ("status", models.IntegerField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="won_auctions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
