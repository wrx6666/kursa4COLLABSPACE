from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from accounts.models import Profile
from .forms import ProjectForm, InviteParticipantForm, TaskForm, ProjectSearchForm, CommentForm
from .models import Project, ProjectParticipant, ProjectFavorite, ProjectInvitation, Task, Comment, Notification, create_notification


def home(request):
    """Главная страница с поиском и фильтрацией проектов"""
    projects = Project.objects.all().select_related('owner').order_by('-created_at')
    
    # Инициализируем форму с данными из GET запроса (форма для обработки)
    form = ProjectSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search', '').strip()
        selected_tags = form.cleaned_data.get('tags', [])
        selected_section = form.cleaned_data.get('section', '')
        
        # Фильтрация по поисковому запросу (название)
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        
        # Фильтрация по тегам
        if selected_tags:
            # Проекты должны содержать хотя бы один из выбранных тегов
            # Теги хранятся как строка через запятую, поэтому ищем точное совпадение
            tag_filter = Q()
            for tag in selected_tags:
                # Ищем тег как отдельное слово (с запятыми или в начале/конце строки)
                tag_filter |= Q(tags__icontains=tag)
            projects = projects.filter(tag_filter).distinct()
        
        # Фильтрация по разделу
        if selected_section:
            projects = projects.filter(section=selected_section)
    
    # ТОП-15 проектов по количеству лайков за сутки
    yesterday = timezone.now() - timedelta(days=1)
    top_projects_qs = Project.objects.annotate(
        favorites_count=Count('favorited_by', filter=Q(favorited_by__created_at__gte=yesterday))
    ).filter(
        favorites_count__gt=0
    ).order_by('-favorites_count', '-created_at')[:15]
    
    # Преобразуем в список, чтобы получить все элементы
    top_projects_list = list(top_projects_qs)
    top_projects_pks = [p.pk for p in top_projects_list]
    
    # Если TOP-15 не хватает, добавляем проекты по общему количеству лайков
    if len(top_projects_list) < 15:
        remaining = 15 - len(top_projects_list)
        if top_projects_pks:
            # Используем список PK вместо подзапроса
            additional = Project.objects.annotate(
                total_favorites=Count('favorited_by')
            ).exclude(
                pk__in=top_projects_pks
            ).filter(total_favorites__gt=0).order_by('-total_favorites', '-created_at')[:remaining]
        else:
            # Если нет проектов с лайками за сутки, берем по общему количеству
            additional = Project.objects.annotate(
                total_favorites=Count('favorited_by')
            ).filter(total_favorites__gt=0).order_by('-total_favorites', '-created_at')[:remaining]
        top_projects_list = top_projects_list + list(additional)
    
    top_projects = top_projects_list
    
    # Новые проекты (последние 20)
    new_projects = Project.objects.all().select_related('owner', 'owner__profile').order_by('-created_at')[:20]
    
    # Новые авторы (зарегистрировались меньше 30 дней назад)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_authors = User.objects.filter(
        profile__role='author',
        date_joined__gte=thirty_days_ago
    ).select_related('profile')
    new_author_projects = Project.objects.filter(
        owner__in=new_authors
    ).select_related('owner', 'owner__profile').order_by('-created_at')[:20]
    
    return render(request, 'home.html', {
        'projects': projects,
        'top_projects': top_projects,
        'new_projects': new_projects,
        'new_author_projects': new_author_projects
    })


