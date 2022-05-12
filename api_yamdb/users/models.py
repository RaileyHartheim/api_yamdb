from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,
        max_length=254,
        blank=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True, blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        max_length=500,
        blank=True
    )
    role = models.TextField(
        verbose_name='Роль',
        choices=USER_ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=50,
        blank=True
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
