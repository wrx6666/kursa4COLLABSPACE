from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'verified', 'created_at')
    list_filter = ('role', 'verified')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'role', 'verified')
        }),
        ('Профиль', {
            'fields': ('bio', 'avatar_url', 'project_links')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['verify_authors', 'unverify_authors']
    
    def verify_authors(self, request, queryset):
        """Подтвердить выбранных авторов"""
        updated = queryset.filter(role='author').update(verified=True)
        self.message_user(request, f'{updated} авторов подтверждено.')
    verify_authors.short_description = 'Подтвердить авторов'
    
    def unverify_authors(self, request, queryset):
        """Снять подтверждение с выбранных авторов"""
        updated = queryset.filter(role='author').update(verified=False)
        self.message_user(request, f'Подтверждение снято с {updated} авторов.')
    unverify_authors.short_description = 'Снять подтверждение'
