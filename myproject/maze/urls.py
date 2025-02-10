from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_maze, name='start_maze_game'),  # 게임 시작
    path('question/', views.maze_question, name='maze_question'),  # 문제 페이지
    path('submit/', views.submit_answer, name='submit_answer'),  # 정답 제출
    path('complete/', views.maze_complete, name='maze_complete'),  # 게임 완료
]