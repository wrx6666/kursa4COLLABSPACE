import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from projects.models import Project, ProjectParticipant, ProjectFavorite, ProjectInvitation

from .forms import SignupForm, LoginForm, ProfileEditForm
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаём профиль с ролью и ссылками на проекты
            role = form.cleaned_data.get('role', 'user')
            project_links = form.cleaned_data.get('project_links', [])
            Profile.objects.create(
                user=user,
                role=role,
                project_links=json.dumps(project_links) if project_links else None,
                verified=False  # Авторы по умолчанию не верифицированы
            )
            login(request, user)
            messages.success(request, "Аккаунт успешно создан!")
            return redirect("profile")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Получаем активную вкладку из GET параметра
    active_tab = request.GET.get('tab', 'info')
    
    # Получаем проекты пользователя (где он владелец)
    my_projects = Project.objects.filter(owner=request.user).order_by('-created_at')
    
    # Получаем проекты, где пользователь участник
    participant_projects = Project.objects.filter(
        participants__user=request.user
    ).exclude(owner=request.user).distinct().order_by('-created_at')
    
    # Получаем понравившиеся проекты
    favorite_projects = Project.objects.filter(
        favorited_by__user=request.user
    ).order_by('-favorited_by__created_at')
    
    # Получаем приглашения в проекты
    pending_invitations = ProjectInvitation.objects.filter(
        invited_user=request.user,
        status='pending'
    ).select_related('project', 'invited_by', 'project__owner').order_by('-created_at')
    
    # Вычисляем общее количество проектов
    total_projects_count = my_projects.count() + participant_projects.count()
    
    return render(request, "accounts/profile.html", {
        "user": request.user,
        "profile": profile,
        "active_tab": active_tab,
        "my_projects": my_projects,
        "participant_projects": participant_projects,
        "favorite_projects": favorite_projects,
        "pending_invitations": pending_invitations,
        "total_projects_count": total_projects_count
    })

@login_required
def profile_edit_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            # Если загружено изображение, сохраняем URL в avatar_url
            if profile.avatar_file:
                profile.avatar_url = request.build_absolute_uri(profile.avatar_file.url)
                profile.save(update_fields=['avatar_url'])
            
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=profile)
    
    return render(request, "accounts/profile_edit.html", {
        "form": form,
        "profile": profile
    })