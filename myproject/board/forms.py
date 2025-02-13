from django import forms
from .models import Post,Tag, Category
from .models import Comment

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), #초기값 설정
        required=False,
        empty_label="카테고리 선택"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all() # 동적으로 할당
    
    tags = forms.CharField(required=False, help_text="쉼표(,)로 구분해서 태그를 입력하세요.", strip=True)
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
        tag_names = {name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()}  # 중복 제거

        existing_tags = Tag.objects.filter(name__in=tag_names)
        existing_tag_names = set(existing_tags.values_list('name', flat=True))
        
        tag_list = []

        new_tags = [Tag(name=name) for name in tag_names if name not in existing_tag_names]
        Tag.objects.bulk_create(new_tags)  # 새 태그 한 번에 추가

        all_tags = list(existing_tags) + new_tags  # 기존 + 새 태그 결합

        if commit:
            post.save()
            post.tags.set(all_tags)  # ManyToMany 관계 설정
        return post
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, strip=True)  # 공백 자동 제거
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글 내용'
        }