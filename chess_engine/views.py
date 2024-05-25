from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SelfChessGame, BotChessGame, MultiplayerChessGame
import chess
import chess.svg
import chess.engine


class CreateNewSelfGameView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        new_game = SelfChessGame.create_new_game(player=request.user)
        return redirect("display_self_game_board", game_id=new_game.game_id)


class DisplayBoardSelfGameView(TemplateView):
    template_name = "chess_engine/display_board.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        game_id = kwargs.get("game_id")
        game = get_object_or_404(SelfChessGame, game_id=game_id)
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        context = super().get_context_data(**kwargs)
        context["svg_board"] = svg_board
        context["game_id"] = game_id
        context["game"] = game
        context["player"] = game.player
        context["fen"] = game.fen
        return context


class MakeMoveSelfViewAPI(APIView):
    def post(self, request, game_id):
        fen = request.data.get("fen")
        move = request.data.get("move")

        game = get_object_or_404(SelfChessGame, game_id=game_id)

        board = chess.Board(fen)
        game.moves.append(move)
        game.fen = board.fen()

        if board.outcome():
            game.is_finished = True
            if board.result() == "0-1":
                game.winner = "black"
            elif board.result() == "1-0":
                game.winner = "white"
            else:
                game.winner = "draw"
        game.save()
        return Response(status=status.HTTP_200_OK)


class CreateNewBotGameView(View):
    @classmethod
    def post(cls, request):
        new_game = BotChessGame.create_new_game(player=request.user)
        return redirect("display_bot_game_board", game_id=new_game.game_id)


class DisplayBoardBotGameView(View):
    @classmethod
    def get(cls, request, game_id):
        game = get_object_or_404(BotChessGame, game_id=game_id)
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        return render(
            request,
            "chess_engine/display_board_bot.html",
            {
                "svg_board": svg_board,
                "game_id": game_id,
                "game": game,
                "player": game.player,
                "fen": game.fen,
            },
        )


class MakeMoveBotViewAPI(APIView):
    def post(self, request, game_id):
        fen = request.data.get("fen")
        move = request.data.get("move")

        game = get_object_or_404(BotChessGame, game_id=game_id)

        board = chess.Board(fen)

        if board.outcome():
            game.is_finished = True
            if board.result() == "0-1":
                game.winner = "black"
            elif board.result() == "1-0":
                game.winner = "white"
            else:
                game.winner = "draw"
        else:
            engine = chess.engine.SimpleEngine.popen_uci(
                "chess_engine/bbc_1.4_sf_nnue_final_64bit_windows.exe"
            )
            result = engine.play(board, chess.engine.Limit(time=1))
            board.push(result.move)
        fen = board.fen()
        game.fen = fen
        game.moves.append(move)

        game.save()
        return Response({"fen": fen, "moves": game.moves}, status=status.HTTP_200_OK)


class CreateNewMultiplayerGameView(View):
    @classmethod
    def post(cls, request):
        players = request.data.get("players")
        new_game = MultiplayerChessGame.create_new_game(players)
        return redirect("display_multiplayer_game_board", game_id=new_game.game_id)


class DisplayBoardMultiplayerGameView(View):
    @classmethod
    def get(cls, request, game_id):
        game = get_object_or_404(MultiplayerChessGame, game_id=game_id)
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        return render(
            request,
            "chess_engine/display_board_multiplayer.html",
            {
                "svg_board": svg_board,
                "game_id": game_id,
                "game": game,
                "players": game.players.all(),
                "current_turn": game.current_turn,
                "fen": game.fen,
            },
        )
