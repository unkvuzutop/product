from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from product.models import Comment


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        name = forms.CharField(min_length=4)
        exclude = ('user', 'product', 'created_at')
