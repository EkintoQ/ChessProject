from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from users.forms import RegisterForm, AvatarForm
from users.models import CustomUser


class CustomRegistrationView(FormView):
    template_name = "users/register.html"

    form_class = RegisterForm
    success_url = reverse_lazy("start")  # login page

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
        return reverse_lazy("start")  # login page

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
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar,
                "own": True,
            }
        else:
            user = get_object_or_404(CustomUser, username=username)
            user_data = {
                "username": user.username,
                "email": user.email,
                "avatar": user.avatar,
            }

        form = AvatarForm(instance=user)
        return render(
            request, self.template_name, {"user_data": user_data, "form": form}
        )

    @classmethod
    def post(cls, request, *args, **kwargs):
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

        return redirect("profile", username=request.user.username)
