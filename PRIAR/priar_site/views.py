from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from .logs.SetLogs import SetLogs

logger = SetLogs().logger

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, 'services.html')

def login(request):
    try:
        return render(request, 'login.html')
    except Exception as e:
        print(f'ошибка в login: {e}')
        logger.exception(f'ошибка в login: {e}')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Пользователь успешно вошел, перенаправьте его на нужную страницу
            return redirect('index')
        else:
            # Ошибка аутентификации, покажите сообщение об ошибке
            messages.error(request, 'Неправильный логин или пароль.')
    return redirect('login')

# Создание пользователя
@login_required
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        region = request.POST.get('region')

        if not login or not password or not region:
            return JsonResponse({'success': False, 'message': 'Login and password are required.'})

        if UsersModel.objects.filter(login=login).exists():
            return JsonResponse({'success': False, 'message': 'A user with this login already exists.'})
    
        hashed_password = make_password(password)
        user = UsersModel(login=login, password=hashed_password, region=region)
        user.save()
        return JsonResponse({'success': True, 'message': 'The user has been successfully created.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})