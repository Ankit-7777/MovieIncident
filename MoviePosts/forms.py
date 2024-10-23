from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Comment, Rating


class BaseForm(forms.ModelForm):
    """A base form to handle common attributes for other forms."""
    class Meta:
        widgets = {
            'style': 'width: 300px;',
        }


class SignUpForm(UserCreationForm):
    """Form for user registration."""
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'style': 'width: 300px;'}),
            'password1': forms.PasswordInput(attrs={'style': 'width: 300px;'}),
            'password2': forms.PasswordInput(attrs={'style': 'width: 300px;'}),
        }


class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'style': 'width: 300px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: 300px;'}))


class MovieForm(BaseForm):
    """Form for creating a movie."""
    class Meta(BaseForm.Meta):
        model = Movie
        fields = ('name', 'description', 'poster', 'trailer_video', 'full_movie_video', 'release_date', 'language', 'tags')
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'language': forms.TextInput(),
        }



class CommentForm(BaseForm):
    """Form for submitting a comment."""
    class Meta(BaseForm.Meta):
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }


class RatingForm(BaseForm):
    """Form for submitting a rating and review."""
    class Meta(BaseForm.Meta):
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-rating'}),
            'review': forms.Textarea(attrs={'style': 'width: 300px;', 'rows': 4}),
        }

