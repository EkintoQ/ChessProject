# Generated by Django 5.0 on 2024-01-31 18:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BotChessGame",
            fields=[
                ("fen", models.CharField(max_length=255)),
                ("game_id", models.AutoField(primary_key=True, serialize=False)),
                ("moves", models.JSONField(default=list)),
                (
                    "player",
                    models.ForeignKey(
                        help_text="Customer account who played this game.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Move",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField(null=True)),
                ("move_text", models.CharField(max_length=10)),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MultiplayerChessGame",
            fields=[
                ("fen", models.CharField(max_length=255)),
                ("game_id", models.AutoField(primary_key=True, serialize=False)),
                ("moves", models.JSONField(default=list)),
                (
                    "player",
                    models.ForeignKey(
                        help_text="Customer account who played this game.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SelfChessGame",
            fields=[
                ("fen", models.CharField(max_length=255)),
                ("game_id", models.AutoField(primary_key=True, serialize=False)),
                ("moves", models.JSONField(default=list)),
                (
                    "player",
                    models.ForeignKey(
                        help_text="Customer account who played this game.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
