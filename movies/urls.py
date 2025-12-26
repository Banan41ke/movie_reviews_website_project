# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("<int:movie_id>/review/add/", views.add_review, name="add_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("<int:movie_id>/comment/add/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path('<int:movie_id>/favorite/add/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:movie_id>/favorite/remove/', views.remove_from_favorites, name='remove_from_favorites'),
    path("year/<int:year>/", views.movies_by_year, name="movies_by_year"),
]