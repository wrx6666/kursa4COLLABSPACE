"""
Context processors для проектов
"""
from .forms import ProjectSearchForm
from .models import Notification


def search_form(request):
    """Добавляет форму поиска в контекст всех шаблонов"""
    # Инициализируем форму с данными из GET запроса
    form = ProjectSearchForm(request.GET if request.method == 'GET' else None)
    
    # Обновляем стили поля поиска для header
    form.fields['search'].widget.attrs.update({
        'class': 'flex-1 bg-transparent outline-none text-ink placeholder-inkMuted text-sm',
        'placeholder': 'Поиск...'
    })
    
    # Проверяем, есть ли активные фильтры
    has_active_filters = False
    if request.method == 'GET':
        has_active_filters = bool(
            request.GET.getlist('tags') or request.GET.get('section')
        )
    
    # Получаем количество непрочитанных уведомлений
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return {
        'search_form': form,
        'has_active_filters': has_active_filters,
        'unread_notifications_count': unread_notifications_count
    }

