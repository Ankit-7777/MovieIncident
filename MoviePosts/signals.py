from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import View, Movie

@receiver(post_save, sender=View)
def update_movie_views_count(sender, instance, created, **kwargs):
    if created:
        movie = instance.movie
        movie.views_count += 1
        movie.save()
