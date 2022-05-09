from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'role',
        'email',
        'bio',
        'confirmation_code',
    )
    search_fields = ('username',)
    list_filter = ('username', 'role',)
    empty_value_display = '-пусто-'
