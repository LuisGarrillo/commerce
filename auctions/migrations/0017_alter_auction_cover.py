# Generated by Django 5.0.3 on 2024-04-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0016_alter_auction_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="cover",
            field=models.ImageField(upload_to="covers/"),
        ),
    ]
