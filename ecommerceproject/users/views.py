from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'users/index.html', {})

def no_user(request):
    return render(request, 'users/index.html', {'no_user': True})

def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return render(request, 'users/login.html', {})
    if username and password:
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/users/login/success/')
            else:
                return render(request, 'users/login.html', {'try_again': True})
        else:
           return render(request, 'users/login.html', {'try_again': True}) 

def login_success(request):
    return render(request, 'users/login_success.html', {})

def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html', {})

def signup(request):
    return render(request, 'users/signup.html', {})

def signup_success(request):
    new_user = User.objects.create_user(username = request.POST.get('username'), password = request.POST.get('password'), email = request.POST.get('email'), first_name = request.POST.get('firstname'), last_name = request.POST.get('lastname'))
    return render(request, 'users/signup_success.html', {'new_user': new_user})