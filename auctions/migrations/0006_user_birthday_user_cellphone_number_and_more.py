# Generated by Django 5.0.3 on 2024-04-09 14:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_alter_auction_cover"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="user",
            name="cellphone_number",
            field=models.CharField(default="04246246432", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="email_address",
            field=models.CharField(default="luis@gmail.com", max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(default="Luis Garrillo", max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(default="Non-Binary", max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="auction",
            name="cover",
            field=models.ImageField(upload_to="uploads/auctions"),
        ),
        migrations.CreateModel(
            name="Bid",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=11)),
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bid_list",
                        to="auctions.auction",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="comments",
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
                ("body", models.CharField(max_length=500)),
                ("image", models.ImageField(upload_to="uploads/auctions")),
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_list",
                        to="auctions.auction",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="liked_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