@login_required
def create_project(request):
    """Создание проекта (только для верифицированных авторов)"""
    # Проверяем, что пользователь - автор
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.role != 'author' and profile.role != 'admin':
            messages.error(request, 'Только авторы могут создавать проекты.')
            return redirect('home')
    
    # Проверяем, что автор верифицирован (для авторов, админы могут создавать без верификации)
    if profile.role == 'author' and not profile.verified:
        messages.warning(request, 'Вы не можете создавать проекты, пока ваш аккаунт автора не будет верифицирован администратором.')
        return redirect('home')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            
            # Обработка изображения перед сохранением
            if 'image_file' in request.FILES and request.FILES['image_file']:
                image_file = request.FILES['image_file']
                
                # Открываем изображение
                img = Image.open(image_file)
                
                # Целевой размер: 800x800 (квадратный формат)
                target_size = 800
                
                # Получаем текущие размеры
                img_width, img_height = img.size
                
                # Вычисляем новые размеры с сохранением пропорций
                if img_width > img_height:
                    # Горизонтальное изображение - подгоняем по высоте
                    new_height = target_size
                    new_width = int(img_width * (target_size / img_height))
                else:
                    # Вертикальное или квадратное - подгоняем по ширине
                    new_width = target_size
                    new_height = int(img_height * (target_size / img_width))
                
                # Изменяем размер с сохранением пропорций (высокое качество)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Конвертируем в RGBA если нужно (для работы с прозрачностью)
                if img.mode == 'P':
                    img = img.convert('RGBA')
                elif img.mode not in ('RGBA', 'LA', 'RGB'):
                    img = img.convert('RGB')
                
                # Создаем квадратное изображение с темным фоном
                # Если изображение не квадратное, добавляем padding
                if new_width != target_size or new_height != target_size:
                    # Создаем новое квадратное изображение с темным фоном
                    if img.mode in ('RGBA', 'LA'):
                        # Для изображений с прозрачностью - конвертируем в RGB с темным фоном
                        square_img = Image.new('RGB', (target_size, target_size), (11, 13, 19))  # #0b0d13
                        # Центрируем изображение
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                        # Создаем временное RGB изображение для вставки
                        if img.mode == 'LA':
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1])
                        else:
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        square_img.paste(rgb_img, (x_offset, y_offset))
                        img = square_img
                    else:
                        # Для RGB используем темный фон
                        square_img = Image.new('RGB', (target_size, target_size), (11, 13, 19))  # #0b0d13
                        # Центрируем изображение
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                        square_img.paste(img, (x_offset, y_offset))
                        img = square_img
                else:
                    # Изображение уже квадратное, но может быть с прозрачностью
                    if img.mode in ('RGBA', 'LA'):
                        # Конвертируем в RGB с темным фоном
                        background = Image.new('RGB', img.size, (11, 13, 19))
                        if img.mode == 'LA':
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1])
                            background.paste(rgb_img)
                        else:
                            background.paste(img, mask=img.split()[-1])
                        img = background
                
                # Сохраняем в BytesIO
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=95, optimize=True)
                img_io.seek(0)
                
                # Создаем новое имя файла
                file_name = image_file.name
                if '.' in file_name:
                    name, ext = file_name.rsplit('.', 1)
                    file_name = f"{name}_processed.jpg"
                else:
                    file_name = f"{file_name}_processed.jpg"
                
                # Сохраняем обработанное изображение
                project.image_file.save(
                    file_name,
                    ContentFile(img_io.read()),
                    save=False
                )
            
            # Обрабатываем теги - преобразуем список в строку через запятую
            tags = form.cleaned_data.get('tags', [])
            if tags:
                project.tags = ', '.join(tags)
            else:
                project.tags = ''
            
            project.save()  # Сохраняем проект
            
            # Сохраняем URL в image_url
            if project.image_file:
                project.image_url = request.build_absolute_uri(project.image_file.url)
                project.save(update_fields=['image_url'])
            
            messages.success(request, f'Проект "{project.title}" успешно создан!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/create_project.html', {'form': form})


def project_detail(request, pk):
    """Детальная страница проекта"""
    project = get_object_or_404(Project, pk=pk)
    participants = project.get_participants()
    
    # Проверки для авторизованных пользователей
    if request.user.is_authenticated:
        is_owner = project.owner == request.user
        is_participant = project.is_participant(request.user)
        can_edit = is_owner or is_participant
        is_favorite = ProjectFavorite.objects.filter(user=request.user, project=project).exists()
    else:
        is_owner = False
        is_participant = False
        can_edit = False
        is_favorite = False
    
    # Получаем задачи проекта с комментариями
    tasks = Task.objects.filter(project=project).select_related('assignee', 'created_by').prefetch_related('comments__author', 'comments__author__profile').order_by('-created_at')
    
    # Получаем комментарии к проекту (только к проекту, без ответов)
    comments = Comment.objects.filter(project=project, parent__isnull=True).select_related('author', 'author__profile').prefetch_related('replies__author', 'replies__author__profile').order_by('-created_at')
    
    # Форма для комментариев (только для авторизованных)
    comment_form = CommentForm(project=project) if request.user.is_authenticated else None
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'participants': participants,
        'is_owner': is_owner,
        'can_edit': can_edit,
        'is_favorite': is_favorite,
        'tasks': tasks,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def toggle_favorite(request, pk):
    """Добавление/удаление проекта в избранное"""
    project = get_object_or_404(Project, pk=pk)
    
    favorite, created = ProjectFavorite.objects.get_or_create(
        user=request.user,
        project=project
    )
    
    if created:
        messages.success(request, f'Проект "{project.title}" добавлен в понравившиеся!')
        is_favorite = True
    else:
        favorite.delete()
        messages.success(request, f'Проект "{project.title}" удален из понравившихся.')
        is_favorite = False
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})
    
    return redirect('project_detail', pk=project.pk)


