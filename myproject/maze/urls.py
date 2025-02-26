from django.urls import path
from . import views

urlpatterns = [
    path('select_difficulty/', views.select_difficulty, name='select_difficulty'), # 난이도 선택
    path('start/', views.start_maze, name='start_maze'),  # 게임 시작
    path('question/', views.maze_question, name='maze_question'),  # 문제 페이지
    path("submit/", views.submit_answer, name='submit_answer'),  # 정답 제출
    path("hint/", views.get_hint, name="get_hint"),  # 힌트 제공
    path('complete/', views.maze_complete, name='maze_complete'),  # 게임 완료
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # 문제 관리 관련
    path('questions/manage/', views.manage_maze_questions, name='manage_maze_questions'), # 문제 관리 페이지
    path('questions/add/', views.add_maze_question, name='add_maze_question'), # 문제 추가 페이지
    path('questions/edit/<int:pk>/', views.edit_maze_question, name='edit_maze_question'), # 문제 수정 페이지
    path('questions/delete/<int:pk>/', views.delete_maze_question, name='delete_maze_question'), # 문제 삭제 페이지
    path("questions/list/", views.question_list, name="question_list"), # 문제 리스트
]