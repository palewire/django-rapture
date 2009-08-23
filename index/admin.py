# Admin
from django.contrib import admin

# Models
from index.models import *


class CategoryAdmin(admin.ModelAdmin):
	pass


class EditionAdmin(admin.ModelAdmin):
	pass


class ScoreAdmin(admin.ModelAdmin):
	pass


admin.site.register(Edition, EditionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Score, ScoreAdmin)