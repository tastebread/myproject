from django.db import models

class MazeQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "쉬움"),
        ("normal", "보통"),
        ("hard", "어려움"),
    ]
    question_text = models.TextField()  # 문제 내용
    answer = models.CharField(max_length=100)  # 정답
    hint = models.TextField(blank=True, null=True)  # 힌트
    order = models.IntegerField(unique=True)  # 문제 순서
    level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="easy") #난이도추가
    time_limit = models.IntegerField(default=60) # 제한 시간 (초 단위)
    score_value = models.IntegerField(default=10) # 기본 점수 (맞힐 경우)
    hint_available = models.BooleanField(default=True) #힌트 사용 가능 여부

    def __str__(self):
        return f"[{self.get_level_display()}] 문제 {self.order}: {self.question_text[:30]}..."
    
    def check_answer(self, user_answer):
        """사용자가 입력한 정답이 맞는지 체크"""
        return self.answer.strip().lower() == user_answer.strip().lower()
    
from django.contrib.auth.models import User
from django.db import models

class MazeProgress(models.Model):
    """사용자의 미궁 게임 진행 상황 저장"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 어떤 유저가 진행 중인지
    current_question = models.ForeignKey(MazeQuestion, on_delete=models.SET_NULL, null=True)  # 현재 진행 중인 문제
    score = models.IntegerField(default=0)  # 현재 점수
    completed = models.BooleanField(default=False)  # 게임 클리어 여부

    def __str__(self):
        return f"{self.user.username} - {self.current_question} (점수: {self.score})"