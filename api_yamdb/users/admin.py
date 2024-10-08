from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Административная панель пользователей."""
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )
    search_fields = ('username', 'email')
    list_display_links = ('username',)


admin.site.register(User, UserAdmin)
