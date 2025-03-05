#  Django 기반 웹 애플리케이션 프로젝트



Django를 활용하여 개발된 다기능 웹 애플리케이션 프로젝트입니다.
게시판(board), 계정(account), 미궁 게임(maze) 기능을 포함하며,   
사용자가 다양한 서비스를 하나의 플랫폼에서 활용할 수 있도록 구성되었습니다.   

## 주요 기능

1. 미궁 게임 – 사용자가 다양한 난이도의 문제를 풀며 진행하는 텍스트 기반 게임   
2. 리더보드 – 점수를 저장하고, 최고 점수를 기록하여 랭킹 확인 가능   
3. 게시판 – 자유로운 게시글 작성 및 댓글 기능 제공   
4. 계정 관리 – 회원가입 및 로그인, 프로필 관리   
5. Railway 배포 – 클라우드 환경에서 애플리케이션을 실행 및 관리   

Live Demo • 🛠 GitHub Repository

## 기술 스택
|구분|사용기술|
|------|-----------|
|백엔드|Django,Python,Django ORM|
|프론트엔드|HTML,CSS,JavaScript|
|데이터베이스|PostgreSQL (Railway)|
|배포환경|Railway,CI/CD 지원|


## 프로젝트 스크린샷

### 미궁 게임 플레이

텍스트 기반 문제 풀이를 통해 미궁을 탐험하세요.



### 게시판 기능

사용자가 자유롭게 글을 작성하고 댓글을 달 수 있습니다.



### 리더보드 시스템

게임 점수가 기록되며, 사용자 랭킹을 확인할 수 있습니다.



## 프로젝트 구조

myproject/   
### maze/              # 미궁 게임 앱   
ㄴ models.py      # 데이터베이스 모델 정의   
ㄴ views.py       # 게임 관련 로직 구현   
ㄴ urls.py        # URL 매핑   
ㄴ templates/     # 템플릿 파일 저장   
ㄴ froms.py/        # 문제 제작   

### accounts/          # 계정 관리 앱   
ㄴ views.py/      # 계정 관련 로직 구현   
ㄴ urls.py/       # URL 매핑   
ㄴ models.py/     # 데이터베이스 모델 정의   
ㄴ templates/     # 템플릿 파일   
### board/             # 게시판 앱   
ㄴ views.py/      # 게시판 관련 로직 구현   
ㄴ urls.py/       # URL 매핑   
ㄴ models.py/     # 데이터베이스 모델 정의   
ㄴ templates/     # 템플릿 파일   

manage.py          # Django 프로젝트 실행 파일   
requirements.txt   # 프로젝트 의존성 패키지 목록   
templates          # 전체 템플릿 파일 관리   
static             # 정적 파일 저장   
README.md          # 프로젝트 설명 파일   

## 개발 과정 및 배운 점(업데이트 예정)

1.Django ORM 최적화 → select_related() 및 prefetch_related() 활용하여 성능 개선   
2.Railway 배포 문제 해결 → ALLOWED_HOSTS 설정 조정 및 whitenoise 적용   
3.반응형 UI 개선 → 모바일에서도 정상 동작하도록 CSS 최적화   
4.한번에 여러개의 앱을 만들고 적용시켰을때 꼬이는 현상이 자주 일어나서 코드 최적화도 함께 진행했음

## 프로젝트의 차별점   

1.텍스트 기반의 인터랙티브 문제 풀이 제공   
2.여러 테마의 미궁제작하여 차별화된 게임 경험 제공   
3.리더보드 시스템을 통해 경쟁 요소 추가   
4.게시판 기능을 활용한 사용자 간 소통 가능   

## 향후 추가 기능 (업데이트 예정)   
1.


## 설치 및 실행 방법
```
git clone https://github.com/your-repository.git   
cd myproject   
pip install -r requirements.txt   
python manage.py migrate   
python manage.py runserver   
```
이후, 브라우저에서 http://127.0.0.1:8000/ 열어 프로젝트를 확인하세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자유롭게 사용하고 개선할 수 있습니다!

