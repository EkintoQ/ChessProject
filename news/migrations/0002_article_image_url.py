# Generated by Django 5.0.2 on 2024-04-13 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
