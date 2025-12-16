# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.http import JsonResponse
from .models import Favorite
from .models import Movie, Review, Comment, Genre
from .forms import ReviewForm, CommentForm


@login_required
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        movie=movie
    )
    
    if created:
        messages.success(request, f'Фильм "{movie.title}" добавлен в избранное!')
    else:
        messages.info(request, f'Фильм "{movie.title}" уже в избранном!')
    
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def remove_from_favorites(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    Favorite.objects.filter(user=request.user, movie=movie).delete()
    messages.success(request, f'Фильм "{movie.title}" удален из избранного!')
    
    if request.GET.get('from') == 'favorites':
        return redirect('favorites')
    
    return redirect('movie_detail', movie_id=movie_id)

def movie_list(request):
    movies = Movie.objects.all().annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-created_at')

    # Фильтрация по жанру
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(title__icontains=search_query)

    # Все жанры
    genres = Genre.objects.all()

    context = {
        'movies': movies,
        'genres': genres,
        'selected_genre': genre_id,
        'search_query': search_query,
    }
    
    return render(request, 'movies/index.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Отзывы для этого фильма
    reviews = Review.objects.filter(movie=movie).select_related('user').order_by('-created_at')

    # Комментарии для этого фильма
    comments = Comment.objects.filter(movie=movie).select_related('user').order_by('-created_at')

    # Формы
    review_form = ReviewForm()
    comment_form = CommentForm()

    # Проверяем, оставлял ли текущий пользователь отзыв
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(movie=movie, user=request.user)
        except Review.DoesNotExist:
            pass

    context = {
        'movie': movie,
        'reviews': reviews,
        'comments': comments,
        'review_form': review_form,
        'comment_form': comment_form,
        'user_review': user_review,
        'avg_rating': movie.average_rating(),
        'reviews_count': reviews.count(),
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Проверяем, не оставлял ли пользователь уже отзыв
    if Review.objects.filter(movie=movie, user=request.user).exists():
        messages.warning(request, 'Вы уже оставили отзыв на этот фильм!')
        return redirect('movie_detail', movie_id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, 'movies/review_form.html', {
        'form': form,
        'movie': movie,
    })


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Проверяем, не оставлял ли пользователь уже отзыв
    if Review.objects.filter(movie=movie, user=request.user).exists():
        messages.warning(request, 'Вы уже оставили отзыв на этот фильм!')
        return redirect('movie_detail', movie_id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('movie_detail', movie_id=movie_id)
        else:
            # Если форма невалидна, показываем ее снова с ошибками
            return render(request, 'movies/review_form.html', {
                'form': form,
                'movie': movie,
            })
    else:
        # GET запрос - показываем пустую форму
        form = ReviewForm()

    # ОБЯЗАТЕЛЬНО вернуть render в конце
    return render(request, 'movies/review_form.html', {
        'form': form,
        'movie': movie,
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_id = review.movie.id
    review.delete()
    messages.success(request, 'Отзыв успешно удален!')
    return redirect('movie_detail', movie_id=movie_id)


@login_required
def add_comment(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен!')

    return redirect('movie_detail', movie_id=movie_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    movie_id = comment.movie.id
    comment.delete()
    messages.success(request, 'Комментарий успешно удален!')
    return redirect('movie_detail', movie_id=movie_id)