from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_engine.views import display_board, create_new_game, start, make_move

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", start, name="start"),
    path("board/<int:game_id>/", display_board, name="display_board"),
    path("board/<int:game_id>/make_move/", make_move, name="make_move"),
    path("new_game/", create_new_game, name="create_new_game"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
