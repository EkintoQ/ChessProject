from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.forms import RegisterForm


def registration_view(request):  # CBV
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("")  # Redirect to your home or login page
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})
