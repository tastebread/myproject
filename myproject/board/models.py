from django.db import models
import uuid
import os

from django.contrib.auth.models import User

def post_file_path(instance, filename):
    """업로드된 파일을 저장할 경로 설정(UUID를 사용하여 중복 방지)"""
    ext = filename.split('.')[-1] # 확장자 가져오기
    new_filename = f"{uuid.uuid4()}.{ext}" # UUID로 새로운 파일명 생성
    return os.path.join('uploads/posts', instance.author.username, new_filename)

#카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) # 카테고리 이름

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) # 태그 이름 중복 방지

    def __str__(self):
        return self.name

#게시글 모델
class Post(models.Model):
    title = models.CharField(max_length=200) #글내용
    content = models.TextField() # 글제목
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    created_at = models.DateTimeField(auto_now_add=True) #작성 시간
    updated_at = models.DateTimeField(auto_now=True) # 수정 시간
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) #이미지 필드 추가
    views = models.PositiveIntegerField(default=0) #조회수 필드 추가
    tags = models.ManyToManyField(Tag, blank=True) # 태그 (다대다 관계)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts') # 카테고리 추가


    #파일 업로드 필드 추가
    attached_file = models.FileField(upload_to=post_file_path, blank=True, null=True)
    #북마크 기능 추가
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_posts", blank=True)
    #좋아요 수 추가
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def related_posts(self):
        """ 태그가 겹치는 게시글 추천 """
        tag_ids = self.tags.values_list('id', flat=True)
        return Post.objects.filter(tags__in=tag_ids).exclude(id=self.id).distinct().select_related('author','category')[:5]
    
    @classmethod
    def popular_posts(cls):
        """ 조회수 & 좋아요 수 기반 인기 게시글 추천 """
        return cls.objects.annotate(
            score=models.Count('likes', distinct=True) + models.F('views')
        ).order_by('-score')[:5]
    
    def __str__(self):
        return self.title

#좋아요 모델 추가 (누가 어떤 게시글을 좋아요 했는지 저장)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]
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
        content_preview = (self.content[:20] + "...") if len(self.content) > 20 else self.content
        return f"{self.author}: {content_preview}"