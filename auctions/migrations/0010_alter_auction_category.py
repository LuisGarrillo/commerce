# Generated by Django 5.0.3 on 2024-04-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0009_auction_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="category",
            field=models.CharField(max_length=64),
        ),
    ]