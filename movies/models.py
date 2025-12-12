from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=100)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.count() == 0:
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "user"],
                name="one_review_per_user_per_movie"
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.rating})"
