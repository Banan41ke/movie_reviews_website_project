from django.contrib import admin
from .models import Movie, Genre, Review
from django.utils.html import format_html


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "genres_list", "poster_preview")
    list_filter = ("release_year", "genres")
    search_fields = ("title",)
    filter_horizontal = ("genres",)

    def genres_list(self, obj):
        return ", ".join(g.name for g in obj.genres.all())
    genres_list.short_description = "Жанры"

    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="height:60px;" />', obj.poster.url)
        return "—"
    poster_preview.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    list_filter = ("rating",)
