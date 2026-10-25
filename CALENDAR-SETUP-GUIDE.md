# 📅 Taipan AI Assistant - Calendar Integration Guide

**Google Calendar & MS Outlook을 AI Assistant에 통합하는 완벽한 가이드**

---

## 🎯 개요

이 모듈은 Taipan AI Assistant가 다음을 할 수 있게 합니다:

✅ Google Calendar에서 일정 조회  
✅ MS Outlook Calendar에서 일정 조회  
✅ 여러 달력의 일정을 통합 표시  
✅ 자연스러운 일정 기반 조언 제공  
✅ 일정 최적화 팁 제공

---

## 📦 파일 구조

```
calendar-integration/
├── calendar_integration.py         # Calendar API 통합 모듈
├── taipan_ai_with_calendar.py      # Calendar 통합 AI Assistant
├── CALENDAR-SETUP-GUIDE.md         # 이 파일
└── requirements.txt                # 필요한 패키지
```

---

## 🚀 설정 단계

### 1️⃣ **패키지 설치**

```bash
pip install -r requirements.txt
```

또는 수동 설치:

```bash
pip install anthropic python-dotenv
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install requests
```

---

### 2️⃣ **Google Calendar 설정**

#### Step 1: Google Cloud 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. **새 프로젝트** 생성
   - 프로젝트명: "Taipan Calendar"
3. **Calendar API** 활성화
   - API 및 서비스 > 라이브러리
   - "Google Calendar API" 검색
   - **활성화** 클릭

#### Step 2: OAuth 2.0 클라이언트 생성

1. **API 및 서비스 > 인증정보**로 이동
2. **인증정보 만들기** > **OAuth 클라이언트 ID**
3. 애플리케이션 유형: **데스크톱 앱**
4. JSON 파일 다운로드 → **google_credentials.json**으로 저장

#### Step 3: 환경 설정

`.env` 파일에 추가:

```
GOOGLE_CALENDAR_ENABLED=true
GOOGLE_CREDENTIALS_FILE=./google_credentials.json
```

또는 Python에서:

```python
from calendar_integration import GoogleCalendarProvider

google_cal = GoogleCalendarProvider(
    credentials_file="google_credentials.json"
)
google_cal.authenticate()  # 브라우저에서 인증
```

**첫 실행 시:** 브라우저가 열려서 Google 계정으로 인증하도록 요청합니다.

---

### 3️⃣ **MS Outlook Calendar 설정**

#### Step 1: Azure App 등록

