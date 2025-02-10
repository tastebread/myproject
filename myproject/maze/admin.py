from django.contrib import admin
from .models import MazeQuestion


class MazeQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_text', 'level', 'time_limit','hint_available')
    list_filter = ('level',)
    search_fields = ('question_text','answer')
    ordering = ('order',)
admin.site.register(MazeQuestion,MazeQuestionAdmin)