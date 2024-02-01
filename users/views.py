from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


from chess_engine.models import SelfChessGame
from users.forms import RegisterForm, ProfileEditForm

from users.models import CustomUser


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
                "total_games": user.total_games,
                "own": True,
            }
        else:
            user = get_object_or_404(CustomUser, username=username)
            user_data = {
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar,
                "date_joined": user.date_joined,
                "total_games": user.total_games,
            }
        user_self_games = SelfChessGame.objects.filter(player=user)

        return render(
            request,
            self.template_name,
            {"user_data": user_data, "user_self_games": user_self_games},
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
