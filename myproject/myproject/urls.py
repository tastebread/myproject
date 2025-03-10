from django.contrib import admin
from django.urls import path,include #include 추가
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf.urls.static import static
from accounts.views import home

schema_view = get_schema_view(
    openapi.Info(
        title="MyProject API",
        default_version='v1',
        description="Django API with JWT Authentication",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #JWT 인증 API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/accounts/', include('accounts.api_urls')),  # 회원 관련 URL
    
    # Swagger 문서 (API 테스트 가능)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('board/', include('board.urls')),  # 게시판 URL 추가!
    path('maze/', include("maze.urls")), #미궁게임 URL 추가
    path('tinymce/', include('tinymce.urls')),
    path('',include('board.urls')),  # 기본 URL을 board 뷰에 연결
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)