# GPTing (지피팅) - AI 기반 소개팅 서비스
![image](https://github.com/user-attachments/assets/ee0fec20-ae0d-43f4-bc4d-0447d0fe1e4e)

GPTing은 AI 기술을 활용한 소개팅 서비스API 입니다. 

사용자의 프로필과 대화 내용을 분석하여 최적의 매칭을 제공합니다.

## 팀 구성
| **이름** | **역할**            | **기능**                          |
|:------------:|--------------------------|----------------------------------|
|      |  |                   | 
|   손진우   | 부팀장 | 회원기능, 매칭기능, 백엔드, LLM |
|      |  |                   |
|      |  |                   |

## 주요 기능

- AI 기반 사용자 매칭
- 실시간 채팅
- 부적절한 언어 감지
- 대화 주제 추천
- 프로필 관리
- 관심사 기반 추천

## 기술 스택

- Backend: Django, Django REST Framework
- Database: PostgreSQL
- AI/ML: OpenAI GPT
- 인증: JWT (JSON Web Tokens)
- 배포: AWS

## 보안
- JWT 인증
- 회원가입 이메일 인증 기능
- 비밀번호 해시화

## 서비스 아키텍쳐
![image](https://github.com/user-attachments/assets/d0829a34-efb8-44d1-9796-0d6ddd666b7e)

## ERD
[ERD 사진 추가해주세용](https://github.com/Jinw000/teamsparta_final/issues/9#issue-2609810408)

## 설치 및 실행 방법

1. 저장소 클론

git clone https://github.com/Jinw000/teamsparta_final.git

3. 가상 환경 생성 및 활성화

python -m venv venv

source venv/bin/activate # Windows: venv\Scripts\activate

5. 페키지 설치

pip install -r requirements.txt


6. 데이터베이스 마이그레이션 및 서버 실행

python manage.py migrate

python manage.py runserver


