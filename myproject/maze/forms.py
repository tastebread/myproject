from django import forms
from .models import MazeQuestion

class MazeQuestionForm(forms.ModelForm):
    class Meta:
        model = MazeQuestion
        fields = ['question_text', 'answer', 'level', 'time_limit', 'hint', 'hint_available', 'order']
        labels = {
            'question_text': '문제 내용',
            'answer': '정답',
            'level': '난이도',
            'time_limit': '제한 시간(초)',
            'hint': '힌트 내용',
            'hint_available': '힌트 제공 여부',
            'order': '문제 순서'
        }