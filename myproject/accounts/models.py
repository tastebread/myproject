from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # User와 1대1 관계
    birth_date = models.DateField(null=True, blank=True) #생년월일
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True,verbose_name="자기소개") #프로필 사진
    bio = models.TextField(blank=True, null=True) #자기소개 추가

    #게임 관련 데이터 추가
    highest_score = models.IntegerField(default=0)  # 최고 점수 저장
    games_played = models.IntegerField(default=0)  # 총 플레이 횟수 저장
    last_played = models.DateTimeField(auto_now=True)  # 마지막으로 플레이한 날짜 저장

    class Meta:
        verbose_name = "프로필"
        verbose_name_plural = "프로필들"
        ordering = ['user']
        
    def __str__(self):
        return f"{self.user.username}의 프로필 " # 관리 페이지에서 보기 쉽게 표시
