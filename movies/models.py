# movies/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


User = get_user_model()

def poster_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'posters/{uuid.uuid4()}.{ext}'


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,  # ← ДОБАВЛЕНО: уникальность
        db_index=True  # ← ДОБАВЛЕНО: индекс для быстрого поиска
    )

    # ДОБАВЛЕНО: добавим метаданные и индексы
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(
        max_length=255,
        db_index=True  # ← ДОБАВЛЕНО: индекс для поиска по названию
    )
    description = models.TextField()
    release_year = models.IntegerField(
        validators=[  # ← ДОБАВЛЕНО: валидаторы
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 5)
        ],
        db_index=True  # ← ДОБАВЛЕНО: индекс для фильтрации по году
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
        blank=True,
        db_table="movie_genres"  # ← ДОБАВЛЕНО: явное имя таблицы для SQL Server
    )
    poster = models.ImageField(
        upload_to=poster_upload_path,
        blank=True,
        null=True,
        max_length=500  # ← ДОБАВЛЕНО: SQL Server требует max_length для ImageField
    )
    trailer_url = models.URLField(
        blank=True,
        null=True,
        max_length=500  # ← ДОБАВЛЕНО: увеличенная длина для URL
    )
    director = models.CharField(
        max_length=200,
        blank=True,
        db_index=True  # ← ДОБАВЛЕНО: индекс для поиска по режиссеру
    )
    country = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # ← ДОБАВЛЕНО: индекс для сортировки
    )

    # ДОБАВЛЕНО: кэшированные поля для оптимизации
    avg_rating = models.FloatField(default=0.0, db_index=True)
    reviews_count = models.PositiveIntegerField(default=0, db_index=True)

    # ДОБАВЛЕНО: поле для мягкого удаления
    is_active = models.BooleanField(default=True, db_index=True)

    def update_cached_fields(self):
        """Обновление кэшированных полей"""
        from django.db.models import Avg, Count
        if self.pk:
            result = self.reviews.aggregate(
                avg_rating=Avg('rating'),
                count=Count('id')
            )
            self.avg_rating = result['avg_rating'] or 0.0
            self.reviews_count = result['count'] or 0
            self.save(update_fields=['avg_rating', 'reviews_count'])

    def average_rating(self):
        """Используем кэшированное значение"""
        return round(self.avg_rating, 1)

    def reviews_count_method(self):
        """Используем кэшированное значение"""
        return self.reviews_count

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title', 'release_year']),
            models.Index(fields=['director', 'release_year']),
            models.Index(fields=['release_year', 'avg_rating']),
            models.Index(fields=['is_active', 'created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'release_year'],
                name='unique_movie_title_year'
            )
        ]


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_index=True  # ← ДОБАВЛЕНО: индекс для внешнего ключа
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_index=True  # ← ДОБАВЛЕНО: индекс для внешнего ключа
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]  # ← ДОБАВЛЕНО: валидаторы
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # ← ДОБАВЛЕНО: индекс для сортировки
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """При сохранении обновляем кэш фильма"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or 'rating' in kwargs.get('update_fields', []):
            self.movie.update_cached_fields()

    def delete(self, *args, **kwargs):
        """При удалении обновляем кэш фильма"""
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_cached_fields()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "user"],
                name="one_review_per_user_per_movie"
            )
        ]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['movie', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['rating', 'created_at']),
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.rating})"


class Comment(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )

    # ДОБАВЛЕНО: поле для ответов на комментарии
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # ДОБАВЛЕНО: поле для мягкого удаления
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['movie', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['parent', 'created_at']),
        ]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )
    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # ← ДОБАВЛЕНО: индекс
    )

    # ДОБАВЛЕНО: поле для заметок
    note = models.TextField(blank=True, null=True, max_length=500)

    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['movie', 'created_at']),
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


# ДОБАВЛЕНО: Модель для хранения просмотров/посещений
class MovieView(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='views',
        db_index=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['movie', 'created_at']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Просмотр фильма"
        verbose_name_plural = "Просмотры фильмов"

    def __str__(self):
        user_str = self.user.username if self.user else 'Аноним'
        return f"{user_str} просмотрел {self.movie.title}"