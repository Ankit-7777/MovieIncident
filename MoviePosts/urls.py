from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    signup,
    login_view,
    user_logout,
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    add_comment,
    rate_movie,
    profile,
    edit_movie_tags, remove_tag, add_tag, view_movie_tags,
    add_review, update_review, delete_review
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    
    path('', MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    
    path('movie/<int:pk>/comment/', add_comment, name='add_comment'),
    path('movie/<int:pk>/rate/', rate_movie, name='rate_movie'),
    path('profile/', profile, name='user_profile'),
    
    path('movies/<int:pk>/edit_tags/', edit_movie_tags, name='edit_movie_tags'),
    path('movies/<int:pk>/remove_tag/', remove_tag, name='remove_tag'),
    path('movies/<int:pk>/add_tag/', add_tag, name='add_tags'),
    path('movies/<int:pk>/tags/', view_movie_tags, name='view_movie_tags'),
    
    path('movie/<int:pk>/add_review/', add_review, name='add_review'),
    path('rating/<int:pk>/update/', update_review, name='update_review'),
    path('rating/<int:pk>/delete/', delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

