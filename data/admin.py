# Admin
from django.contrib import admin

# Models
from data.models import *


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'short_explanation')


class EditionAdmin(admin.ModelAdmin):
	list_display = ('date', 'total',)


class ScoreAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'comment')
	list_filter = ('edition', 'category', 'score')


admin.site.register(Edition, EditionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Score, ScoreAdmin)