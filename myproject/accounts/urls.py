from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.views import (
    PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,PasswordResetCompleteView
)
from .views import signup,profile,profile_view,profile_edit
from accounts.views import home

urlpatterns = [
    path('signup/', signup,name='signup'), #회원가입 페이지
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('profile/', profile, name='profile'), #프로필 페이지 추가
    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    #비밀번호 재설정 요청 페이지
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    #비밀번호 재설정 요청 완료 페이지
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    #비밀번호 재설정 확인 페이지
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    #비밀번호 재설정 완료 페이지
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    #프로필 수정 페이지
    path('profile/edit/', profile_edit, name='profile_edit'), 
    #특정 유저의 프로필
    path('profile/<str:username>/', profile_view, name='profile_detail'),

]
