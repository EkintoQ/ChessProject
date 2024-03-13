from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SelfChessGame
import chess
import chess.svg


class HomeView(View):
    @classmethod
    def get(cls, request, *args, **kwargs):
        return render(request, "chess_engine/home.html")


class CreateNewSelfGameView(View):
    @classmethod
    def post(cls, request):
        new_game = SelfChessGame.create_new_game(player=request.user)
        return redirect("display_self_game_board", game_id=new_game.game_id)


class DisplayBoardSelfGameView(View):
    @classmethod
    def get(cls, request, game_id):
        game = get_object_or_404(SelfChessGame, game_id=game_id)
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        return render(
            request,
            "chess_engine/display_board.html",
            {
                "svg_board": svg_board,
                "game_id": game_id,
                "game": game,
                "player": game.player,
                "fen": game.fen,
            },
        )


class MakeMoveViewAPI(APIView):
    def post(self, request, game_id):
        move_text = request.data.get("move")
        game = get_object_or_404(SelfChessGame, game_id=game_id)
        board = chess.Board(game.fen)

        try:
            move = chess.Move.from_uci(move_text)
        except chess.InvalidMoveError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if move in board.legal_moves:
            board.push(move)
            game.fen = board.fen()
            game.moves.append(move_text)

            game.is_finished = board.is_checkmate()
            outcome = board.result()
            if outcome == "1/2-1/2":
                game.winner = "Draw"
            elif outcome == "1-0":
                game.winner = "White"
            else:
                game.winner = "Black"

            game.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
