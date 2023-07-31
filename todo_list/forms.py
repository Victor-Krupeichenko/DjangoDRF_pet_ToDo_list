from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CreateTaskForm(forms.ModelForm):
    """Form create Task"""

    class Meta:
        model = Task
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
            self.fields[field].label = ""

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        if len(title) < 3 or len(description) < 3:
            raise forms.ValidationError(f"Поля должны содеражть минимум по 3 символа")
        return cleaned_data


class RegisterUserForm(UserCreationForm):
    """Register User"""

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"{username} уже существует")
        if len(username.replace(" ", '')) < 3:
            raise forms.ValidationError("Имя пользователя должно состоять не меньше чем из 3 символов")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs["class"] = "form-control"
            self.fields[filed].label = ""
            self.fields[filed].help_text = ""
        self.fields["password1"].widget.attrs["placeholder"] = "password"
        self.fields["password2"].widget.attrs["placeholder"] = "confirm password"
        self.fields["username"].widget.attrs["placeholder"] = "username"


class LoginUserForm(AuthenticationForm):
    """Login user"""
    username = forms.CharField(min_length=3)
    password = forms.CharField(label="password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
            self.fields[field].label = ""
