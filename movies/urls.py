from django.urls import path
from .views import movie_list, movie_detail

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
]

