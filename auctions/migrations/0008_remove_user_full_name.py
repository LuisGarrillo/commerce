# Generated by Django 5.0.3 on 2024-04-09 14:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_rename_comments_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="full_name",
        ),
    ]
