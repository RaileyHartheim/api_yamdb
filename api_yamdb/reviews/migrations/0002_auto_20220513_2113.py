# Generated by Django 2.2.16 on 2022-05-13 18:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Оценка'),
        ),
    ]
