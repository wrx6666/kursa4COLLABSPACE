from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('<int:pk>/remove-participant/<int:participant_id>/', views.remove_participant, name='remove_participant'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('invitations/<int:invitation_id>/accept/', views.accept_invitation, name='accept_invitation'),
    path('invitations/<int:invitation_id>/reject/', views.reject_invitation, name='reject_invitation'),
    path('invitations/<int:invitation_id>/cancel/', views.cancel_invitation, name='cancel_invitation'),
    # Задачи
    path('<int:project_pk>/tasks/create/', views.create_task, name='create_task'),
    path('<int:project_pk>/tasks/<int:task_pk>/edit/', views.edit_task, name='edit_task'),
    path('<int:project_pk>/tasks/<int:task_pk>/delete/', views.delete_task, name='delete_task'),
    # Комментарии
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('<int:project_pk>/tasks/<int:task_pk>/comment/', views.add_task_comment, name='add_task_comment'),
    # Уведомления
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]

