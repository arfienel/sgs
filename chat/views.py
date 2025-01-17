from django.shortcuts import render

from django.shortcuts import render

def chat_room(request, channel_name):
    return render(request, 'chat/chat_room.html', {
        'channel_name': channel_name
    })