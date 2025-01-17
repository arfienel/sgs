# Generated by Django 5.1.4 on 2025-01-16 23:45

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название канала')),
                ('is_voice', models.BooleanField(default=False, verbose_name='Является ли канал голосовым')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания канала')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар пользователя')),
                ('status', models.CharField(default='Online', max_length=100, verbose_name="Статус пользователя (например, 'Online')")),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержимое сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки сообщения')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.channel', verbose_name='Канал, в котором отправлено сообщение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, отправивший сообщение')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/', verbose_name='Файл вложения')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время загрузки файла')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='chat.message', verbose_name='Сообщение, к которому прикреплено вложение')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название сервера')),
                ('description', models.TextField(blank=True, verbose_name='Описание сервера')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания сервера')),
                ('members', models.ManyToManyField(related_name='joined_servers', to=settings.AUTH_USER_MODEL, verbose_name='Участники сервера')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_servers', to=settings.AUTH_USER_MODEL, verbose_name='Владелец сервера')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название роли')),
                ('permissions', models.TextField(verbose_name='Права доступа в формате JSON или строки')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='chat.server', verbose_name='Сервер, на котором действует роль')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Уникальный код приглашения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания приглашения')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время истечения срока действия приглашения')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_invitations', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, создавший приглашение')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='chat.server', verbose_name='Сервер, на который создается приглашение')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='chat.server', verbose_name='Сервер, к которому относится канал'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['created_at'], name='message_created_at_idx'),
        ),
        migrations.AddIndex(
            model_name='attachment',
            index=models.Index(fields=['uploaded_at'], name='attachment_uploaded_at_idx'),
        ),
        migrations.AddIndex(
            model_name='server',
            index=models.Index(fields=['name'], name='server_name_idx'),
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['name'], name='role_name_idx'),
        ),
        migrations.AddIndex(
            model_name='invitation',
            index=models.Index(fields=['code'], name='invitation_code_idx'),
        ),
        migrations.AddIndex(
            model_name='channel',
            index=models.Index(fields=['name'], name='channel_name_idx'),
        ),
    ]
