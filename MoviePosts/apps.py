from django.apps import AppConfig


class MoviepostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MoviePosts'
    
    def ready(self):
        import MoviePosts.signals
