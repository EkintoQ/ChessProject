# Generated by Django 5.0.2 on 2024-04-13 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_article_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
