from django.contrib import admin
from .models import Movie, Comment, Rating, View

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'release_date', 'rating', 'views_count')
    search_fields = ('name', 'director__username')
    list_filter = ('release_date', 'language', 'tags')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'created_date', 'approved')
    list_filter = ('approved',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_date')
    list_filter = ('rating',)

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'created_date')
