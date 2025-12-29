from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Project, ProjectParticipant, Task, Comment
from utils.validators import validate_content


class ProjectForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=Project.TAG_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        label='Теги',
        help_text='Выберите один или несколько тегов (не обязательно)'
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'section', 'tags', 'image_file']
        labels = {
            'title': 'Название проекта',
            'description': 'Описание',
            'section': 'Раздел',
            'image_file': 'Изображение проекта',
        }
        help_texts = {
            'image_file': 'Загрузите изображение с вашего компьютера (не обязательно)',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
                'placeholder': 'Введите название проекта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
                'placeholder': 'Опишите ваш проект',
                'rows': 6
            }),
            'section': forms.Select(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink'
            }),
            'image_file': forms.FileInput(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink file:mr-4 file:py-2 file:px-4 file:rounded-btn file:border-0 file:text-sm file:font-semibold file:bg-accent-blue/20 file:text-accent-blue hover:file:bg-accent-blue/30 file:cursor-pointer',
                'accept': 'image/*'
            }),
        }
    
    def clean_title(self):
        """Валидация названия проекта на запрещенные слова"""
        title = self.cleaned_data.get('title')
        if title:
            validate_content(title, 'Название проекта')
        return title
    
    def clean_description(self):
        """Валидация описания проекта на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            validate_content(description, 'Описание проекта')
        return description
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если редактируем существующий проект, устанавливаем начальные значения тегов
        # Это нужно для правильного отображения выбранных тегов при редактировании
        if self.instance and self.instance.pk and self.instance.tags:
            # Получаем список тегов из строки
            tags_list = self.instance.get_tags_list()
            # Устанавливаем начальные значения для MultipleChoiceField
            # Django автоматически использует initial только если нет данных в POST
            self.initial['tags'] = tags_list
            self.fields['tags'].initial = tags_list


class InviteParticipantForm(forms.Form):
    """Форма для приглашения участника в проект"""
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Введите имя пользователя'
        }),
        help_text='Введите имя пользователя, которого хотите пригласить'
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Введите имя пользователя.')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Пользователь с таким именем не найден.')
        
        return username


class TaskForm(forms.ModelForm):
    """Форма для создания и редактирования задач"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status', 'deadline']
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'assignee': 'Исполнитель',
            'status': 'Статус',
            'deadline': 'Дедлайн',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
                'placeholder': 'Введите название задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
                'placeholder': 'Опишите задачу (не обязательно)',
                'rows': 4
            }),
            'assignee': forms.Select(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
        }
    
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        
        # Ограничиваем выбор исполнителя только участниками проекта
        if self.project:
            # Получаем всех участников проекта (владелец + участники)
            participants = [self.project.owner]
            participants.extend([p.user for p in self.project.get_participants()])
            
            # Создаем queryset из участников
            from django.db.models import Q
            participant_ids = [p.id for p in participants]
            self.fields['assignee'].queryset = User.objects.filter(
                Q(id__in=participant_ids)
            )
            self.fields['assignee'].required = False
            self.fields['assignee'].empty_label = 'Не назначен'
        
        # Устанавливаем формат для дедлайна
        if 'deadline' in self.fields:
            self.fields['deadline'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
            # Если редактируем существующую задачу, форматируем дедлайн для datetime-local
            if self.instance and self.instance.pk and self.instance.deadline:
                from django.utils import timezone
                deadline = self.instance.deadline
                if timezone.is_aware(deadline):
                    deadline = timezone.localtime(deadline)
                self.fields['deadline'].widget.attrs['value'] = deadline.strftime('%Y-%m-%dT%H:%M')
    
    def clean_title(self):
        """Валидация названия задачи на запрещенные слова"""
        title = self.cleaned_data.get('title')
        if title:
            validate_content(title, 'Название задачи')
        return title
    
    def clean_description(self):
        """Валидация описания задачи на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            validate_content(description, 'Описание задачи')
        return description


class ProjectSearchForm(forms.Form):
    """Форма для поиска и фильтрации проектов"""
    search = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Поиск по названию проекта...'
        })
    )
    tags = forms.MultipleChoiceField(
        choices=Project.TAG_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        label='Теги',
        help_text='Выберите теги для фильтрации (не обязательно)'
    )
    section = forms.ChoiceField(
        choices=[('', 'Все разделы')] + list(Project.SECTION_CHOICES),
        required=False,
        label='Раздел',
        widget=forms.Select(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink'
        })
    )


class CommentForm(forms.ModelForm):
    """Форма для создания комментариев к проектам и задачам"""
    
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Комментарий',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted resize-none',
                'placeholder': 'Напишите комментарий...',
                'rows': 4
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Извлекаем project и task из kwargs ДО вызова super()
        self.project = kwargs.pop('project', None)
        self.task = kwargs.pop('task', None)
        super().__init__(*args, **kwargs)
        
        # Дополнительная проверка
        if not hasattr(self, 'project'):
            self.project = None
        if not hasattr(self, 'task'):
            self.task = None
    
    def clean_text(self):
        """Валидация текста комментария на запрещенные слова"""
        text = self.cleaned_data.get('text')
        if text:
            validate_content(text, 'Комментарий')
        return text
    
    def save(self, commit=True, author=None, project=None, task=None, parent=None):
        """Сохраняет комментарий с указанным автором, проектом или задачей"""
        comment = super().save(commit=False)
        
        if not author:
            raise ValueError('Необходимо указать автора комментария.')
        
        if not project and not task:
            # Пытаемся получить из атрибутов формы
            project = getattr(self, 'project', None)
            task = getattr(self, 'task', None)
        
        if not project and not task:
            raise ValueError('Необходимо указать либо проект, либо задачу.')
        
        if project and task:
            raise ValueError('Нельзя указать одновременно проект и задачу.')
        
        comment.author = author
        if project:
            comment.project = project
        if task:
            comment.task = task
        
        if parent:
            comment.parent = parent
        
        if commit:
            # Просто сохраняем, валидация уже прошла в форме
            comment.save()
        return comment

