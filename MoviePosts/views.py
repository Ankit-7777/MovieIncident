from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag

from .models import Movie, Comment, Rating
from .forms import SignUpForm, LoginForm, MovieForm, CommentForm, RatingForm

# --- User Authentication Views ---

# User Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('movie_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# User Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('movie_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# --- Movie Views ---

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies'
    paginate_by = 10  # Pagination: 10 movies per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_rating'] = Movie.objects.aggregate(Avg('rating'))['rating__avg']
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object
        context['comments'] = movie.comments.all()
        user_rating = movie.ratings.filter(user=self.request.user).first()
        context['user_rating'] = user_rating.rating if user_rating else None
        context['comment_form'] = CommentForm()
        context['rating_form'] = RatingForm()
        context['messages'] = messages.get_messages(self.request)
        context['can_edit'] = movie.director == self.request.user
        return context


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy('movie_list')

    def form_valid(self, form):
        form.instance.director = self.request.user
        return super().form_valid(form)


class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy('movie_list')


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movie_confirm_delete.html'
    success_url = reverse_lazy('movie_list')


# --- Comment Views ---

@login_required
def add_comment(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if movie.director == request.user:
                messages.error(request, "You cannot comment on your own movie.")
            else:
                existing_comment = Comment.objects.filter(movie=movie, author=request.user).first()
                if existing_comment:
                    existing_comment.text = form.cleaned_data['text']
                    existing_comment.save()
                    messages.success(request, "Your comment has been updated!")
                else:
                    comment = form.save(commit=False)
                    comment.movie = movie
                    comment.author = request.user
                    comment.save()
                    messages.success(request, "Your comment has been added!")
            return redirect('movie_detail', pk=pk)
    return redirect('movie_detail', pk=pk)


# --- Rating Views ---

@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if movie.director == request.user:
                messages.error(request, "You cannot rate your own movie.")
            else:
                existing_rating = Rating.objects.filter(movie=movie, user=request.user).first()
                rating_value = form.cleaned_data['rating']

                if existing_rating:
                    existing_rating.rating = rating_value
                    existing_rating.review = form.cleaned_data['review']
                    existing_rating.save()
                    messages.success(request, "Your rating has been updated!")
                else:
                    rating = form.save(commit=False)
                    rating.movie = movie
                    rating.user = request.user
                    rating.save()
                    messages.success(request, "Your rating has been submitted!")
            return redirect('movie_detail', pk=pk)
    return redirect('movie_detail', pk=pk)


@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if Rating.objects.filter(movie=movie, user=request.user).exists():
                messages.error(request, "You have already reviewed this movie.")
            else:
                rating = form.save(commit=False)
                rating.movie = movie
                rating.user = request.user
                rating.save()
                messages.success(request, "Your review has been added!")
            return redirect('movie_detail', pk=pk)
    return redirect('movie_detail', pk=pk)


@login_required
def update_review(request, pk):
    rating = get_object_or_404(Rating, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated!")
        return redirect('movie_detail', pk=rating.movie.pk)
    return redirect('movie_detail', pk=rating.movie.pk)


@login_required
def delete_review(request, pk):
    rating = get_object_or_404(Rating, pk=pk, user=request.user)
    if request.method == 'POST':
        rating.delete()
        messages.success(request, "Your review has been deleted!")
        return redirect('movie_detail', pk=rating.movie.pk)
    return redirect('movie_detail', pk=rating.movie.pk)


# --- Tag Management Views ---

@login_required
@csrf_exempt
def edit_movie_tags(request, pk):
    movie = get_object_or_404(Movie, pk=pk, director=request.user)
    if request.method == 'POST':
        tags = request.POST.get('tags').split(',')
        movie.tags.clear()
        for tag in tags:
            tag = tag.strip()
            if tag:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                movie.tags.add(tag_obj)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@csrf_exempt
def remove_tag(request, pk):
    movie = get_object_or_404(Movie, pk=pk, director=request.user)
    if request.method == 'POST':
        tag_name = request.POST.get('tag', '').strip()
        if tag_name:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag:
                movie.tags.remove(tag)
                return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@csrf_exempt
def add_tag(request, pk):
    movie = get_object_or_404(Movie, pk=pk, director=request.user)
    if request.method == 'POST':
        tag_name = request.POST.get('tag', '').strip()
        if tag_name:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            movie.tags.add(tag_obj)
            return JsonResponse({'success': True, 'tag': tag_name})
    return JsonResponse({'success': False}, status=400)


@login_required
def view_movie_tags(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    tags = movie.tags.all()
    tag_names = [tag.name for tag in tags]
    return JsonResponse({'tags': tag_names})


# --- User Profile ---

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})
