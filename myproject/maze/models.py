from django.db import models

class MazeQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', '쉬움'),
        ('normal', '보통'),
        ('hard', '어려움'),
    ]
    question_text = models.TextField()  # 문제 내용
    answer = models.CharField(max_length=100)  # 정답
    hint = models.TextField(blank=True, null=True)  # 힌트
    order = models.IntegerField(unique=True)  # 문제 순서
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='normal') #난이도추가
    time_limit = models.IntegerField(default=60) # 제한 시간 (초 단위)

    def __str__(self):
        return f"[{self.get_difficulty_display()}] 문제 {self.order}: {self.question_text[:30]}..."
    
    def check_answer(self, user_answer):
        """사용자가 입력한 정답이 맞는지 체크"""
        return self.answer.strip().lower() == user_answer.strip().lower()