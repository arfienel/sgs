from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
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

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")

@login_required
def create_server(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name:
            server = Server.objects.create(name=name, description=description, owner=request.user)
            server.members.add(request.user)
            messages.success(request, "Сервер успешно создан")
            return redirect("server_detail", server_id=server.id)
        else:
            messages.error(request, "Название сервера обязательно")
    return render(request, "chat/create_server.html")

@login_required
def create_channel(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if request.method == "POST":
        if request.user != server.owner:
            messages.error(request, "Вы не можете создавать каналы на этом сервере")
            return redirect("server_detail", server_id=server_id)
        name = request.POST.get("name")
        is_voice = request.POST.get("is_voice")
        if name:
            Channel.objects.create(name=name, is_voice=is_voice, server=server)
            messages.success(request, f"Канал {name} успешно создан")
            return redirect("server_detail", server_id=server_id)
        else:
            messages.error(request, "Название канала обязательно")
    return render(request, "chat/create_channel.html", {"server": server})

@login_required
def server_detail(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    return render(request, "chat/server_detail.html", {"server": server})