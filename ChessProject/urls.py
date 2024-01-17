from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_engine.views import display_board, create_new_game, start, make_move
from users.views import RegistrationView, CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", start, name="start"),
    path("board/<int:game_id>/", display_board, name="display_board"),
    path("board/<int:game_id>/make_move/", make_move, name="make_move"),
    path("new_game/", create_new_game, name="create_new_game"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
