from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Move, SelfChessGame
import chess
import chess.svg


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "chess_engine/home.html")


class CreateNewGameView(View):
    def post(self, request):
        new_game = SelfChessGame.create_new_game(player=request.user)
        return redirect("display_board", game_id=new_game.game_id)


class DisplayBoardView(View):
    def get(self, request, game_id):
        game = get_object_or_404(SelfChessGame, game_id=game_id)
        board = chess.Board(game.fen)
        svg_board = chess.svg.board(board=board)
        return render(
            request,
            "chess_engine/display_board.html",
            {"svg_board": svg_board, "game_id": game_id},
        )


class MakeMoveView(View):
    def post(self, request, game_id):
        move_text = request.POST.get("move_text")
        if move_text:
            game = get_object_or_404(SelfChessGame, game_id=game_id)
            board = chess.Board(game.fen)

            move = chess.Move.from_uci(move_text)
            if move in board.legal_moves:
                board.push(move)
                game.fen = board.fen()
                game.save()
                Move.objects.create(game=game, move_text=move_text)
                return redirect("display_board", game_id=game_id)

        return JsonResponse({"error": "Invalid move or request."}, status=400)
