import chess
import chess.svg

from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from chess_engine.models import SelfChessGame, BotChessGame
from users.forms import RegisterForm, ProfileEditForm

from users.models import CustomUser, FriendshipRequest


class CustomRegistrationView(FormView):
    template_name = "users/register.html"

    form_class = RegisterForm
    success_url = reverse_lazy("login")  # login page

    def form_valid(self, form):
        messages.success(self.request, "You have successfully registered!")
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        context = self.get_context_data(form=form)
        context["errors"] = errors

        return self.render_to_response(context)


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")  # home page

    def form_valid(self, form):
        messages.success(self.request, "You have successfully logged in!")
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        context = self.get_context_data(form=form)
        context["errors"] = errors

        return self.render_to_response(context)


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        request.session.flush()

        return redirect("/")


class UserProfileView(View):
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        status = kwargs.get("status")
        games = []

        if request.user.username == username:
            user = request.user
            user_data = {
                "username": user.username,
                "bio": user.bio,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar,
                "date_joined": user.date_joined,
                "location": user.location,
                "birth_date": user.birth_date,
                "country": user.country,
                "total_games": len(games),
                "friends": user.friends.all(),
                "own": True,
                "status": status,
            }

        else:
            user = get_object_or_404(CustomUser, username=username)
            user_data = {
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar,
                "date_joined": user.date_joined,
                "total_games": len(games),
                "friends": user.friends.all(),
            }

        if status == "finished":
            user_self_games = SelfChessGame.objects.filter(
                player=user, is_finished=True
            )
            user_bot_games = BotChessGame.objects.filter(player=user, s_finished=True)
        elif status == "active":
            user_self_games = SelfChessGame.objects.filter(
                player=user, is_finished=False
            )
            user_bot_games = SelfChessGame.objects.filter(
                player=user, is_finished=False
            )
        else:
            user_self_games = SelfChessGame.objects.filter(player=user)
            user_bot_games = BotChessGame.objects.filter(player=user)

        for game in user_self_games:
            board = chess.Board(game.fen)
            svg_board = chess.svg.board(board=board)
            games.append(
                {
                    "id": game.game_id,
                    "svg_board": svg_board,
                    "player": game.player,
                    "is_finished": game.is_finished,
                    "winner": game.winner,
                    "bot": False,
                }
            )

        for game in user_bot_games:
            board = chess.Board(game.fen)
            svg_board = chess.svg.board(board=board)
            games.append(
                {
                    "id": game.game_id,
                    "svg_board": svg_board,
                    "player": game.player,
                    "is_finished": game.is_finished,
                    "winner": game.winner,
                    "bot": True,
                }
            )

        all_friends_request = FriendshipRequest.objects.filter(
            to_user__username=username
        )
        games.reverse()

        return render(
            request,
            self.template_name,
            {
                "user_data": user_data,
                "games": games,
                "all_friends_request": all_friends_request,
            },
        )


class ProfileEditView(LoginRequiredMixin, View):
    template_name = "users/profile_edit.html"

    def get(self, request, *args, **kwargs):
        form = ProfileEditForm(instance=request.user)
        user = request.user
        user_data = {
            "bio": user.bio,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": user.avatar,
            "location": user.location,
            "birth_date": user.birth_date,
            "country": user.country,
        }
        return render(
            request, self.template_name, {"user_data": user_data, "form": form}
        )

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated!")

        return redirect("edit_profile")


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id: int):
        friend_request = get_object_or_404(FriendshipRequest, id=request_id)

        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()

            messages.success(request, "Friend request accepted")
        else:
            messages.error(request, "friend request not accepted")

        return redirect(
            request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
        )


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        from_user = request.user
        to_user = get_object_or_404(CustomUser, username=username)

        friend_request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
        )

        if created:
            messages.success(request, "Friend request sent")
        else:
            messages.error(request, "Friend request was already sent")

        return redirect(
            request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
        )


class SearchUsersView(View):
    template_name = "users/users_search.html"

    def get(self, request):
        query = request.GET.get("q", "")
        results = []

        if query:
            results = CustomUser.objects.filter(username__icontains=query)

        context = {
            "query": query,
            "results": results,
        }

        return render(request, self.template_name, context)
