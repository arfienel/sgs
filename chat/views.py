from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, CustomUserRegistrationForm

def index(request):
    return render(request, 'index.html')

def chat_room(request, channel_name):
    return render(request, 'chat/chat_room.html', {'channel_name': channel_name})

def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")