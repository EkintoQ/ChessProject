from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import ChessGame, Move
import chess
import chess.svg


def start(request):
    return render(request, 'chess_engine/start.html')


def display_board(request, game_id):
    game = get_object_or_404(ChessGame, game_id=game_id)
    board = chess.Board(game.fen)
    svg_board = chess.svg.board(board=board)
    return render(request, 'chess_engine/display_board.html', {'svg_board': svg_board, 'game_id': game_id})


def create_new_game(request):
    new_game = ChessGame.create_new_game()
    return redirect('display_board', game_id=new_game.game_id)


def make_move(request, game_id):
    if request.method == 'POST':
        move_text = request.POST.get('move_text')
        if move_text:
            game = get_object_or_404(ChessGame, game_id=game_id)
            board = chess.Board(game.fen)

            move = chess.Move.from_uci(move_text)
            if move in board.legal_moves:
                board.push(move)
                game.fen = board.fen()
                game.save()
                Move.objects.create(game=game, move_text=move_text)
                return redirect('display_board', game_id=game_id)

    return JsonResponse({'error': 'Invalid move or request.'}, status=400)
