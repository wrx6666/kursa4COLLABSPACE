from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('author', 'Автор'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Роль')
    verified = models.BooleanField(default=False, verbose_name='Верифицирован')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    avatar_file = models.ImageField(
        upload_to='profiles/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Загрузите аватар с вашего компьютера'
    )
    avatar_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на аватар', help_text='URL аватара (сохраняется автоматически после загрузки)')
    project_links = models.TextField(blank=True, null=True, verbose_name='Ссылки на проекты', help_text='JSON массив ссылок')
    
    def get_project_links_list(self):
        """Возвращает список ссылок на проекты"""
        import json
        if self.project_links:
            try:
                return json.loads(self.project_links)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Профиль {self.user.username}'
    
    def get_role_display_class(self):
        """Возвращает CSS класс для отображения роли"""
        role_classes = {
            'user': 'text-inkMuted',
            'author': 'text-accent-blue',
            'admin': 'text-accent-purple',
        }
        return role_classes.get(self.role, 'text-inkMuted')