@login_required
def edit_project(request, pk):
    """Редактирование проекта (владелец и участники)"""
    project = get_object_or_404(Project, pk=pk)
    
    # Проверяем права доступа: владелец или участник
    is_owner = project.owner == request.user
    is_participant = project.is_participant(request.user)
    
    if not (is_owner or is_participant):
        messages.error(request, 'У вас нет прав для редактирования этого проекта.')
        return redirect('project_detail', pk=project.pk)
    
    participants = project.get_participants()
    invite_form = InviteParticipantForm()
    # Получаем отправленные приглашения
    sent_invitations = ProjectInvitation.objects.filter(
        project=project,
        invited_by=request.user,
        status='pending'
    ).select_related('invited_user').order_by('-created_at')
    
    # Обработка приглашения участника (только для владельца)
    if is_owner and request.method == 'POST' and 'invite_participant' in request.POST:
        invite_form = InviteParticipantForm(request.POST)
        if invite_form.is_valid():
            username = invite_form.cleaned_data['username']
            try:
                user_to_invite = User.objects.get(username=username)
                
                # Проверяем, что пользователь не владелец
                if user_to_invite == project.owner:
                    messages.error(request, 'Владелец проекта уже является участником.')
                # Проверяем, что пользователь еще не участник
                elif ProjectParticipant.objects.filter(project=project, user=user_to_invite).exists():
                    messages.error(request, 'Этот пользователь уже является участником проекта.')
                # Проверяем, что нет активного приглашения
                elif ProjectInvitation.objects.filter(project=project, invited_user=user_to_invite, status='pending').exists():
                    messages.error(request, 'Приглашение этому пользователю уже отправлено.')
                else:
                    # Создаем приглашение вместо сразу добавления в участники
                    invitation = ProjectInvitation.objects.create(
                        project=project,
                        invited_user=user_to_invite,
                        invited_by=request.user,
                        status='pending'
                    )
                    # Создаем уведомление для приглашенного пользователя
                    create_notification(
                        user=user_to_invite,
                        notification_type='invitation',
                        message=f'Вас пригласили в проект "{project.title}"',
                        project=project,
                        invitation=invitation
                    )
                    messages.success(request, f'Приглашение пользователю {username} успешно отправлено!')
                    return redirect('edit_project', pk=project.pk)
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден.')
        # Если форма невалидна, продолжаем отображение страницы редактирования
    
    if request.method == 'POST' and 'invite_participant' not in request.POST:
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            
            # Обработка нового изображения, если загружено
            if 'image_file' in request.FILES and request.FILES['image_file']:
                image_file = request.FILES['image_file']
                
                # Открываем изображение
                img = Image.open(image_file)
                
                # Целевой размер: 800x800 (квадратный формат)
                target_size = 800
                
                # Получаем текущие размеры
                img_width, img_height = img.size
                
                # Вычисляем новые размеры с сохранением пропорций
                if img_width > img_height:
                    # Горизонтальное изображение - подгоняем по высоте
                    new_height = target_size
                    new_width = int(img_width * (target_size / img_height))
                else:
                    # Вертикальное или квадратное - подгоняем по ширине
                    new_width = target_size
                    new_height = int(img_height * (target_size / img_width))
                
                # Изменяем размер с сохранением пропорций (высокое качество)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Конвертируем в RGBA если нужно (для работы с прозрачностью)
                if img.mode == 'P':
                    img = img.convert('RGBA')
                elif img.mode not in ('RGBA', 'LA', 'RGB'):
                    img = img.convert('RGB')
                
                # Создаем квадратное изображение с темным фоном
                # Если изображение не квадратное, добавляем padding
                if new_width != target_size or new_height != target_size:
                    # Создаем новое квадратное изображение с темным фоном
                    if img.mode in ('RGBA', 'LA'):
                        # Для изображений с прозрачностью - конвертируем в RGB с темным фоном
                        square_img = Image.new('RGB', (target_size, target_size), (11, 13, 19))  # #0b0d13
                        # Центрируем изображение
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                        # Создаем временное RGB изображение для вставки
                        if img.mode == 'LA':
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1])
                        else:
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        square_img.paste(rgb_img, (x_offset, y_offset))
                        img = square_img
                    else:
                        # Для RGB используем темный фон
                        square_img = Image.new('RGB', (target_size, target_size), (11, 13, 19))  # #0b0d13
                        # Центрируем изображение
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                        square_img.paste(img, (x_offset, y_offset))
                        img = square_img
                else:
                    # Изображение уже квадратное, но может быть с прозрачностью
                    if img.mode in ('RGBA', 'LA'):
                        # Конвертируем в RGB с темным фоном
                        background = Image.new('RGB', img.size, (11, 13, 19))
                        if img.mode == 'LA':
                            rgb_img = Image.new('RGB', img.size, (11, 13, 19))
                            rgb_img.paste(img, mask=img.split()[-1])
                            background.paste(rgb_img)
                        else:
                            background.paste(img, mask=img.split()[-1])
                        img = background
                
                # Сохраняем в BytesIO
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=95, optimize=True)
                img_io.seek(0)
                
                # Создаем новое имя файла
                file_name = image_file.name
                if '.' in file_name:
                    name, ext = file_name.rsplit('.', 1)
                    file_name = f"{name}_processed.jpg"
                else:
                    file_name = f"{file_name}_processed.jpg"
                
                # Сохраняем обработанное изображение
                project.image_file.save(
                    file_name,
                    ContentFile(img_io.read()),
                    save=False
                )
            
            # Обрабатываем теги - преобразуем список в строку через запятую
            tags = form.cleaned_data.get('tags', [])
            if tags:
                project.tags = ', '.join(tags)
            else:
                project.tags = ''
            
            project.save()
            
            # Сохраняем URL в image_url
            if project.image_file:
                project.image_url = request.build_absolute_uri(project.image_file.url)
                project.save(update_fields=['image_url'])
            
            messages.success(request, f'Проект "{project.title}" успешно обновлен!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {
        'form': form,
        'project': project,
        'is_owner': is_owner,
        'participants': participants,
        'invite_form': invite_form,
        'sent_invitations': sent_invitations if is_owner else []
    })


