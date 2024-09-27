# teamsparta_final
Django framework 기반의 LLM(Large Language Model)이 적용된 소개팅 사이트를 제작하는 프로젝트입니다. 범위 사용자 등록, 프로필 관리, 매칭 시스템, 채팅 기능, LLM 통합 등을 포함합니다.

이는 아키텍처 개요 시스템 컨텍스트 소개팅 서비스를 제공하는 웹 애플리케이션으로 사용자 경험을 향상시킵니다.

## 프로젝트 개요
범위 사용자 등록, 프로필 관리, 매칭 시스템, 채팅 기능, LLM 통합 등을 포함합니다.

이는 아키텍처 개요 시스템 컨텍스트 소개팅 서비스를 제공하는 웹 애플리케이션으로 사용자 경험을 향상시킵니다.

## 팀소개
- 팀명: Last Twerking
- 리더: 차민승
- 부 리더: 손진우
- 팀원: 박건희, 박윤성

## 개발일정
- 2024.09.23 ~ 2024.10. 

## 정의 및 약어

 - LLM: Large Language Model

 - Django: 파이썬 웹 프레임워크

 - API: Application Programming Interface

## 주요 컴포넌트

 - 사용자 관리 시스템

 - 프로필 관리 시스템

 - 매칭 엔진

 - 채팅 시스템

 - LLM 통합 모듈

## 컴포넌트 설명

 - 프론트엔드: html을 사용

 - Django 백엔드: RESTful API 제공

 - 데이터베이스: MySQL

 - LLM 서비스: LangChain을 통한 LLM 통합

## 데이터 모델 주요 엔티티

- User 모델: username : 사용자 아이디
- Profile 모델: user : User 모델과 1:1 관계
- Match 모델: user1 : 첫 번째 사용자 (User 모델과 외래키 관계)
- Conversation 모델: participants : 대화 참여자들 (User 모델과 다대다 관계)
- Message 모델: conversation : Conversation 모델과 외래키 관계

## 인터페이스 설계API 엔드 포인트

- `/api/accounts/`: 사용자 관리
- `/api/matches/`: 매칭 관리
- `/api/chat/`: 채팅 관리

## 주요 기능

### 1️⃣ 회원 기능
- 회원가입: 사용자는 플랫폼에 가입하여 개인 계정을 생성할 수 있습니다.
  - Required: user_id, password, nickname, email, 
  - Optional: bio
- 로그인 : 회원은 자신의 계정으로 로그인하여 서비스를 이용할 수 있습니다.
- 로그아웃 : 회원은 자신의 로그인 세션을 종료할 수 있습니다.
- 회원탈퇴 : 회원은 언제든지 계정을 삭제할 수 있으며, 탈퇴 시 계정은 비활성화로 전환됩니다.
- 비밀번호 변경 : 회원은 자신의 비밀번호를 변경할 수 있습니다.
------

 ###  2️⃣ 매칭 기능


------

###  3️⃣ 채팅 기능


------