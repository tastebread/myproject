from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
class MazeQuestion(models.Model):
    ### 난이도 선택
    DIFFICULTY_CHOICES = [
        ("easy", "쉬움"),
        ("normal", "보통"),
        ("hard", "어려움"),
        #필요하면 추가 유형을 넣을 수 있음
    ]
    ### 문제 기본 정보
    question_text = HTMLField()  # 문제 내용
    story_text = models.TextField(blank=True, null=True) #문제를 풀기 전 상황 설명
    image = models.ImageField(upload_to='maze_images/', blank=True, null=True) #문제에 포함될 이미지
    answer = models.CharField(max_length=100)  # 정답
    accepted_answers = models.TextField(
        "허용 정답 (쉼표로 구분)",
        blank=True,
        help_text="여러 정답이 허용될 경우 쉼표로 구분"
    )
    hint = models.TextField(blank=True, null=True)  # 힌트

    ### 게임 속성
    order = models.IntegerField()  # 문제 순서
    level = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default="easy") # 난이도
    time_limit = models.PositiveIntegerField(default=60) # 제한 시간 (초 단위)
    score_value = models.PositiveIntegerField(default=10) # 기본 점수
    hint_available = models.BooleanField(default=True) #힌트 사용 가능 여부

    ### 문제 연결 (스토리 미궁 지원)
    next_question = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="next_step") # 다음 문제 연결
    
    ### 모델 설정
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order','level'], name='unique_maze_question_order')
        ]

    ### 메서드
    def __str__(self):
        return f"[{self.get_level_display()}] 문제 {self.order}: {self.question_text[:30]}..."
    
    def check_answer(self, user_answer):
        """사용자가 입력한 정답이 맞는지 체크"""
        return self.answer.strip().lower() == user_answer.strip().casefold() #국제화 대응
    
    ### 문제 유형 속성
    @property
    def is_puzzle(self):
        return self.level == 'puzzle'
    
    @property
    def is_multiple_choice(self):
        return self.level == 'mc'
    
from django.contrib.auth.models import User
from django.db import models

### 미궁 게임 진행 저장
class MazeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 게임을 플레이하는 사용자
    current_question = models.ForeignKey(MazeQuestion, on_delete=models.PROTECT, null=True)  # 현재 진행 중인 문제
    score = models.IntegerField(default=0)  # 현재 점수
    completed = models.BooleanField(default=False)  # 게임 클리어 여부

    def __str__(self):
        return f"{self.user.username} - {self.current_question} (점수: {self.score})"
    
###점수 저장 (Leaderboard)
class Leaderboard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score','date'] #높은 순으로 정렬

    def __str__(self):
        return f"{self.user.username} -> {self.score}점"