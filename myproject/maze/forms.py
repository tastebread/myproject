from django import forms
from .models import MazeQuestion

class MazeQuestionForm(forms.ModelForm):
    order = forms.IntegerField(
        min_value=1, 
        label="문제 순서", 
        help_text="문제 순서를 입력하세요 (1부터 시작)"
    )
    
    class Meta:
        model = MazeQuestion
        fields = ['question_text', 'answer','accepted_answers' ,'level','image', 'time_limit', 'hint', 'hint_available', 'order']
        labels = {
            'question_text': '문제 내용',
            'answer': '정답',
            'accepted_answers' : '허용되는 정답 목록',
            'level': '난이도',
            'time_limit': '제한 시간(초)',
            'hint': '힌트 내용',
            'hint_available': '힌트 제공 여부',
            'order': '문제 순서'
        }