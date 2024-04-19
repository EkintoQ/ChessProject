from django.contrib import admin

from chess_engine.models import BotChessGame, SelfChessGame

admin.site.register(BotChessGame)
admin.site.register(SelfChessGame)
