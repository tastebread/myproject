from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="아이디", required=True)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="이메일", required=True)
    birth_date = forms.DateField(
        label="생년월일",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )  # 생년월일 추가
    profile_image = forms.ImageField(label="프로필 사진", required=False)  # 프로필 사진 추가

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'birth_date', 'profile_image']
        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        error_messages = {
            'username': {
                'required': "아이디를 입력해주세요.",
                'unique': "이미 사용 중인 아이디입니다.",
            },
            'email': {
                'required': "이메일을 입력해주세요.",
                'invalid': "올바른 이메일 형식을 입력해주세요.",
            },
            'password1': {
                'required': "비밀번호를 입력해주세요.",
            },
            'password2': {
                'required': "비밀번호 확인을 입력해주세요.",
                'password_mismatch': "비밀번호가 일치하지 않습니다.",
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                birth_date=self.cleaned_data.get('birth_date'),  # 오타 수정 (birth_Date → birth_date)
                profile_image=self.cleaned_data.get('profile_image')
            )
            profile.save()
        return user