@login_required
def remove_participant(request, pk, participant_id):
    """Удаление участника из проекта (только владелец)"""
    project = get_object_or_404(Project, pk=pk)
    
    # Проверяем, что пользователь - владелец проекта
    if project.owner != request.user:
        messages.error(request, 'Только владелец проекта может удалять участников.')
        return redirect('project_detail', pk=project.pk)
    
    # Удаляем участника
    participant = get_object_or_404(ProjectParticipant, pk=participant_id, project=project)
    participant_username = participant.user.username
    participant.delete()
    
    messages.success(request, f'Участник {participant_username} удален из проекта.')
    return redirect('project_detail', pk=project.pk)


@login_required
def accept_invitation(request, invitation_id):
    """Принятие приглашения в проект"""
    invitation = get_object_or_404(ProjectInvitation, pk=invitation_id, invited_user=request.user)
    
    # Проверяем, что приглашение еще активно
    if not invitation.can_be_accepted():
        messages.error(request, 'Это приглашение уже обработано или отменено.')
        return redirect(reverse('profile') + '?tab=invitations')
    
    # Проверяем, что пользователь еще не участник
    if ProjectParticipant.objects.filter(project=invitation.project, user=request.user).exists():
        invitation.status = 'rejected'
        invitation.save()
        messages.error(request, 'Вы уже являетесь участником этого проекта.')
        return redirect(reverse('profile') + '?tab=invitations')
    
    # Создаем участника проекта
    ProjectParticipant.objects.create(
        project=invitation.project,
        user=request.user,
        invited_by=invitation.invited_by
    )
    
    # Обновляем статус приглашения
    invitation.status = 'accepted'
    invitation.save()
    
    messages.success(request, f'Вы успешно присоединились к проекту "{invitation.project.title}"!')
    return redirect(reverse('profile') + '?tab=invitations')


