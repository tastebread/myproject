from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200) #글 제목
    content = models.TextField() # 글 내용
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    created_at = models.DateTimeField(auto_now_add=True) #작성 시간
    updated_at = models.DateTimeField(auto_now=True) # 수정 시간

    def __str__(self):
        return self.title

class Comment(models.Model):
    #어떤 게시글(post)에 달린 댓글인지 연결
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # 댓글이 속한 게시글
    #댓글 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 작성자
    #댓글 내용 저장
    content = models.TextField() # 댓글 내용
    #작성 및 수정 시간 자동 기록
    created_at = models.DateTimeField(auto_now_add=True) # 작성시간
    updated_at = models.DateTimeField(auto_now=True) # 수정시간

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"