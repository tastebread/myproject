from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm

# Create your views here.

#글 목록
def post_list(request):
    posts = Post.objects.all().order_by('-created_at') #최신 글 순 정렬
    return render(request, 'board/post_list.html', {'posts':posts})

#글 상세 조회
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm() #댓글폼 추가
    return render(request, 'board/post_detail.html', {'post': post, 'comment_form': comment_form})

#글 작성 (아이디로그인후 가능)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user #현재 로그인한 사용자를 작성자로 설정
            post.save()
            return redirect('post_list') # 글 목록으로 이동
    else:
        form = PostForm()
    
    return render(request, 'board/post_form.html', {'form' : form})

#게시글 수정 (작성자만 가능))
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id) # 수정할 게시글 가져오기 (없으면 404 에러 발생)

    #작성자 본인만 수정 가능하도록 제한
    if post.author != request.user: # 작성자가 아니면 수정 불가 (보안강화)
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post) # instance=post 기존 데이터를 폼에 채워서 수정할 수 있도록 설정
    
    return render(request, 'board/post_form.html', { 'form': form, 'is_edit': True})

#게시글 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    #작성자만 삭제 가능하도록 제한
    if post.author != request.user:
        return redirect('post_list')
    
    if request.method == 'POST': # 삭제 확인 후 실행
        post.delete()
        return redirect('post_list')
    
    return render(request, 'board/post_confirm_delete.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id) # 해당 게시글 가져오는부분

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post # 어떤 게시글에 달리는 댓글인지 설정
            comment.author = request.user # 현재 로그인한 사용자 설정
            comment.save()
            return redirect('post_detail', post_id=post.id) # 댓글 작성 후 게시글 상세 페이지로 이동
    return redirect('post_detail', post_id=post.id)
