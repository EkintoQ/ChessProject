import chess
from django.db import models


class ChessGame(models.Model):
    fen = models.CharField(max_length=255)
    game_id = models.AutoField(primary_key=True)

    @classmethod
    def create_new_game(cls):
        new_game = cls(fen=chess.STARTING_FEN)
        new_game.save()
        return new_game


class Move(models.Model):
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE)
    move_text = models.CharField(max_length=10)

