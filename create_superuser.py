import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_reviews_website_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'admin12345')
    print('✅ Superuser "admin" создан с паролем admin12345')
else:
    print('✅ Superuser "admin" уже существует')