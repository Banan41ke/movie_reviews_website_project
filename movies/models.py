# movies/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.conf import settings

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)  # ТОЛЬКО ОДИН РАЗ!
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    director = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def reviews_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "user"],
                name="one_review_per_user_per_movie"
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.rating})"


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'movie']  # чтобы нельзя было добавить дважды
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"