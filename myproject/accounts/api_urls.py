from django.urls import path
from dj_rest_auth.registration.views import SocialLoginView
from .api_views import RegisterView, LoginView, UserListView, ProfileView
from .api_views import ChangePasswordView, PasswordResetRequestView,DeleteAccountView,LogoutView
from .api_views import PostLikeView
from .api_views import EmailVerificationView,VerifyEmailTokenView,NotificationListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/', ProfileView.as_view(), name='profile-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('post/<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('email-verify/', EmailVerificationView.as_view(), name='email-verify'),
    path('email-verify/<str:uidb64>/<str:token>/', VerifyEmailTokenView.as_view(), name='email-verify-token'),
    path('social-login/google/', SocialLoginView.as_view(), name='google-login'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]