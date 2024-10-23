import factory
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from .models import Movie, Comment, View, Rating
from django.core.files.uploadedfile import SimpleUploadedFile 

# UserFactory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"TestUser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


# MovieFactory
class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    name = factory.Sequence(lambda n: f"Test Movie {n}")
    description = "This is a test movie description."
    director = factory.SubFactory(UserFactory)  # Link to UserFactory
    release_date = factory.LazyFunction(lambda: date.today())
    language = "English"
    rating = 5.0
    views_count = 0
    created_date = factory.LazyFunction(timezone.now)
    published_date = None  # Set to `None`, but you can set a date if needed

    poster = factory.django.ImageField(color='blue')  # Generates a blue image for testing
    trailer_video = factory.LazyAttribute(lambda x: SimpleUploadedFile(
        name='test_video.mp4',
        content=b'semi.mp4',
        content_type='video/mp4'
    ))
    full_movie_video = factory.django.FileField(filename="semi.mp4")


# CommentFactory
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    movie = factory.SubFactory(MovieFactory)
    author = factory.SubFactory(UserFactory)
    text = factory.Faker('text')
    created_date = factory.LazyFunction(timezone.now)
    approved = False


# ViewFactory
class ViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = View

    movie = factory.SubFactory(MovieFactory)
    user = factory.SubFactory(UserFactory)
    session_key = factory.Faker('uuid4')  # Random UUID for session key
    created_date = factory.LazyFunction(timezone.now)


# RatingFactory
class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    movie = factory.SubFactory(MovieFactory)
    user = factory.SubFactory(UserFactory)
    rating = factory.Faker('random_int', min=1, max=10)
    review = factory.Faker('text')
    created_date = factory.LazyFunction(timezone.now)
