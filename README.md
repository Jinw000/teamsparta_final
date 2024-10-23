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

## 기술적 의사 결정
1. 채팅 기능 관련 기술 의사 결정
실시간 양방향 통신이 가능한 Websocket 구현 방식의 채팅 기능 채택

 2. Docker를 활용한 서버 가상화


>> 서버 호스트 (127.0.0.1.6379)를 사용하기 위해 Docker 활용

## 트러블 슈팅
 1. 특정 사용자 websocket 연결 생성
>> JS에서 django로 던지는 것을 인지하여, Postman에서 access token을 발급하고, 
특정 사용자의 websocket 연결 생성 가능하게 함.

<script>
    const roomId = {{ room_id }};
    const accessToken = '...';  // Postman에서 발급받은 실제 액세스 토큰 값
    const chatLog = document.getElementById("chat-log");
    const chatMessageInput = document.getElementById("chat-message-input");
    const chatMessageSubmit = document.getElementById("chat-message-submit");

    // WebSocket 연결 생성
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomId + '/' + '?token=' + accessToken
    );

    // 서버로부터 메시지를 받을 때 호출되는 함수
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const sender = data.sender;
        const timestamp = new Date().toLocaleTimeString();  // 메시지 시간을 현재 시간으로 설정
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");

        // 보낸 사람과 받는 사람에 따라 다른 스타일 적용
        if (sender === "나") {
            messageElement.classList.add("sent");
        } else {
            messageElement.classList.add("received");
        }

        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}<time>${timestamp}</time>`;
        chatLog.appendChild(messageElement);

        // 자동 스크롤
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    // WebSocket 연결이 종료되었을 때
    chatSocket.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };

    // 메시지 전송 버튼 클릭 시 메시지 전송
    chatMessageSubmit.onclick = function() {
        const message = chatMessageInput.value;

        if (message.trim() !== "") { // 빈 문자열은 메시지가 보내지지 않도록 설정
            chatSocket.send(JSON.stringify({
                message
            }));
            chatMessageInput.value = '';  // 메시지 전송 후 입력란 초기화
        }
    };

    // Enter 키를 눌렀을 때 메시지 전송
    chatMessageInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            chatMessageSubmit.click();
        }
    });
</script>
​
 
 2. 브라우저에서 새로 고침을 하여도, 채팅창 메시지가 저장되지 않는 버그가 발생
    
    function addMessageToChatLog(sender, message, timestamp) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        const timeString = new Date(timestamp).toLocaleTimeString(); // 받은 메시지의 시간을 표시
        console.log(sender, message, timestamp);

        // 보낸 사람과 받는 사람에 따라 스타일 적용
        if (sender === currentUser) {
            messageElement.classList.add("sent");
        } else {
            messageElement.classList.add("received");
        }

        messageElement.innerHTML = `<strong>${sender}:</strong> ${message} <time>${timeString}</time>`;
        chatLog.appendChild(messageElement);

        // 스크롤을 아래로 자동 이동
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // 서버에서 기존 메시지를 불러와 채팅창에 추가
    fetch(`http://127.0.0.1:8000/api/chats/api/rooms/${roomId}/messages/`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
})
    .then(response => response.json())
    .then(messages => {
        messages.forEach(message => {
            console.log(message);
            addMessageToChatLog(message.sender_username, message.content, message.timestamp);
        });
    });

        console.log(addMessageToChatLog.data);
​
>> fetch 함수를 사용하여, 기존의 메시지를 불러와 채팅창에 추가


 3. channels 서버 호환 문제
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis 서버 설정 > 도커를 쓸건지 안쓸건지
        },
    },
} # Redis랑 channels랑 연결 > Redis를 수락받아야한다. 방식을 설정하고..

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
​
>> localhost, 6379를 사용하기 위해 Docker를 활용하여 해결


 4. 로그인한 사용자는 오른쪽, 상대방은 왼쪽에 나타나게 하는 방법 해결
 - 프론트엔드 부분 수정
chat-log에서 flex-direction: column, display: flex로 변경
text-align에서 align-self: end, start로 변경
        .chat-log {
            width: 100%;
            height: 400px;
            border: 1px solid #ddd;
            padding: 10px;
            overflow-y: scroll;
            background-color: #f9f9f9;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
        }
        .chat-log .message {
            margin: 5px 0;
            padding: 10px;
            border-radius: 10px;
            width: fit-content;
            max-width: 70%;
        }
        .chat-log .message.sent {
            background-color: #DCF8C6;
            margin-left: auto;
            align-self: end;
        }
        .chat-log .message.received {
            background-color: #fff;
            border: 1px solid #ddd;
            align-self: start;






