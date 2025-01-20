from django.contrib.auth.models import AbstractUser
from django.db import models

# модель для хранения данных о пользователе
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар пользователя")
    status = models.CharField(max_length=100, default="Online", verbose_name="Статус пользователя (например, 'Online')")

# Модель сервера
class Server(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название сервера")
    description = models.TextField(blank=True, verbose_name="Описание сервера")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_servers', verbose_name="Владелец сервера")
    members = models.ManyToManyField(CustomUser, related_name='joined_servers', verbose_name="Участники сервера")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания сервера")

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='server_name_idx'),
        ]

    def __str__(self):
        return self.name

# Модель канала
class Channel(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channels', verbose_name="Сервер, к которому относится канал")
    name = models.CharField(max_length=100, verbose_name="Название канала")
    is_voice = models.BooleanField(default=False, verbose_name="Является ли канал голосовым")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания канала")

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='channel_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({'Voice' if self.is_voice else 'Text'})"

# Модель сообщений
class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages', verbose_name="Канал, в котором отправлено сообщение")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь, отправивший сообщение")
    content = models.TextField(verbose_name="Содержимое сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время отправки сообщения")

    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='message_created_at_idx'),
        ]

    def __str__(self):
        return f"Message from {self.user.username} in {self.channel.name}"

# Модель ролей
class Role(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='roles', verbose_name="Сервер, на котором действует роль")
    name = models.CharField(max_length=50, verbose_name="Название роли")
    permissions = models.TextField(verbose_name="Права доступа в формате JSON или строки")

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='role_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} on {self.server.name}"

# Модель приглашений на сервер
class Invitation(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='invitations', verbose_name="Сервер, на который создается приглашение")
    code = models.CharField(max_length=10, unique=True, verbose_name="Уникальный код приглашения")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_invitations', verbose_name="Пользователь, создавший приглашение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания приглашения")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время истечения срока действия приглашения")

    class Meta:
        indexes = [
            models.Index(fields=['code'], name='invitation_code_idx'),
        ]

    def __str__(self):
        return f"Invite to {self.server.name} by {self.created_by.username}"

# Модель вложений
class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments', verbose_name="Сообщение, к которому прикреплено вложение")
    file = models.FileField(upload_to='attachments/', verbose_name="Файл вложения")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время загрузки файла")

    class Meta:
        indexes = [
            models.Index(fields=['uploaded_at'], name='attachment_uploaded_at_idx'),
        ]
