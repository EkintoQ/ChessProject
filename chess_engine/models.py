import chess

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import CustomUser


class BaseChessGame(models.Model):
    fen = models.CharField(max_length=255)
    game_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="Customer account who played this game.",
    )

    class Meta:
        abstract = True


class BotChessGame(BaseChessGame):
    @classmethod
    def create_new_game(cls, player):
        new_game = cls(fen=chess.STARTING_FEN, player=player)
        new_game.save()
        return new_game


class SelfChessGame(BaseChessGame):
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


class Move(models.Model):
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # game = GenericForeignKey('content_type', 'object_id')
    move_text = models.CharField(max_length=10)
