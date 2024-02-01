from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "avatar",
            "bio",
            "first_name",
            "last_name",
            "location",
            "birth_date",
            "country",
        ]
