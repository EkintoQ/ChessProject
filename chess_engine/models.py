from typing import Optional

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
    player: CustomUser
    winner: Optional[str]

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

    def create_new_game(self, player: CustomUser) -> "BotChessGame":
        new_game = BotChessGame(fen=chess.STARTING_FEN, player=player)
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
    players = models.ManyToManyField(
        CustomUser,
        related_name="multiplayer_games",
        help_text="Players participating in this game.",
    )
    current_turn = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="current_turn_games",
        null=True,
        blank=True,
        help_text="Player whose turn it is.",
    )

    @classmethod
    def create_new_game(cls, players):
        new_game = cls(fen=chess.STARTING_FEN)
        new_game.players.set(players)
        new_game.current_turn = players[0]
        new_game.save()
        return new_game

    def switch_turn(self):
        if self.current_turn == self.players[0]:
            self.current_turn = self.players[1]
        else:
            self.current_turn = self.players[0]
        self.save()
