import chess

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import User


class ChessGame(models.Model):
    fen = models.CharField(max_length=255)
    game_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_new_game(cls):
        new_game = cls(fen=chess.STARTING_FEN)
        new_game.save()
        return new_game


class Move(models.Model):
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE)
    move_text = models.CharField(max_length=10)