@login_required
def reject_invitation(request, invitation_id):
    """Отклонение приглашения в проект"""
    invitation = get_object_or_404(ProjectInvitation, pk=invitation_id, invited_user=request.user)
    
    # Проверяем, что приглашение еще активно
    if not invitation.can_be_accepted():
        messages.error(request, 'Это приглашение уже обработано или отменено.')
        return redirect(reverse('profile') + '?tab=invitations')
    
    # Обновляем статус приглашения
    invitation.status = 'rejected'
    invitation.save()
    
    messages.success(request, f'Вы отклонили приглашение в проект "{invitation.project.title}".')
    return redirect(reverse('profile') + '?tab=invitations')


@login_required
def cancel_invitation(request, invitation_id):
    """Отмена приглашения (только для автора проекта)"""
    invitation = get_object_or_404(ProjectInvitation, pk=invitation_id)
    
    # Проверяем, что пользователь - владелец проекта
    if invitation.project.owner != request.user:
        messages.error(request, 'Только владелец проекта может отменять приглашения.')
        return redirect('edit_project', pk=invitation.project.pk)
    
    # Проверяем, что приглашение еще активно
    if not invitation.can_be_cancelled():
        messages.error(request, 'Это приглашение уже обработано.')
        return redirect('edit_project', pk=invitation.project.pk)
    
    # Обновляем статус приглашения
    invitation.status = 'cancelled'
    invitation.save()
    
    messages.success(request, f'Приглашение пользователю {invitation.invited_user.username} отменено.')
    return redirect('edit_project', pk=invitation.project.pk)


