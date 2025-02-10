from django.contrib import admin
from .models import MazeQuestion

@admin.register(MazeQuestion)
class MazeQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_text', 'difficulty', 'time_limit')
    ordering = ('order',)