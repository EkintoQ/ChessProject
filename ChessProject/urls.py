from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_engine.views import (
    DisplayBoardSelfGameView,
    CreateNewSelfGameView,
    CreateNewBotGameView,
    DisplayBoardBotGameView,
    MakeMoveSelfViewAPI,
    MakeMoveBotViewAPI,
    CreateNewMultiplayerGameView,
)
from news.views import HomeView, NewsView
from users.views import (
    CustomRegistrationView,
    CustomLoginView,
    CustomLogoutView,
    UserProfileView,
    ProfileEditView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    SearchUsersView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("news/", NewsView.as_view(), name="news"),
    path("newselfgame/", CreateNewSelfGameView.as_view(), name="create_new_self_game"),
    path("newbotgame/", CreateNewBotGameView.as_view(), name="create_new_bot_game"),
    path(
        "newmultiplayergame",
        CreateNewMultiplayerGameView.as_view(),
        name="create_new_multiplayer_game",
    ),
    path(
        "board/self/<int:game_id>/",
        DisplayBoardSelfGameView.as_view(),
        name="display_self_game_board",
    ),
    path(
        "board/bot/<int:game_id>/",
        DisplayBoardBotGameView.as_view(),
        name="display_bot_game_board",
    ),
    path("board/self/<int:game_id>/make_move_api/", MakeMoveSelfViewAPI.as_view()),
    path("board/bot/<int:game_id>/make_move_api/", MakeMoveBotViewAPI.as_view()),
    path("register/", CustomRegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/<str:username>/", UserProfileView.as_view(), name="profile"),
    path(
        "users/<str:username>/<str:status>/",
        UserProfileView.as_view(),
        name="profile_games_status",
    ),
    path("edit_profile", ProfileEditView.as_view(), name="edit_profile"),
    path(
        "send_friend_request/<str:username>",
        SendFriendRequestView.as_view(),
        name="send_friend_request",
    ),
    path(
        "accept_friend_request/<int:request_id>",
        AcceptFriendRequestView.as_view(),
        name="accept_friend_request",
    ),
    path("search/users", SearchUsersView.as_view(), name="users_search"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
