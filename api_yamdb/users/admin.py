from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_editable = ('role',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'role',
                    'email',
                    'bio',
                ),
            },
        ),
        (
            'Дополнительно',
            {
                'fields': (
                    'password',
                    'last_login',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
