from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from .models import Notification
from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from board.models import Post
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# 회원가입 API
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "모든 필드를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "이미 사용 중인 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)

# 로그인 API (JWT 발급)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            return Response({"error": "로그인 실패. 아이디 또는 비밀번호를 확인하세요."}, status=status.HTTP_401_UNAUTHORIZED)

# 유저 목록 조회 API
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# 프로필 조회 및 수정 API
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    

#비밀 번호 변경 API
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.data)

        if form.is_valid():
            form.save()
            return Response({"message": "비밀번호 변경 성공!"}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
#비밀번호 재설정(이메일 링크 방식)
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            reset_link = f"http://127.0.0.1:8000/reset-password/{user.pk}/{token}/"
            send_mail(
                "비밀번호 재설정 요청",
                f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}",
                "admin@myproject.com",
                [email],
            )
            return Response({"message": "비밀번호 재설정 이메일이 전송되었습니다."})
        return Response({"error": "등록되지 않은 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

#회원 탈퇴 API
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 성공!"}, status=status.HTTP_200_OK)
    
#로그 아웃 API

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh 토큰을 블랙리스트 처리 (단, 설정 필요)
            return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "토큰이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return Response({"liked": liked, "total_likes": post.likes.count()})
    

#이메일 인증 API
class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"http://127.0.0.1:8000/verify-email/{uid}/{token}/"

            send_mail(
                "이메일 인증 요청",
                f"이메일 인증을 완료하려면 다음 링크를 클릭하세요: {verification_link}",
                "admin@myproject.com",
                [email],
            )

            return Response({"message": "이메일 인증 링크가 전송되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"error": "등록되지 않은 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=id)
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "이메일 인증 실패"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "이메일 인증 실패"}, status=status.HTTP_400_BAD_REQUEST)

#알람기능
class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')