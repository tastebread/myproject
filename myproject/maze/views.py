from django.shortcuts import render, redirect, get_object_or_404
from .models import MazeQuestion,MazeProgress
import random
from django.http import JsonResponse
from .forms import MazeQuestionForm
from django.contrib.auth.decorators import login_required

# 게임 시작 (첫 번째 문제로 이동)
@login_required
def start_maze(request):
    """게임을 시작할 때 기존 진행 상황이 있으면 이어서 진행"""
    progress, created = MazeProgress.objects.get_or_create(user=request.user)

    if created or not progress.current_question:
        first_question = MazeQuestion.objects.order_by('order').first()
        if first_question:
            progress.current_question = first_question
            progress.score = 0  # 점수 초기화
            progress.completed = False
            progress.save()
    
    print(f"게임 시작! 현재 문제: {progress.current_question.order}, 점수: {progress.score}")
    return redirect('maze_question')

# 문제 출제 (순서대로)
def maze_question(request):
    question_order = request.session.get('current_question', 1)  # 현재 문제 순서
    question = MazeQuestion.objects.filter(order=question_order).first()

    if not question:
        print("모든 문제 완료. 게임 종료")
        return redirect('maze_complete')  # 모든 문제를 풀면 완료 화면으로 이동

    return render(request, "maze/maze_question.html", {"question": question})

# 정답 제출 및 점수 반영
def submit_answer(request):
    """정답 제출 및 점수 반영"""
    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip()
        question_order = request.session.get('current_question', 1)
        question = MazeQuestion.objects.filter(order=question_order).first()

        if question:
            print(f"문제 {question.order} 정답 확인: {user_answer} vs {question.answer}")
            if user_answer.lower() == question.answer.lower():
                # ✅ 난이도에 따라 점수 차등 지급
                points = 10 if question.level == "easy" else 20 if question.level == "medium" else 30
                request.session['score'] = request.session.get('score', 0) + points

                # ✅ 다음 문제 찾기
                next_question = MazeQuestion.objects.filter(order=question.order + 1).first()
                
                if next_question:
                    request.session['current_question'] = next_question.order
                    print(f"다음 문제 이동 : {next_question.order}")
                    return JsonResponse({"correct": True, "score": request.session['score'], "next_question_url": "/maze/question/"})
                else:
                    return JsonResponse({"correct": True, "score": request.session['score'], "next_question_url": "/maze/complete/"})

            else:
                # 오답일 경우 감점 (최소 0점 유지)
                request.session['score'] = max(0, request.session.get('score', 0) - 5)
                return JsonResponse({"correct": False, "message": "❌ 오답입니다. 다시 시도하세요!", "score": request.session['score']})

    return JsonResponse({"error": "Invalid request"}, status=400)
# 게임 완료 페이지
def maze_complete(request):
    return render(request, 'maze/maze_complete.html', {"score": request.session.get('score', 0)})

# 힌트 제공 기능
def get_hint(request):
    question_order = request.session.get('current_question', 1)
    question = MazeQuestion.objects.filter(order=question_order).first()

    if question and question.hint:
        return JsonResponse({"hint": question.hint})
    else:
        return JsonResponse({"hint": "❌ 이 문제는 힌트를 제공하지 않습니다."})
    

# 미궁 문제 리스트 (관리자 전용)
@login_required
def manage_maze_questions(request):
    questions = MazeQuestion.objects.order_by('order')
    return render(request, 'maze/manage_questions.html', {'questions': questions})

# 미궁 문제 추가
@login_required
def add_maze_question(request):
    if request.method == "POST":
        form = MazeQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_maze_questions')
    else:
        form = MazeQuestionForm()
    return render(request, 'maze/add_question.html', {'form': form})

# 미궁 문제 수정
@login_required
def edit_maze_question(request, question_id):
    question = get_object_or_404(MazeQuestion, id=question_id)
    if request.method == "POST":
        form = MazeQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('manage_maze_questions')
    else:
        form = MazeQuestionForm(instance=question)
    return render(request, 'maze/edit_question.html', {'form': form, 'question': question})

# 미궁 문제 삭제
@login_required
def delete_maze_question(request, question_id):
    question = get_object_or_404(MazeQuestion, id=question_id)
    if request.method == "POST":
        question.delete()
        return redirect('manage_maze_questions')
    return render(request, 'maze/delete_question.html', {'question': question})

def question_list(request):
    """모든 미궁 문제를 보여주는 페이지"""
    questions = MazeQuestion.objects.all().order_by('order')
    return render(request, "maze/question_list.html", {"questions": questions})