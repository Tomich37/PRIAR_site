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
from .models import UsersModel

logger = SetLogs().logger

def index(request):
    return render(request, "index.html", {'user': request.user})

def about(request):
    return render(request, "about.html", {'user': request.user})

def services(request):
    return render(request, 'services.html', {'user': request.user})

def login(request):
    try:
        return render(request, 'login.html', {'user': request.user})
    except Exception as e:
        print(f'ошибка в login: {e}')
        logger.exception(f'ошибка в login: {e}')
        return HttpResponse('Internal Server Error', status=500)

def registration(request):
    try:
        return render(request, 'registration.html', {'user': request.user})
    except Exception as e:
        print(f'ошибка в registration: {e}')
        logger.exception(f'ошибка в registration: {e}')
        return HttpResponse('Internal Server Error', status=500)

def login_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        print(login, password)
        user = authenticate(request, login=login, password=password)
        if user is not None:
            auth_login(request, user)
            # Пользователь успешно вошел, отображаем нужную страницу с контекстом
            return render(request, 'index.html', {'user': request.user})
        else:
            # Ошибка аутентификации, покажите сообщение об ошибке
            messages.error(request, 'Неправильный логин или пароль.')
            print(f'Неправильный логин или пароль.')
    return render(request, 'login.html')

# Создание пользователя
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(login, password)

        if not login or not password or not email:
            return JsonResponse({'success': False, 'message': 'Login and password are required.'})

        if UsersModel.objects.filter(login=login).exists():
            return JsonResponse({'success': False, 'message': 'A user with this login already exists.'})
    
        hashed_password = make_password(password)
        user = UsersModel(login=login, password=hashed_password, email=email)
        user.save()
        return render(request, 'success.html', {'user': request.user})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def success(request):
    try:
        return render(request, 'success.html', {'user': request.user})
    except Exception as e:
        print(f'ошибка в success: {e}')
        logger.exception(f'ошибка в success: {e}')
        return HttpResponse('Internal Server Error', status=500)
    
def logout_view(request):
    logout(request)
    # Пользователь успешно вышел, перенаправьте его на нужную страницу
    return redirect('index')