from django.contrib import admin
from .models import MazeQuestion
from tinymce.widgets import TinyMCE
from django.db import models

class MazeQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_text', 'level', 'time_limit','hint_available')
    list_filter = ('level',)
    search_fields = ('question_text','answer')
    ordering = ('order',)

    #tinymce 적용
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
admin.site.register(MazeQuestion,MazeQuestionAdmin)