1. [Azure Portal](https://portal.azure.com/) 접속
2. **Azure Active Directory > 앱 등록**
3. **새 등록**
   - 이름: "Taipan Calendar"
   - 지원되는 계정 유형: "조직의 디렉터리에 있는 계정만(Tenant only)"
   - 리다이렉트 URI: `http://localhost:8000/callback`

#### Step 2: 자격증명 생성

1. **관리 > 인증서 및 암호**
2. **새 클라이언트 암호**
3. 값을 복사하여 저장

#### Step 3: API 권한 추가

1. **관리 > API 권한**
2. **권한 추가**
3. **Microsoft Graph**
4. **위임된 권한**
5. "Calendars" 검색
6. **Calendars.Read** 선택
7. **권한 추가**

#### Step 4: 환경 설정

`.env` 파일에 추가:

```
OUTLOOK_CALENDAR_ENABLED=true
OUTLOOK_TENANT_ID=your-tenant-id
OUTLOOK_CLIENT_ID=your-client-id
OUTLOOK_CLIENT_SECRET=your-client-secret
```

**Tenant ID 찾기:**
- Azure Portal > Azure Active Directory > 개요
- **테넌트 ID** 복사

---

## 📝 사용 방법

### 기본 사용

```bash
python taipan_ai_with_calendar.py
```

### 대화 예시

```
👤 당신: 오늘 일정이 뭐야?

🤖 Taipan AI:
📅 **오늘의 일정**

### Google Calendar
1. **팀 회의**
   🕐 10:00 ~ 11:00
   📍 위치: 회의실 A
   👥 참가자: 5명

2. **KPI 분석 미팅**
   🕐 14:00 ~ 15:00
   📝 주간 KPI 검토

### Outlook Calendar
1. **프로젝트 진행 검토**
   🕐 11:30 ~ 12:00
   👥 참가자: 3명

총 3개의 일정
```

### 명령어

| 명령어 | 기능 |
|--------|------|
| `/calendar` | 오늘 일정 강제 새로고침 |
| `/schedule` | 일정 최적화 팁 |
| `/kpi` | KPI 분석 |
| `/help` | 도움말 |

### 자연스러운 질문

```
"이번주 중요한 회의는?"
"점심시간 언제가 비어있어?"
"내일 바쁜가?"
"주간 회의를 분석해줄래?"
"회의 전에 준비해야 할 자료는?"
```

---

## 🔧 Python 코드 사용

### Google Calendar 직접 사용

```python
from calendar_integration import GoogleCalendarProvider

# 인증
google = GoogleCalendarProvider()
google.authenticate()

# 오늘 일정 조회
today_events = google.get_today_events()

for event in today_events:
    print(f"✅ {event['title']}")
    print(f"   시간: {event['start']} ~ {event['end']}")
    print(f"   위치: {event['location']}")
```

### Outlook Calendar 직접 사용

```python
from calendar_integration import OutlookCalendarProvider

# 인증
outlook = OutlookCalendarProvider(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
outlook.authenticate()

# 오늘 일정
events = outlook.get_today_events()
```

### Calendar 통합

```python
from calendar_integration import CalendarAggregator, GoogleCalendarProvider, OutlookCalendarProvider

# 여러 달력 통합
aggregator = CalendarAggregator()

# Google 추가
google = GoogleCalendarProvider()
aggregator.add_provider(google)

# Outlook 추가
outlook = OutlookCalendarProvider(
    tenant_id="...",
    client_id="...",
    client_secret="..."
)
aggregator.add_provider(outlook)

# 모든 일정 조회
all_events = aggregator.get_today_events()

# AI 형식으로 포맷
formatted = aggregator.format_for_ai(all_events)
print(formatted)

# JSON으로 저장
aggregator.save_events_json(all_events, "today_events.json")
```

### AI Assistant와 통합

```python
from taipan_ai_with_calendar import TaipanAIAssistantWithCalendar

# AI Assistant 생성 (Calendar 자동 통합)
assistant = TaipanAIAssistantWithCalendar()

# 일정 관련 질문
response = assistant.chat("오늘 일정이 뭐야?")
print(response)

# 일정 최적화 조언
response = assistant.chat("/schedule")
print(response)
```

---

## ⚙️ 환경 변수 설정 (전체)

### `.env` 파일 템플릿

```env
# Copilot API
COPILOT_API_KEY=your_github_copilot_api_key

# Google Calendar
GOOGLE_CALENDAR_ENABLED=true
GOOGLE_CREDENTIALS_FILE=./google_credentials.json

# Outlook Calendar
OUTLOOK_CALENDAR_ENABLED=true
OUTLOOK_TENANT_ID=your_tenant_id
OUTLOOK_CLIENT_ID=your_client_id
OUTLOOK_CLIENT_SECRET=your_client_secret

# Taipan 설정
TEAM_NAME=Innovation Team
KPI_REVIEW_FREQUENCY=weekly
```

### Windows에서 환경 변수 설정

```batch
set GOOGLE_CALENDAR_ENABLED=true
set OUTLOOK_CALENDAR_ENABLED=true
set OUTLOOK_TENANT_ID=xxx
set OUTLOOK_CLIENT_ID=xxx
set OUTLOOK_CLIENT_SECRET=xxx
python taipan_ai_with_calendar.py
```

### Mac/Linux에서 환경 변수 설정

```bash
export GOOGLE_CALENDAR_ENABLED=true
export OUTLOOK_CALENDAR_ENABLED=true
export OUTLOOK_TENANT_ID=xxx
export OUTLOOK_CLIENT_ID=xxx
export OUTLOOK_CLIENT_SECRET=xxx
python taipan_ai_with_calendar.py
```

---

## 📊 출력 예시

### Calendar 정보 JSON

```json
{
  "timestamp": "2026-10-25T10:30:00",
  "events": {
    "GoogleCalendarProvider": [
      {
        "provider": "Google Calendar",
        "id": "abc123",
        "title": "팀 회의",
        "start": "2026-10-25T10:00:00+09:00",
        "end": "2026-10-25T11:00:00+09:00",
        "location": "회의실 A",
        "description": "주간 팀 미팅",
        "attendees": 5,
        "url": "https://calendar.google.com/..."
      }
    ],
    "OutlookCalendarProvider": [...]
  }
}
```

### AI Assistant 응답

```
📅 **오늘의 일정**

### Google Calendar
1. **팀 회의**
   🕐 10:00 ~ 11:00
   📍 위치: 회의실 A
   👥 참가자: 5명

### Outlook Calendar
1. **프로젝트 진행 검토**
   🕐 11:30 ~ 12:00
   👥 참가자: 3명

총 2개의 일정

**일정 최적화 팁:**
- 10:00~11:00: 팀 회의 (집중)
- 11:00~11:30: 여유 시간 (이메일/메시지 확인)
- 11:30~12:00: 프로젝트 검토
- 12:00~13:00: 점심 시간
```

---

## 🔐 보안 고려사항

### API 키 보안

✅ **해야 할 것:**
- `.env` 파일에 저장
- `.gitignore`에 `.env` 추가
- 환경 변수로 관리
- 정기적으로 키 갱신

❌ **하지 말 것:**
- 코드에 직접 입력
- GitHub에 커밋
- 이메일로 공유
- 평문으로 저장

### 일정 정보 보호

- 민감한 회의 정보 주의
- 타인과 공유 금지
- 임시 로그 파일 정기적 삭제

---

## 🐛 문제 해결

### "Google Calendar 인증 실패"

**원인:** 크리덴셜 파일이 없거나 잘못됨

**해결:**
1. `google_credentials.json` 파일 확인
2. Google Cloud Console에서 다시 다운로드
3. 파일명과 경로 확인

```python
# 디버그
import os
if os.path.exists("google_credentials.json"):
    print("✅ 파일 존재")
else:
    print("❌ 파일 없음")
```

### "Outlook 인증 오류"

**원인:** Tenant ID, Client ID, 또는 Secret이 잘못됨

**해결:**
1. Azure Portal에서 값 재확인
2. 특수문자 확인 (큰따옴표 제거)
3. 권한 설정 재확인

```python
# 테스트
from calendar_integration import OutlookCalendarProvider

outlook = OutlookCalendarProvider(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
print("인증 시도...")
result = outlook.authenticate()
print(f"결과: {result}")
```

### "일정이 비어있음"

**원인:** 
- Calendar가 공유되지 않음
- API 권한 부족
- 일정이 실제로 없음

**해결:**
```python
# 디버그 로그 활성화
import logging
logging.basicConfig(level=logging.DEBUG)

# 일정 조회 시도
events = google.get_today_events()
print(f"조회된 일정: {len(events)}개")
```

### "API 할당량 초과"

**원인:** API 호출이 너무 많음

**해결:**
- Calendar 조회 최소화 (캐시 사용 - 5분)
- 배치 처리
- API 할당량 증가 요청 (Google/Azure)

---

## 📚 추가 자료

### Google Calendar API
- [문서](https://developers.google.com/calendar/api)
- [Python 빠른 시작](https://developers.google.com/calendar/api/quickstart/python)
- [API 리퍼런스](https://developers.google.com/calendar/api/v3/reference)

### MS Graph API (Outlook)
- [문서](https://learn.microsoft.com/en-us/graph/api)
- [Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [인증](https://learn.microsoft.com/en-us/graph/auth)

---

## 🚀 다음 단계

### 구현됨
✅ Google Calendar 통합  
✅ MS Outlook 통합  
✅ Calendar Aggregator  
✅ AI Assistant 통합

### 계획 중
🔄 Outlook Teams 연동  
🔄 Calendar 이벤트 생성  
🔄 회의실 예약  
🔄 참석자 관리  
🔄 일정 충돌 감지  
🔄 자동 일정 제안

---

**Calendar 통합으로 팀의 시간 활용을 최적화하세요! 📅✨**
