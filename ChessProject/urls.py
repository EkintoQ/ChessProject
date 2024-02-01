from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_engine.views import (
    HomeView,
    DisplayBoardSelfGameView,
    MakeMoveSelfGameView,
    CreateNewSelfGameView,
)
from users.views import (
    CustomRegistrationView,
    CustomLoginView,
    CustomLogoutView,
    UserProfileView,
    ProfileEditView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("newselfgame/", CreateNewSelfGameView.as_view(), name="create_new_self_game"),
    path(
        "board/self/<int:game_id>/",
        DisplayBoardSelfGameView.as_view(),
        name="display_self_game_board",
    ),
    path(
        "board/self/<int:game_id>/make_move/",
        MakeMoveSelfGameView.as_view(),
        name="make_self_game_move",
    ),
    path("register/", CustomRegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/<str:username>/", UserProfileView.as_view(), name="profile"),
    path("edit_profile", ProfileEditView.as_view(), name="edit_profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
