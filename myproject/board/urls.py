from django.urls import path
from .views import post_list, post_detail, post_create, add_comment, comment_edit,comment_delete
from .views import post_edit,post_delete,post_like
urlpatterns = [
    path('', post_list, name='post_list'), #글 목록
    path('<int:post_id>/', post_detail, name='post_detail'), #글 상세 조회
    path('new/',post_create, name='post_create'), #글 작성
    path('<int:post_id>/edit/', post_edit, name='post_edit'), #게시글 수정
    path('<int:post_id>/delete/', post_delete, name='post_delete'),
    path('<int:post_id>/comment/', add_comment, name='add_comment'), #댓글 url
    path('comment/<int:comment_id>/edit/', comment_edit,name='comment_edit'), #댓글 수정 URL 추가
    path('comment/<int:comment_id>/delete/', comment_delete, name='comment_delete'), #댓글 삭제 URL
    path('post/<int:post_id>/like', post_like, name='post_like'), #좋아요 기능

]

