from django.db import models

# Create your models here.

from django.contrib.auth.models import User

def post_file_path(instance, filename):
    """업로드된 파일을 저장할 경로 설정"""
    return f'uploads/posts/{instance.author.username}/{filename}'

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
    views = models.IntegerField(default=0) #조회수 필드 추가
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
        return Post.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()[:5]
    
    def popular_posts():
        """ 조회수 & 좋아요 수 기반 인기 게시글 추천 """
        return Post.objects.annotate(score=models.Count('likes') + models.F('views')).order_by('-score')[:5]
    
    def __str__(self):
        return self.title

#좋아요 모델 추가 (누가 어떤 게시글을 좋아요 했는지 저장)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','post') #같은 유저가 같은 게시글을 여러 번 좋아요 못하도록 설정
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