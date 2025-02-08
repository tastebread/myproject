from django import forms
from .models import Post,Tag, Category
from .models import Comment

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="카테고리 선택"
    )
    tags = forms.CharField(required=False, help_text="쉼표(,)로 구분해서 태그를 입력하세요.")
    class Meta:
        model = Post
        fields = ['title','content','image','tags','category']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'image' : '이미지',
            'tags'  :  '태그',
            'category' : '카테고리',
        }
    
    def save(self, commit=True):
        post = super().save(commit=False)
        tag_names = self.cleaned_data['tags'].split(',')  # 쉼표로 태그 분리
        tag_list = []

        for name in tag_names:
            name = name.strip()  # 공백 제거
            if name:
                tag, created = Tag.objects.get_or_create(name=name)  # 중복 방지
                tag_list.append(tag)

        if commit:
            post.save()
            post.tags.set(tag_list)  # ManyToMany 관계 설정
        return post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글 내용'
        }