import json
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Profile
from utils import validate_content


User = get_user_model()


class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('author', 'Автор'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='user',
        widget=forms.HiddenInput(),
        label='Тип аккаунта',
        required=True
    )
    
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Введите имя пользователя'
        }),
        help_text="",
        error_messages={
            'required': 'Введите имя пользователя.',
            'unique': 'Пользователь с таким именем уже существует.',
        }
    )
    
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Введите пароль'
        }),
        help_text="",
    )
    
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Подтвердите пароль'
        }),
        help_text="",
    )
    
    # project_links будет обрабатываться через JavaScript и отправляться как скрытое поле
    
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'example@email.com'
        }),
        error_messages={
            'required': 'Введите email.',
            'invalid': 'Введите корректный email адрес.',
        }
    )
    
    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            "username": "Имя пользователя",
            "email": "Email",
        }
        help_texts = {
            "username": "",
            "email": "",
        }
        error_messages = {
            "username": {
                "required": "Введите имя пользователя.",
                "unique": "Пользователь с таким именем уже существует.",
            },
            "email": {
                "required": "Введите email.",
                "invalid": "Введите корректный email адрес.",
                "unique": "Пользователь с таким email уже существует.",
            },
        }

    error_messages = {
        "password_mismatch": "Введённые пароли не совпадают.",
    }
    
    def clean_username(self):
        """Валидация имени пользователя на запрещенные слова"""
        username = self.cleaned_data.get('username')
        if username:
            validate_content(username, 'Имя пользователя')
        return username
    
    def clean_email(self):
        """Валидация email на уникальность"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        # project_links приходит как JSON строка из скрытого поля
        project_links_json = self.data.get('project_links_json', '[]')
        try:
            project_links = json.loads(project_links_json)
            project_links = [link.strip() for link in project_links if link.strip()]
        except:
            project_links = []
        
        if role == 'author' and not project_links:
            raise forms.ValidationError('Для регистрации автора необходимо указать хотя бы одну ссылку на проекты.')
        
        if len(project_links) > 3:
            raise forms.ValidationError('Максимум 3 ссылки на проекты.')
        
        # Валидация URL
        validator = URLValidator()
        for link in project_links:
            try:
                validator(link)
            except DjangoValidationError:
                raise forms.ValidationError(f'Некорректная ссылка: {link}')
        
        cleaned_data['project_links'] = project_links
        return cleaned_data
    
    def save(self, commit=True):
        """Сохраняет пользователя с email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Неверные имя пользователя или пароль.",
        "inactive": "Аккаунт не активирован.",
    }
    
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted',
            'placeholder': 'Введите пароль'
        }),
    )


class ProfileEditForm(forms.ModelForm):
    def clean_bio(self):
        """Валидация описания профиля на запрещенные слова"""
        bio = self.cleaned_data.get('bio')
        if bio:
            validate_content(bio, 'Описание профиля')
        return bio
    
    class Meta:
        model = Profile
        fields = ['bio', 'avatar_file']
        labels = {
            'bio': 'О себе',
            'avatar_file': 'Аватар',
        }
        help_texts = {
            'avatar_file': 'Загрузите аватар с вашего компьютера (не обязательно)',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink placeholder-inkMuted resize-none',
                'rows': 6,
                'placeholder': 'Расскажите о себе...'
            }),
            'avatar_file': forms.FileInput(attrs={
                'class': 'w-full rounded-btn bg-bgElevated border border-border px-3 py-3 text-ink file:mr-4 file:py-2 file:px-4 file:rounded-btn file:border-0 file:text-sm file:font-semibold file:bg-accent-blue/20 file:text-accent-blue hover:file:bg-accent-blue/30 file:cursor-pointer',
                'accept': 'image/*'
            }),
        }

