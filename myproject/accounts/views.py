from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Profile
from .forms import ProfileForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from board.models import Post, Comment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user) # 회원가입 후 자동 로그인
            #return redirect('/') # 회원 가입 후 홈으로 이동
            return redirect('profile') #홈 대신 프로필 페이지로 이동
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})

@login_required #로그인한 사용자만 접근 가능
def profile(request):
    return render(request,'accounts/profile.html')

@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)  # 유저가 있는지 확인

    profile, created = Profile.objects.get_or_create(user=user)  # 프로필이 없으면 자동 생성
    
    #사용자가 작성한 게시글 & 댓글 가져오기
    posts = Post.objects.filter(author=user).order_by('-created_at') #최신순 정렬
    comments = Comment.objects.filter(author=user).order_by('-created_at') # 최신순 정렬
    
    return render(request, 'accounts/profile.html', {'profile': profile, 'user': user})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)  #  URL 패턴에 맞게 수정
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form, 'user': request.user})

@csrf_exempt
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})