@login_required
def create_task(request, project_pk):
    """Создание задачи в проекте"""
    project = get_object_or_404(Project, pk=project_pk)
    
    # Проверяем права доступа: владелец или участник
    is_owner = project.owner == request.user
    is_participant = project.is_participant(request.user)
    
    if not (is_owner or is_participant):
        messages.error(request, 'У вас нет прав для создания задач в этом проекте.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, f'Задача "{task.title}" успешно создана!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(project=project)
    
    return render(request, 'projects/create_task.html', {
        'form': form,
        'project': project
    })


@login_required
def edit_task(request, project_pk, task_pk):
    """Редактирование задачи"""
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(Task, pk=task_pk, project=project)
    
    # Проверяем права доступа: владелец или участник
    is_owner = project.owner == request.user
    is_participant = project.is_participant(request.user)
    
    if not (is_owner or is_participant):
        messages.error(request, 'У вас нет прав для редактирования задач в этом проекте.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            # Сохраняем старые значения для сравнения
            old_status = task.status
            old_assignee = task.assignee
            
            task = form.save()
            
            # Создаем уведомления при изменении задачи
            users_to_notify = []
            
            # Если изменился статус или другие поля - уведомляем исполнителя и автора задачи
            if task.status != old_status or task.assignee != old_assignee:
                if task.assignee and task.assignee != request.user:
                    users_to_notify.append(task.assignee)
                if task.created_by != request.user and task.created_by not in users_to_notify:
                    users_to_notify.append(task.created_by)
            
            # Если задача была назначена на нового исполнителя
            if task.assignee and task.assignee != old_assignee and task.assignee != request.user:
                create_notification(
                    user=task.assignee,
                    notification_type='task_assigned',
                    message=f'Вам назначена задача "{task.title}" в проекте "{project.title}"',
                    project=project,
                    task=task
                )
            
            # Уведомляем об изменении задачи
            for user in users_to_notify:
                if user != task.assignee or task.assignee == old_assignee:  # Чтобы не дублировать уведомление о назначении
                    create_notification(
                        user=user,
                        notification_type='task_changed',
                        message=f'Задача "{task.title}" в проекте "{project.title}" была изменена',
                        project=project,
                        task=task
                    )
            
            messages.success(request, f'Задача "{task.title}" успешно обновлена!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task, project=project)
    
    return render(request, 'projects/edit_task.html', {
        'form': form,
        'project': project,
        'task': task
    })


@login_required
def delete_task(request, project_pk, task_pk):
    """Удаление задачи"""
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(Task, pk=task_pk, project=project)
    
    # Проверяем права доступа: владелец или участник
    is_owner = project.owner == request.user
    is_participant = project.is_participant(request.user)
    
    if not (is_owner or is_participant):
        messages.error(request, 'У вас нет прав для удаления задач в этом проекте.')
        return redirect('project_detail', pk=project.pk)
    
    task_title = task.title
    task.delete()
    messages.success(request, f'Задача "{task_title}" успешно удалена!')
    return redirect('project_detail', pk=project.pk)


@login_required
def add_comment(request, pk):
    """Добавление комментария к проекту"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, project=project)
        if form.is_valid():
            try:
                comment = form.save(commit=True, author=request.user, project=project)
                # Создаем уведомление для автора проекта (если это не он сам комментирует)
                if project.owner != request.user:
                    create_notification(
                        user=project.owner,
                        notification_type='comment_project',
                        message=f'{request.user.username} оставил комментарий к вашему проекту "{project.title}"',
                        project=project,
                        comment=comment
                    )
                messages.success(request, 'Комментарий успешно добавлен!')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении комментария: {str(e)}')
        else:
            # Показываем конкретные ошибки формы
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            if error_messages:
                messages.error(request, 'Ошибка при добавлении комментария: ' + '; '.join(error_messages))
            else:
                messages.error(request, 'Ошибка при добавлении комментария. Проверьте форму.')
    else:
        messages.error(request, 'Неверный метод запроса.')
    
    return redirect('project_detail', pk=pk)


@login_required
def add_reply(request, pk, comment_id):
    """Добавление ответа на комментарий (только для автора проекта)"""
    project = get_object_or_404(Project, pk=pk)
    parent_comment = get_object_or_404(Comment, pk=comment_id, project=project)
    
    # Проверяем, что пользователь - автор проекта
    if project.owner != request.user:
        messages.error(request, 'Только автор проекта может отвечать на комментарии.')
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, project=project)
        if form.is_valid():
            try:
                reply = form.save(commit=True, author=request.user, project=project, parent=parent_comment)
                # Создаем уведомление для автора комментария, на который отвечают (если это не он сам)
                if parent_comment.author != request.user:
                    create_notification(
                        user=parent_comment.author,
                        notification_type='comment_project',
                        message=f'{request.user.username} ответил на ваш комментарий к проекту "{project.title}"',
                        project=project,
                        comment=reply
                    )
                messages.success(request, 'Ответ успешно добавлен!')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении ответа: {str(e)}')
        else:
            # Показываем конкретные ошибки формы
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            if error_messages:
                messages.error(request, 'Ошибка при добавлении ответа: ' + '; '.join(error_messages))
            else:
                messages.error(request, 'Ошибка при добавлении ответа. Проверьте форму.')
    else:
        messages.error(request, 'Неверный метод запроса.')
    
    return redirect('project_detail', pk=pk)


@login_required
def add_task_comment(request, project_pk, task_pk):
    """Добавление комментария к задаче"""
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(Task, pk=task_pk, project=project)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, task=task)
        if form.is_valid():
            try:
                comment = form.save(commit=True, author=request.user, task=task)
                # Создаем уведомления для автора задачи и исполнителя (если это не они сами комментируют)
                users_to_notify = []
                if task.created_by != request.user:
                    users_to_notify.append(task.created_by)
                if task.assignee and task.assignee != request.user and task.assignee not in users_to_notify:
                    users_to_notify.append(task.assignee)
                
                for user in users_to_notify:
                    create_notification(
                        user=user,
                        notification_type='comment_task',
                        message=f'{request.user.username} оставил комментарий к задаче "{task.title}" в проекте "{project.title}"',
                        project=project,
                        task=task,
                        comment=comment
                    )
                messages.success(request, 'Комментарий к задаче успешно добавлен!')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении комментария: {str(e)}')
        else:
            # Показываем конкретные ошибки формы
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            if error_messages:
                messages.error(request, 'Ошибка при добавлении комментария: ' + '; '.join(error_messages))
            else:
                messages.error(request, 'Ошибка при добавлении комментария. Проверьте форму.')
    else:
        messages.error(request, 'Неверный метод запроса.')
    
    return redirect('project_detail', pk=project_pk)


@login_required
def notifications(request):
    """Страница со всеми уведомлениями пользователя"""
    notifications_list = Notification.objects.filter(user=request.user).select_related(
        'project', 'task', 'invitation', 'comment', 'comment__author'
    ).order_by('-created_at')
    
    unread_count = notifications_list.filter(is_read=False).count()
    
    return render(request, 'projects/notifications.html', {
        'notifications': notifications_list,
        'unread_count': unread_count
    })


@login_required
def mark_notification_read(request, notification_id):
    """Отмечает уведомление как прочитанное"""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications')


@login_required
def mark_all_notifications_read(request):
    """Отмечает все уведомления как прочитанные"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications')


