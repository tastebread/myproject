from django.shortcuts import render, redirect, get_object_or_404
from .models import MazeQuestion,MazeProgress
import random
from django.http import JsonResponse
from .forms import MazeQuestionForm
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.views.decorators.http import require_POST
from django.contrib import messages
#난이도 선택
def select_difficulty(request):
    if request.method == "POST":
        difficulty = request.POST.get("difficulty")
        if difficulty in ['easy','medium','hard']:
            request.session['difficulty'] = difficulty
            request.session['current_question'] = 1 #문제 순서 초기화
            request.session['score'] = 0 # 점수 초기화
            return redirect('start_maze')
        else:
            #유효 하지 않은 난이도가 선택된 경우, 에러 메시지와 함께 난이도 선택 화면 다시 렌더링
            context = {"error": "올바른 난이도를 선택해주세요."}
            return render(request, "maze/select_difficulty.html", context)
    else:
        return render(request, "maze/select_difficulty.html")
# 게임 시작 (첫 번째 문제로 이동)
@login_required
def start_maze(request):
    """게임을 시작할 때 기존 진행 상황이 있으면 이어서 진행"""
    #난이도 값 가져오기 (단 세션에 저장되어있어야함)
    difficulty = request.session.get('difficulty')
    if not difficulty:
        return redirect('select_difficulty')
    
    progress, created = MazeProgress.objects.get_or_create(user=request.user)

    if created or not progress.current_question_id: #DB 조회 최소화
        first_question = MazeQuestion.objects.filter(level=difficulty).order_by('order').first()
        if first_question:
            progress.current_question = first_question
            progress.score = 0  # 점수 초기화
            progress.completed = False
            progress.save()
        else:
            messages.error(request, "문제가 없습니다. 관리자에게 문의하세요.")
            return redirect('select_difficulty')
    
    print(f"게임 시작! 현재 문제: {progress.current_question.order}, 점수: {progress.score}")
    return redirect('maze_question')

# 문제 출제 (순서대로)
def maze_question(request):
    question_order = request.session.get('current_question', 1)  # 현재 문제 순서
    difficulty = request.session.get('difficulty','easy')
    #난이도와 order를 함께 필터링
    question = MazeQuestion.objects.filter(level=difficulty, order=question_order).first()

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
        difficulty = request.session.get('difficulty')
        question = MazeQuestion.objects.filter(level=difficulty, order=question_order).first()

        if question:
            #타이머가 자동 제출이라면, user_answer가 빈 문자열일 수 있음
            if user_answer == "":
                #시간 초과 처리 : 오답 취급, 감점 적용
                request.session['score'] = max(0, request.session.get('score', 0) - 5)
                return JsonResponse({"correct": False, "message":"시간 초과! ❌ 오답입니다.", "score" : request.session['score']})
            print(f"문제 {question.order} 정답 확인: {user_answer} vs {question.answer}") # 디버깅
            correct_answer = question.answer.strip().lower()
            if user_answer.lower() == escape(correct_answer): #보안 강화 추가
                #  난이도에 따라 점수 차등 지급
                points = 10 if question.level == "easy" else 20 if question.level == "medium" else 30
                request.session['score'] = request.session.get('score', 0) + points

                #  다음 문제 찾기
                next_question = MazeQuestion.objects.filter(level=difficulty, order=question_order + 1).first()
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
    difficulty = request.session.get('difficulty') #현재 난이도에 맞는 힌트만 제공
    question = MazeQuestion.objects.filter(order=question_order, level=difficulty).first()

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
            messages.success(request, "문제가 성공적으로 수정되었습니다!")
            return redirect('manage_maze_questions')
    else:
        form = MazeQuestionForm(instance=question)
    return render(request, 'maze/edit_question.html', {'form': form, 'question': question})

# 미궁 문제 삭제
@login_required
@require_POST
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


            