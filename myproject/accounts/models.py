from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # User와 1대1 관계
    birth_date = models.DateField(null=True, blank=True) #생년월일
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True) #프로필 사진

    def __str__(self):
        return self.user.username # 관리 페이지에서 보기 쉽게 표시
