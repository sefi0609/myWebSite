"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Main page
def index(request):
    return render(request, 'login_app/index.html')

# Logout a user view
def logout_user(request):
    auth.logout(request)
    return redirect('login_app:index')

# Login a user view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('login_app:index')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_app:login_user')
    else:
         return render(request, 'login_app/login.html')

# Singup a user view
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('login_app:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('login_app:register')
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login_app:login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('login_app:register')
    else:
        return render(request, 'login_app/registeration.html')

# Contact view
def contact(request):
    return render(request, 'login_app/contact.html')

# About view
def about(request):
    return render(request, 'login_app/about.html')
