# movies/views.py
from django.shortcuts import render


def movie_list(request):
    movies = [
        {
            'id': 1,
            'title': 'Форсаж 9',
            'year': 2021,
            'duration': 143,
            'avg_rating': 7.5,
            'reviews_count': 245,
            'description': 'Доминик Торетто ведёт тихую жизнь с Летти и своим сыном, но опасность снова настигает его команду.',
            'genres': ['Боевик', 'Триллер'],
            'poster': {'url': '/static/img/posters/fast9.jpg'}
        },
        {
            'id': 2,
            'title': 'Дэдпул и Россомаха',
            'year': 2024,
            'duration': 127,
            'avg_rating': 8.2,
            'reviews_count': 189,
            'description': 'Дэдпул и Россомаха объединяются для выполнения опасной миссии с большим количеством шуток и экшена.',
            'genres': ['Комедия', 'Боевик', 'Фантастика'],
            'poster': {'url': '/static/img/posters/deadpool.jpg'}
        },
        {
            'id': 3,
            'title': 'Легенда',
            'year': 2015,
            'duration': 131,
            'avg_rating': 7.0,
            'reviews_count': 156,
            'description': 'История близнецов Реджи и Ронни Крэй, которые стали королями криминального мира Лондона 1960-х.',
            'genres': ['Драма', 'Криминал', 'Биография'],
            'poster': {'url': '/static/img/posters/legend.jpg'}
        },
        {
            'id': 4,
            'title': 'Интерстеллар',
            'year': 2014,
            'duration': 169,
            'avg_rating': 8.6,
            'reviews_count': 589,
            'description': 'Группа исследователей использует недавно обнаруженный пространственно-временной тоннель.',
            'genres': ['Фантастика', 'Драма', 'Приключения'],
            'poster': {'url': '/static/img/posters/interstellar.jpg'}
        }
    ]
    return render(request, 'movies/index.html', {'movies': movies})


def movie_detail(request, movie_id):
    # Все фильмы
    all_movies = [
        {
            'id': 1,
            'title': 'Форсаж 9',
            'year': 2021,
            'duration': 143,
            'avg_rating': 7.5,
            'reviews_count': 245,
            'description': 'Доминик Торетто ведёт тихую жизнь с Летти и своим сыном, но опасность снова настигает его команду. Новая угроза заставляет Дома собрать свою команду для выполнения самой опасной миссии в их жизни.',
            'genres': ['Боевик', 'Триллер', 'Приключения'],
            'poster': {'url': '/static/img/posters/fast9.jpg'},
            'director': 'Джастин Лин',
            'country': 'США',
            'actors': 'Вин Дизель, Мишель Родригес, Джон Сина'
        },
        {
            'id': 2,
            'title': 'Дэдпул и Россомаха',
            'year': 2024,
            'duration': 127,
            'avg_rating': 8.2,
            'reviews_count': 189,
            'description': 'Дэдпул и Россомаха объединяются для выполнения опасной миссии с большим количеством шуток и экшена. Фильм полон отсылок к комиксам и самоиронии.',
            'genres': ['Комедия', 'Боевик', 'Фантастика', 'Супергерои'],
            'poster': {'url': '/static/img/posters/deadpool.jpg'},
            'director': 'Шон Леви',
            'country': 'США, Канада',
            'actors': 'Райан Рейнольдс, Хью Джекман'
        },
        {
            'id': 3,
            'title': 'Легенда',
            'year': 2015,
            'duration': 131,
            'avg_rating': 7.0,
            'reviews_count': 156,
            'description': 'История близнецов Реджи и Ронни Крэй, которые стали королями криминального мира Лондона 1960-х. Основано на реальных событиях.',
            'genres': ['Драма', 'Криминал', 'Биография', 'Исторический'],
            'poster': {'url': '/static/img/posters/legend.jpg'},
            'director': 'Брайан Хелгеленд',
            'country': 'Великобритания, Франция',
            'actors': 'Том Харди, Эмили Браунинг'
        },
        {
            'id': 4,
            'title': 'Интерстеллар',
            'year': 2014,
            'duration': 169,
            'avg_rating': 8.6,
            'reviews_count': 589,
            'description': 'Группа исследователей использует недавно обнаруженный пространственно-временной тоннель, чтобы обойти ограничения космических путешествий и спасти человечество.',
            'genres': ['Фантастика', 'Драма', 'Приключения'],
            'poster': {'url': '/static/img/posters/interstellar.jpg'},
            'director': 'Кристофер Нолан',
            'country': 'США, Великобритания',
            'actors': 'Мэттью Макконахи, Энн Хэтэуэй'
        }
    ]

    # Находим фильм по ID
    movie = next((m for m in all_movies if m['id'] == movie_id), None)

    if not movie:
        movie = {
            'id': movie_id,
            'title': 'Фильм не найден',
            'description': 'Извините, запрошенный фильм не существует.',
            'year': '—',
            'duration': '—',
            'avg_rating': 0,
            'genres': [],
            'poster': {'url': '/static/img/posters/fast9.jpg'}
        }

    # Тестовые отзывы
    reviews = [
        {
            'user': {'username': 'Алексей Петров'},
            'rating': 8,
            'text': 'Отличный фильм! Экшен на высоте, спецэффекты впечатляют. Мурашки по коже от некоторых сцен. Рекомендую к просмотру всем любителям жанра.',
            'created_at': '15 января 2024'
        },
        {
            'user': {'username': 'Мария Иванова'},
            'rating': 6,
            'text': 'Неплохо, но предыдущие части были лучше. Сюжет немного предсказуем, но общее впечатление положительное.',
            'created_at': '10 января 2024'
        },
        {
            'user': {'username': 'Дмитрий Сидоров'},
            'rating': 9,
            'text': 'Шикарный боевик! Очень динамичный сюжет, отличная операторская работа. Обязательно к просмотру в кинотеатре.',
            'created_at': '5 января 2024'
        }
    ]

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'avg_rating': movie.get('avg_rating', 0)
    })


def review_form(request, movie_id):
    # Простой view для формы отзыва
    movie = {'id': movie_id, 'title': f'Фильм {movie_id}'}
    return render(request, 'movies/review_form.html', {'movie': movie})