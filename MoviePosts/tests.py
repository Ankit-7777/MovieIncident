from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .factories import MovieFactory, CommentFactory, ViewFactory, RatingFactory, UserFactory
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from .models import Movie



class MovieTestCase(TestCase):
    def setUp(self):
        self.movie = MovieFactory(name="Test Movie 1")

    def test_movie_creation(self):
        """Test that a movie is created successfully."""
        self.assertIsNotNone(self.movie.release_date)
        self.assertEqual(self.movie.name, "Test Movie 1") 
        self.assertTrue(self.movie.poster)
        self.assertTrue(self.movie.trailer_video)
        self.assertTrue(self.movie.full_movie_video)

    def test_movie_update(self):
        """Test that a movie is updated successfully."""
        response = self.client.post(reverse('movie_edit', args=[self.movie.pk]), {
            'release_date': '2024-01-01', 
            'poster': self.movie.poster,
            'trailer_video': self.movie.trailer_video,
            'full_movie_video': self.movie.full_movie_video,
        })
        
        self.assertEqual(response.status_code, 200)  
        print(response.context) 
        print(response.content) 
        self.movie.refresh_from_db()

    def test_movie_delete(self):
        """Test that a movie is deleted successfully."""
        response = self.client.post(reverse('movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())  


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="TestUser1", email="TestUser1@example.com")  

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.username, "TestUser1")  
        self.assertTrue(self.user.check_password("password123"))
    
    def test_user_email(self):
        """Test that user email is correctly formatted."""
        self.assertEqual(self.user.email, "TestUser1@example.com")  


class CommentTestCase(TestCase):
    def setUp(self):
        self.comment = CommentFactory()

    def test_comment_creation(self):
        """Test that a comment is created successfully."""
        self.assertIsNotNone(self.comment.text)
        self.assertFalse(self.comment.approved)
        self.assertIsNotNone(self.comment.created_date)

    def test_comment_approval(self):
        """Test that a comment can be approved."""
        self.comment.approve()
        self.assertTrue(self.comment.approved)

    


class RatingTestCase(TestCase):
    def setUp(self):
        self.rating = RatingFactory()

    def test_rating_creation(self):
        """Test that a rating is created successfully."""
        self.assertTrue(1 <= self.rating.rating <= 7)  
        self.assertIsNotNone(self.rating.review)
        self.assertIsNotNone(self.rating.created_date)
    
    def test_rating_value(self):
        """Test that the rating value is valid."""
        self.assertTrue(1 <= self.rating.rating <= 10, "Rating should be between 1 and 10")

    def test_rating_review_optional(self):
        """Test that a review is optional."""
        rating_without_review = RatingFactory(review=None)
        self.assertIsNone(rating_without_review.review)

