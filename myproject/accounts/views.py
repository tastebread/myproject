from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

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