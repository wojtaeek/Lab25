from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Issue, Registration


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control"})


class CourseRegisterForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["course", "name", "surname", "phone", "email", "rodo"]
        widgets = {
            "rodo": forms.CheckboxInput(),
        }
