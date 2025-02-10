from django.shortcuts import render, redirect, get_object_or_404
from .models import MazeQuestion
import random
from django.http import JsonResponse

# 게임 시작 (첫 번째 문제로 이동)
def start_maze(request):
    first_question = MazeQuestion.objects.order_by('order').first()
    if first_question:
        return redirect('maze_question')
    return render(request, 'maze/maze_complete.html')

def maze_question(request):
    """랜덤으로 미궁 문제를 출제"""
    questions = MazeQuestion.objects.all()
    
    if not questions.exists():
        return redirect('maze_complete')  # 문제가 없으면 클리어 화면으로 이동

    question = random.choice(questions)  # 랜덤 문제 선택
    
    return render(request, "maze/maze_question.html", {"question": question})

# 정답 제출
def submit_answer(request):
    """사용자가 입력한 정답을 검사"""
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        user_answer = request.POST.get("answer", "").strip()

        question = get_object_or_404(MazeQuestion, id=question_id)

        if question.check_answer(user_answer):
            return redirect('maze_question')  # 정답이면 다음 문제로 이동
        else:
            return render(request, "maze/maze_question.html", {"question": question, "error": "❌ 오답입니다. 다시 시도하세요!"})

    return redirect('maze_start')

# 게임 완료 페이지
def maze_complete(request):
    return render(request, 'maze/maze_complete.html')