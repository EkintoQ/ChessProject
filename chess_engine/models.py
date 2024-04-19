import chess

from django.db import models

from users.models import CustomUser


class BaseChessGame(models.Model):
    fen = models.CharField(max_length=255)
    game_id = models.AutoField(primary_key=True)
    moves = models.JSONField(default=list)
    is_finished = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BotChessGame(BaseChessGame):
    player = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="Customer account who played this game.",
        null=True,
        blank=True,
    )

    winner = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        help_text="Winner of the game (Bot or Player).",
    )

    @classmethod
    def create_new_game(cls, player):
        new_game = cls(fen=chess.STARTING_FEN, player=player)
        new_game.save()
        return new_game


class SelfChessGame(BaseChessGame):
    player = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="Customer account who played this game.",
    )

    winner = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        help_text="Winner of the game (White or Black or Draw).",
    )

    @classmethod
    def create_new_game(cls, player):
        new_game = cls(fen=chess.STARTING_FEN, player=player)
        new_game.save()
        return new_game


class MultiplayerChessGame(BaseChessGame):
    @classmethod
    def create_new_game(cls, player):
        new_game = cls(fen=chess.STARTING_FEN, player=player)
        new_game.save()
        return new_game
