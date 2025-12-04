from django.contrib import admin
from .models import Movie, Genre, Review

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year")
    list_filter = ("release_year",)
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("movie__title", "user__username")
