from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

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
        player = game.player
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        return render(
            request,
            "chess_engine/display_board.html",
            {
                "svg_board": svg_board,
                "game_id": game_id,
                "game": game,
                "player": player,
            },
        )


class MakeMoveSelfGameView(View):
    @classmethod
    def post(cls, request, game_id):
        move_text = request.POST.get("move_text")
        if move_text:
            game = get_object_or_404(SelfChessGame, game_id=game_id)
            board = chess.Board(game.fen)

            try:
                move = chess.Move.from_uci(move_text)
            except chess.InvalidMoveError as e:
                messages.error(request, "Invalid request. Please provide a move.")
                return redirect("display_self_game_board", game_id=game_id)

            if move in board.legal_moves:
                board.push(move)
                game.fen = board.fen()
                game.moves.append(move_text)

                game.save()
                return redirect("display_self_game_board", game_id=game_id)
            else:
                messages.error(request, "Invalid move. Please try again.")

        else:
            messages.error(request, "Invalid request. Please provide a move.")

        return redirect("display_self_game_board", game_id=game_id)
