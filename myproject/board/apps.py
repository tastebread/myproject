from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'
    verbose_name = "게시판 관리" # 관리자 페이지 이름 변경
