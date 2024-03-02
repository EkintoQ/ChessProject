# Generated by Django 5.0.2 on 2024-03-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chess_engine", "0002_delete_move"),
    ]

    operations = [
        migrations.AddField(
            model_name="botchessgame",
            name="is_finished",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="multiplayerchessgame",
            name="is_finished",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="selfchessgame",
            name="is_finished",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="selfchessgame",
            name="winner",
            field=models.CharField(
                blank=True,
                choices=[("white", "White"), ("black", "Black"), ("draw", "Draw")],
                help_text="Winner of the game (White or Black or Draw).",
                max_length=5,
                null=True,
            ),
        ),
    ]