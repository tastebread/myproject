from django.contrib import admin
from .models import MazeQuestion
from tinymce.widgets import TinyMCE
from django.db import models

class MazeQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_text', 'level')
    list_filter = ('level',)
    search_fields = ('question_text','answer')
    ordering = ('order',)

    #tinymce 적용
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    fieldsets = (
        ("문제 정보", {"fields": ("question_text", "answer", "accepted_answers", "hint", "image")}),
        ("스토리 설정", {"fields": ("story_text", "next_question")}),
        ("기타 설정", {"fields": ("level", "order", "time_limit")}),
    )

admin.site.register(MazeQuestion,MazeQuestionAdmin)