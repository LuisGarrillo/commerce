# Generated by Django 5.0.3 on 2024-04-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0015_alter_auction_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="cover",
            field=models.ImageField(upload_to="media/"),
        ),
    ]
