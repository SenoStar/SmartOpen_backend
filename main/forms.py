from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .constants import VOLUME_CHOICES
from .models import User, Cooperation

class CooperationForm(forms.ModelForm):
    """Форма для Сотрудничество."""

    class Meta:
        model = Cooperation
        fields = ['name', 'surname', 'country', 'city', 'number_of_phone', 'email']


class PurchaseForm(forms.Form):
    """Форма для заказа."""

    volume = forms.ChoiceField(choices=VOLUME_CHOICES)
    quantity = forms.IntegerField(min_value=1)
    phone = forms.CharField(max_length=13)
    email = forms.EmailField()


class LoginForm(AuthenticationForm):
    """Форма для POST запроса на вход юзера."""
    
    class Meta:
        model = User
        fields = ['username', 'password'] 


class RegisterForm(UserCreationForm):
    """Форма для POST запроса на создание юзера."""
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 