from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_engine.views import (
    HomeView,
    DisplayBoardView,
    MakeMoveView,
    CreateNewGameView,
)
from users.views import (
    CustomRegistrationView,
    CustomLoginView,
    CustomLogoutView,
    UserProfileView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("board/<int:game_id>/", DisplayBoardView.as_view(), name="display_board"),
    path("board/<int:game_id>/make_move/", MakeMoveView.as_view(), name="make_move"),
    path("new_game/", CreateNewGameView.as_view(), name="create_new_game"),
    path("register/", CustomRegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/<str:username>/", UserProfileView.as_view(), name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
