from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-posta")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {"username": "Kullanıcı adı"}

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten kullanılıyor.")
        return username

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"]).lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return email


class TurkishAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı adı")
    password = forms.CharField(label="Parola", strip=False, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Kullanıcı adı veya parola hatalı.",
        "inactive": "Bu hesap etkin değil.",
    }
