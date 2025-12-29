from django.contrib import admin
from .models import Project, ProjectParticipant, ProjectFavorite, ProjectInvitation, Task, Comment, Notification


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'section', 'created_at', 'updated_at')
    list_filter = ('section', 'created_at')
    search_fields = ('title', 'description', 'tags', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(ProjectParticipant)
class ProjectParticipantAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'invited_by', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('project__title', 'user__username', 'invited_by__username')
    readonly_fields = ('joined_at',)
    date_hierarchy = 'joined_at'


@admin.register(ProjectFavorite)
class ProjectFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'project__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(ProjectInvitation)
class ProjectInvitationAdmin(admin.ModelAdmin):
    list_display = ('project', 'invited_user', 'invited_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'invited_user__username', 'invited_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'project__title', 'assignee__username', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новая задача
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'project', 'task', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'project__title', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('message', 'user__username', 'project__title', 'task__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_read',)

