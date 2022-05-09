from django.db import models
from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator

User = get_user_model()

class reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,  verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
        )
    text = models.TextField(
        max_length=255, verbose_name='Отзыв'
        )
    score = models.IntegerField(
        validators=[MaxValueValidator(10)], verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )

class comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_author', verbose_name='Автор')
    rewiew = models.ForeignKey(
        reviews, on_delete=models.CASCADE, related_name='comment', blank=True)
    text = models.TextField(max_length=255, verbose_name='Коментарий')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
