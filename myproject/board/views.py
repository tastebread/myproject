from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Tag, Category
from .forms import PostForm
from .forms import CommentForm
from django.db.models import Q, Count # 여러 필드 검색, 댓글 개수 계산할 때 사용
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST

#글 목록
def post_list(request):
    query = request.GET.get('q')  # 검색어 가져오기
    tag_name = request.GET.get('tag') # 특정 태그로 필터링
    category_name = request.GET.get('category') # 카테고리 필터링
    sort_option = request.GET.get('sort', 'latest')  # 정렬 옵션 가져오기 (기본값: 최신순)

    posts = Post.objects.all()  # 모든 게시글 가져오기
    
    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name) # 태그 확인
        posts = posts.filter(tags=tag) #해당 태그가 포함된 게시글만 필터링

    if category_name:  # 선택한 카테고리가 있을 경우 필터링
        category = get_object_or_404(Category, name=category_name)
        posts = posts.filter(category=category)

    categories = Category.objects.all()  # 카테고리 목록 가져오기

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | #제목에 검색어 포함
            Q(content__icontains=query) | # 내용에 검색어 포함
            Q(author__username__icontains=query) # 작성자 이름에 검색어 포함
        )

    # 정렬 기능 추가
    if sort_option == 'latest':
        posts = posts.order_by('-created_at')  # 최신순
    elif sort_option == 'oldest':
        posts = posts.order_by('created_at')  # 오래된순
    elif sort_option == 'views':
        posts = posts.order_by('-views')  # 조회수 순
    
    # 페이지네이션 적용 (10개씩 표시)
    paginator = Paginator(posts, 10)  # 한 페이지에 10개 게시글 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'board/post_list.html', {
        'page_obj': page_obj,  # 템플릿에서 사용 가능하도록 전달
        'categories': Category.objects.all(),
        'query': query,
        'tag_name': tag_name,
        'sort_option': sort_option
    })

    #return render(request, 'board/post_list.html', {'posts': posts, 'categories': categories, 'query': query,'tag_name': tag_name, 'sort_option': sort_option})

#글 상세 조회
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #조회수 증가 로직 추가
    post.views += 1
    post.save()
    
    comment_form = CommentForm() #댓글폼 추가
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = post.bookmarks.filter(id=request.user.id).exists()
    
    related_posts = post.related_posts()

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'is_bookmarked': is_bookmarked,
        'related_posts': related_posts  #  템플릿에 추천 게시글 전달
    })

#글 작성 (아이디로그인후 가능)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user #현재 로그인한 사용자를 작성자로 설정

            if 'image' in request.FILES: #이미지 파일이 있는 경우만 저장!
                print(" DEBUG: 이미지 업로드 감지됨")
                post.image = request.FILES['image']
            else:
                print(" DEBUG: 이미지 파일이 없습니다.")
            
            post.save()
            return redirect('post_detail', post_id=post.id) # 글 목록으로 이동
        else:
            print(" DEBUG: 폼 오류 발생 ->", form.errors)  # 폼 에러 확인
    else:
        form = PostForm()
    
    return render(request, 'board/post_create.html', {'form' : form})

#게시글 수정 (작성자만 가능))
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id) # 수정할 게시글 가져오기 (없으면 404 에러 발생)

    #작성자 본인만 수정 가능하도록 제한
    if post.author != request.user: # 작성자가 아니면 수정 불가 (보안강화)
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post) # instance=post 기존 데이터를 폼에 채워서 수정할 수 있도록 설정
    
    return render(request, 'board/post_form.html', { 'form': form, 'is_edit': True})

#게시글 삭제
@login_required
@require_POST
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    #작성자만 삭제 가능하도록 제한
    if post.author != request.user:
        message.error(request, "삭제 권한이 없습니다.")
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

#댓글 수정 기능(작성자만 가능)
@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment,id=comment_id) # 수정할 댓글을 가져옴

    #댓글 작성자만 수정 가능
    if comment.author != request.user: # 작성자만 수정 가능하도록 제한
        return redirect('post_detail', post_id=comment.post.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id) # 수정 후 해당 게시글 상세 페이지로 이동
        
    else:
        form = CommentForm(instance=comment) #instance=comment -> 기존 댓글 내용을 폼에 채워서 수정 가능하게함

    return render(request, 'board/comment_form.html', {'form': form, 'comment':comment})

#댓글 삭제 기능
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment,id=comment_id)

    #댓글 작성자만 삭제 가능
    if comment.author != request.user:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('post_detail', post_id=comment.post.id)
    
    if request.method == 'POST': #삭제 확인 후 실행
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    
    return render(request, 'board/comment_confirm_delete.html', {'comment':comment})

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    liked = not post.likes.filter(id=user.id).exists()
    if liked:
        post.likes.add(user)
    else:
        post.likes.remove(user)
    
    return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})

@login_required
def bookmarked_posts(request):
    posts = request.user.bookmarked_posts.all()  # 🔹 현재 로그인한 사용자가 북마크한 게시글 가져오기
    return render(request, 'board/bookmarked_posts.html', {'posts': posts})

@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 북마크 추가/삭제 토글
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)  # 북마크 삭제
    else:
        post.bookmarks.add(request.user)  # 북마크 추가
    
    return redirect('post_detail', post_id=post.id)

