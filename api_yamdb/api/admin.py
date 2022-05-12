from django.contrib import admin
from reviews.models import Category, Comments, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(Review)
admin.site.register(Comments)
