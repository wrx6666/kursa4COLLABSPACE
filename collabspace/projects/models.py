from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    SECTION_CHOICES = [
        ('design', 'Дизайн'),
        ('music', 'Музыка'),
        ('writing', 'Писательство'),
        ('video', 'Видео'),
        ('photography', 'Фотография'),
        ('programming', 'Программирование'),
        ('art', 'Искусство'),
        ('other', 'Другое'),
    ]
    
    TAG_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('professional', 'Профессиональный'),
        ('collaboration', 'Коллаборация'),
        ('solo', 'Соло'),
        ('experimental', 'Экспериментальный'),
        ('commercial', 'Коммерческий'),
        ('personal', 'Личный'),
        ('educational', 'Образовательный'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    section = models.CharField(
        max_length=20, 
        choices=SECTION_CHOICES, 
        default='other',
        verbose_name='Раздел'
    )
    tags = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name='Теги',
        help_text='Выберите один или несколько тегов'
    )
    image_file = models.ImageField(
        upload_to='projects/images/',
        blank=True,
        null=True,
        verbose_name='Изображение проекта',
        help_text='Загрузите изображение проекта (не обязательно)'
    )
    image_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name='Ссылка на изображение проекта',
        help_text='URL изображения (сохраняется автоматически после загрузки)'
    )
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Возвращает список тегов"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_tags_display_list(self):
        """Возвращает список отображаемых названий тегов"""
        if not self.tags:
            return []
        tag_values = [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        tag_dict = dict(self.TAG_CHOICES)
        return [tag_dict.get(tag, tag) for tag in tag_values]
    
    def get_participants(self):
        """Возвращает список участников проекта"""
        return self.participants.all()
    
    def is_participant(self, user):
        """Проверяет, является ли пользователь участником проекта"""
        return self.participants.filter(user=user).exists()
    
    def is_owner_or_participant(self, user):
        """Проверяет, является ли пользователь владельцем или участником"""
        return self.owner == user or self.is_participant(user)


class ProjectParticipant(models.Model):
    """Участники проекта"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name='Проект'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_participations',
        verbose_name='Участник'
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_participants',
        verbose_name='Приглашен'
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата присоединения')
    
    class Meta:
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проектов'
        unique_together = ['project', 'user']  # Один пользователь не может быть участником дважды
        ordering = ['-joined_at']
    
    def __str__(self):
        return f'{self.user.username} в проекте {self.project.title}'


class ProjectFavorite(models.Model):
    """Понравившиеся проекты"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_projects',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Проект'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Понравившийся проект'
        verbose_name_plural = 'Понравившиеся проекты'
        unique_together = ['user', 'project']  # Один пользователь не может добавить проект дважды
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.project.title}'


class ProjectInvitation(models.Model):
    """Приглашения в проекты"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='invitations',
        verbose_name='Проект'
    )
    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_invitations',
        verbose_name='Приглашенный пользователь'
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
        verbose_name='Пригласил'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Приглашение в проект'
        verbose_name_plural = 'Приглашения в проекты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Приглашение {self.invited_user.username} в {self.project.title}'
    
    def can_be_accepted(self):
        """Проверяет, можно ли принять приглашение"""
        return self.status == 'pending'
    
    def can_be_cancelled(self):
        """Проверяет, можно ли отменить приглашение"""
        return self.status == 'pending'


class Task(models.Model):
    """Задачи проекта"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Исполнитель'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дедлайн'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Создал'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} ({self.project.title})'
    
    def is_overdue(self):
        """Проверяет, просрочена ли задача"""
        if self.deadline and self.status not in ['completed', 'cancelled']:
            from django.utils import timezone
            return timezone.now() > self.deadline
        return False


class Comment(models.Model):
    """Комментарии к проектам и задачам"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
        verbose_name='Проект'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
        verbose_name='Задача'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
        verbose_name='Родительский комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
    
    def __str__(self):
        if self.project:
            return f'Комментарий к проекту "{self.project.title}" от {self.author.username}'
        elif self.task:
            return f'Комментарий к задаче "{self.task.title}" от {self.author.username}'
        return f'Комментарий от {self.author.username}'
    
    # Метод clean() удален, так как проект устанавливается в форме при сохранении
    
    def get_replies(self):
        """Возвращает все ответы на комментарий"""
        return self.replies.all().order_by('created_at')
    
    def is_reply(self):
        """Проверяет, является ли комментарий ответом"""
        return self.parent is not None


def create_notification(user, notification_type, message, project=None, task=None, invitation=None, comment=None):
    """Вспомогательная функция для создания уведомлений"""
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        project=project,
        task=task,
        invitation=invitation,
        comment=comment
    )


class Notification(models.Model):
    """Уведомления для пользователей"""
    NOTIFICATION_TYPES = [
        ('invitation', 'Приглашение в проект'),
        ('comment_project', 'Комментарий к проекту'),
        ('comment_task', 'Комментарий к задаче'),
        ('task_changed', 'Изменение задачи'),
        ('task_assigned', 'Назначение на задачу'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    message = models.TextField(verbose_name='Текст уведомления')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    
    # Связи с объектами (опциональные)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Проект'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Задача'
    )
    invitation = models.ForeignKey(
        'ProjectInvitation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Приглашение'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Комментарий'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f'{self.get_notification_type_display()} для {self.user.username}'
    
    def mark_as_read(self):
        """Отмечает уведомление как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])

