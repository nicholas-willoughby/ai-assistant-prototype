# 🤖 Taipan AI Assistant - Text-based Chat

**Taipan 혁신 팀을 위한 AI 기반 채팅 어시스턴트**

---

## 🎯 주요 기능

✅ **KPI 분석 및 조언**
- 8개 KPI 현황 실시간 분석
- Green/Yellow/Red 상태 판별
- 개선 방안 자동 제안

✅ **주간/월간 보고서 작성 지원**
- 보고서 구조 제안
- 주요 포인트 강조
- 템플릿 기반 작성 가이드

✅ **팀 성과 분석**
- 팀 협업 품질 평가
- 성과 지표 분석
- 트렌드 파악

✅ **리스크 조기 발견**
- 잠재 리스크 식별
- 대응 방안 제시
- 모니터링 가이드

✅ **자동화 기회 식별**
- 반복업무 분석
- 자동화 우선순위 제안
- 구현 방안 제시

---

## 🚀 설치 및 실행

### 1️⃣ 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2️⃣ API 키 설정

#### Windows
```bash
set COPILOT_API_KEY=your_github_copilot_api_key
```

#### Mac/Linux
```bash
export COPILOT_API_KEY=your_github_copilot_api_key
```

#### 또는 .env 파일 사용
```
COPILOT_API_KEY=your_github_copilot_api_key
```

### 3️⃣ 실행

```bash
python taipan_ai_chat.py
```

---

## 💬 사용 방법

### 기본 대화

```
👤 당신: 이번주 KPI 현황이 어떻게 돼?

🤖 Taipan AI: 이번주 KPI 현황을 분석해드리겠습니다.

## 📊 KPI 분석 결과

### 🟢 Green (80~100%)
- 문서화 자동화: 90%
- 협업 품질 향상: 80%

### 🟡 Yellow (50~79%)
- 업무 생산성: 85%
- 프로젝트 가시성: 72%
- KPI 달성: 68%
- 지식 축적: 75%

### 🔴 Red (0~49%)
- 리스크 조기 발견: 45% ⚠️ 긴급

[상세 분석 및 액션]
```

### 명령어 사용

| 명령어 | 기능 | 예시 |
|--------|------|------|
| `/kpi` | KPI 분석 | `/kpi` |
| `/risk` | 리스크 분석 | `/risk` |
| `/report` | 보고서 작성 지원 | `/report` |
| `/team` | 팀 분석 | `/team` |
| `/automate` | 자동화 제안 | `/automate` |
| `/context` | 현재 컨텍스트 확인 | `/context` |
| `/clear` | 대화 초기화 | `/clear` |
| `/help` | 도움말 | `/help` |

---

## 📝 질문 예시

### KPI 관련
```
- "업무 생산성을 10% 올리려면 어떻게 해야 할까?"
- "현재 가장 문제가 되는 KPI는?"
- "리스크 조기발견 45%를 개선하는 방법은?"
- "팀 KPI 목표가 달성 가능할까?"
```

### 보고서 관련
```
- "이번주 보고서를 어떻게 작성할까?"
- "주간 보고서에서 강조해야 할 포인트는?"
- "KPI 기여도를 어떻게 계산하지?"
- "리스크 섹션에 뭘 넣어야 할까?"
```

### 팀 관련
```
- "팀의 협업 품질을 어떻게 개선할까?"
- "팀원들의 역할이 명확한가?"
- "팀 성과가 지난주 대비 어떻게 됐어?"
- "팀에 필요한 교육은?"
```

### 자동화 관련
```
- "어떤 업무를 자동화할 수 있을까?"
- "주간 보고서 작성을 자동화할 수 있어?"
- "KPI 계산을 자동화하려면?"
- "Teams 알림을 자동화하는 방법은?"
```

---

## 🔧 고급 사용법

### Python 코드로 사용

```python
from taipan_ai_chat import TaipanAIAssistant

# AI 어시스턴트 초기화
assistant = TaipanAIAssistant(api_key="your_api_key")

# KPI 데이터 추가
assistant.add_kpi_data({
    "업무 생산성 향상": 85,
    "프로젝트 가시성 확보": 72,
    "리스크 조기 발견": 45
})

# 팀 컨텍스트 추가
assistant.add_team_context({
    "팀명": "Innovation Team",
    "팀원 수": "10명"
})

# 대화 시작
response = assistant.chat("이번주 KPI는?")
print(response)

# 대화 저장
assistant.save_conversation("conversation.json")

# 대화 불러오기
assistant.load_conversation("conversation.json")
```

### JSON으로 대화 저장/로드

```python
# 자동으로 JSON 형식으로 저장됨
# 포함 내용:
# - timestamp: 저장 시간
# - conversation: 전체 대화 히스토리
# - kpi_data: KPI 데이터
# - team_context: 팀 컨텍스트

# 나중에 불러와서 이어서 대화할 수 있음
assistant.load_conversation("taipan_chat.json")
```

---

## 📊 대화 히스토리 관리

- **최근 20개 메시지** 유지 (토큰 절약)
- `/clear` 명령어로 초기화 가능
- 종료 시 자동 저장 옵션 제공
- JSON 형식으로 저장/로드 가능

---

## 🎓 학습 및 개선

AI 어시스턴트는 대화를 통해:

✅ Taipan 팀의 컨텍스트를 학습  
✅ KPI 분석 능력 향상  
✅ 팀 특성에 맞는 조언 제공  
✅ 이전 대화 내용 활용

---

## ⚠️ 주의사항

### 데이터 보안
- 민감한 개인정보는 공유하지 마세요
- 대화는 저장되므로 보안에 유의하세요
- API 키는 환경변수로만 관리하세요

### 활용 가이드
- AI 조언은 참고용이며, 최종 결정은 팀리더가 하세요
- 정확하지 않을 수 있으므로 검증이 필요합니다
- 특별한 도메인 지식이 필요한 경우 전문가에게 상담하세요

---

## 🔗 관련 파일

- `kpi-dashboard-template.md` - KPI 대시보드 템플릿
- `kpi-dashboard.json` - KPI 데이터 (JSON)
- `weekly-report-template.md` - 주간 보고서 템플릿
- `weekly-report.json` - 주간 보고서 데이터

---

## 📞 문제 해결

### "COPILOT_API_KEY not set" 오류
→ 환경변수 설정 확인
→ `.env` 파일에 키 추가 후 재실행

### "API 연결 오류"
→ 인터넷 연결 확인
→ API 키 유효성 확인
→ Copilot API 할당량 확인

### "응답이 느림"
→ 인터넷 속도 확인
→ API 서버 상태 확인
→ 대화 히스토리 `/clear` 로 초기화

---

## 🚀 다음 단계

1. **Teams 연동** - Teams 채널에서 직접 사용
2. **Slack 연동** - Slack에서 @Taipan AI로 사용
3. **대시보드 연동** - KPI 데이터 자동 업데이트
4. **보고서 자동 생성** - 주간/월간 보고서 자동화
5. **예측 분석** - KPI 트렌드 예측

---

**Taipan AI Assistant와 함께 팀 성과를 높이세요! 🚀**
