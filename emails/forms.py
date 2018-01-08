from django import forms
from django.forms import ModelForm
from .models import Subscriber


class EmailForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "city"]
