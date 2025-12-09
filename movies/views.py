from django.http import JsonResponse
from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()

    data = []
    for movie in movies:
        data.append({
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "average_rating": movie.average_rating(),
            "genres": [g.name for g in movie.genres.all()],
        })

    return JsonResponse({"movies": data})


def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"error": "Movie not found"}, status=404)

    reviews_data = []
    for review in movie.reviews.all():
        reviews_data.append({
            "user": review.user.username,
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at,
        })

    data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "release_year": movie.release_year,
        "average_rating": movie.average_rating(),
        "genres": [g.name for g in movie.genres.all()],
        "reviews": reviews_data,
    }

    return JsonResponse(data)
