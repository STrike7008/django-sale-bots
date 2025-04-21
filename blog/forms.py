from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'image', 'additional_images']

    additional_images = forms.ModelMultipleChoiceField(
        queryset=PostImage.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField(label='Пошук', required=False)