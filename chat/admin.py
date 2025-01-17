from .models import Server, Channel, Message, CustomUser
from django.contrib import admin

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('username',)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'server', 'created_at')
    search_fields = ('name', 'server__name')
    list_filter = ('server', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'content', 'created_at')
    search_fields = ('user__username', 'channel__name', 'content')
    list_filter = ('channel', 'created_at')
