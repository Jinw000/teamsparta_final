# GPTing (지피팅) - AI 기반 소개팅 서비스
![image](https://github.com/user-attachments/assets/ee0fec20-ae0d-43f4-bc4d-0447d0fe1e4e)

GPTing은 AI 기술을 활용한 소개팅 서비스API 입니다. 

사용자의 프로필과 대화 내용을 분석하여 최적의 매칭을 제공합니다.

## 팀 구성
| **이름** | **역할**            | **기능**                          |
|:------------:|--------------------------|----------------------------------|
|   차민승   | 팀장 | 채팅 기능, 배포, 시연 영상 |
|      |  |                   | 
|   손진우   | 부팀장 | 회원기능, 매칭기능, 백엔드, LLM |
|      |  |                   |
|      |  |                   |

## 정의 및 약어

 - LLM: Large Language Model

 - Django: 파이썬 웹 프레임워크

 - API: Application Programming Interface


## 인터페이스 설계API 엔드 포인트

- `/api/accounts/`: 사용자 관리
- `/api/matches/`: 매칭 관리
- `/api/chat/`: 채팅 관리

## 주요 컴포넌트

 - 사용자 관리 시스템
 - 프로필 관리 시스템
 - 매칭 엔진
 - 채팅 시스템
 - LLM

## 주요 기능

- AI 기반 사용자 매칭
- 실시간 1:1 채팅
- 프로필 관리
- 이메일 인증
- 채팅 관리

## 기술 스택

- Backend: Django, Django REST Framework, Django channels, Websocket, Docker(서버 가상화)
- Database: PostgreSQL
- AI/ML: OpenAI GPT
- 인증: JWT (JSON Web Tokens)
- 배포: AWS, daphne, MobaXterm, gunicorn, nginx

## 보안
- JWT 인증
- 회원가입 이메일 인증 기능
- 비밀번호 해시화

## 서비스 아키텍쳐
![image](https://github.com/user-attachments/assets/d0829a34-efb8-44d1-9796-0d6ddd666b7e)

## ERD
[![image](https://github.com/Jinw000/teamsparta_final/issues/9#issue-2609810408)](https://github.com/Jinw000/teamsparta_final/issues/10#issue-2609821045)


## 설치 및 실행 방법

1. 저장소 클론

git clone https://github.com/Jinw000/teamsparta_final.git

2. 가상 환경 생성 및 활성화

python -m venv venv

source venv/bin/activate # Windows: venv\Scripts\activate

3. 페키지 설치

pip install -r requirements.txt


4. 데이터베이스 마이그레이션 및 서버 실행

python manage.py migrate

python manage.py runserver



