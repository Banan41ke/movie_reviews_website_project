from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Страница логина работает!")
