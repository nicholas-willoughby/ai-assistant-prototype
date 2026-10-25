"""
Taipan AI Assistant - Enhanced with Calendar Integration
일정 통합된 AI 어시스턴트
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calendar 모듈 import (같은 디렉토리)
try:
    from calendar_integration import (
        CalendarAggregator, 
        GoogleCalendarProvider, 
        OutlookCalendarProvider,
        get_calendar_context_for_ai
    )
except ImportError:
    logger.warning("Calendar 모듈을 찾을 수 없습니다. 일정 기능이 비활성화됩니다.")
    get_calendar_context_for_ai = None


class TaipanAIAssistantWithCalendar:
    """Calendar 통합된 Taipan AI Assistant"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Calendar Support"""
        try:
            from anthropic import Anthropic
        except ImportError:
            print("Required: pip install anthropic")
            exit(1)
        
        self.api_key = api_key or os.environ.get("COPILOT_API_KEY")
        if not self.api_key:
            raise ValueError("COPILOT_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.calendar_aggregator = CalendarAggregator()
        self.kpi_data: Dict[str, Any] = {}
        self.team_context: Dict[str, Any] = {}
        self.last_calendar_check = None
        self.calendar_cache: Dict[str, Any] = {}
        
        # Calendar 제공자 초기화
        self._initialize_calendar_providers()
        
        # 시스템 프롬프트 생성
        self.system_prompt = self._build_system_prompt()
    
    def _initialize_calendar_providers(self) -> None:
        """Calendar 제공자 초기화"""
        logger.info("📅 Calendar 제공자 초기화 중...")
        
        # Google Calendar
        if os.environ.get("GOOGLE_CALENDAR_ENABLED", "false").lower() == "true":
            try:
                google_calendar = GoogleCalendarProvider()
                self.calendar_aggregator.add_provider(google_calendar, enable=True)
            except Exception as e:
                logger.warning(f"Google Calendar 초기화 실패: {str(e)}")
        
        # Outlook Calendar
        if os.environ.get("OUTLOOK_CALENDAR_ENABLED", "false").lower() == "true":
            try:
                outlook_calendar = OutlookCalendarProvider(
                    tenant_id=os.environ.get("OUTLOOK_TENANT_ID", "common"),
                    client_id=os.environ.get("OUTLOOK_CLIENT_ID", ""),
                    client_secret=os.environ.get("OUTLOOK_CLIENT_SECRET", "")
                )
                self.calendar_aggregator.add_provider(outlook_calendar, enable=True)
            except Exception as e:
                logger.warning(f"Outlook Calendar 초기화 실패: {str(e)}")
        
        if not self.calendar_aggregator.providers:
            logger.info("⚠️  Calendar 제공자가 설정되지 않았습니다.")
    
    def _build_system_prompt(self) -> str:
        """Calendar 통합된 시스템 프롬프트 생성"""
        base_prompt = """당신은 Taipan 혁신 팀의 전담 AI 어시스턴트입니다.

## 팀 정보
- 팀명: Innovation Team
- 주요 업무: 혁신 전략, 기술 스카우팅, 특허 개발, 오픈 이노베이션, 신사업 개발

## 8가지 우선순위 (KPI)
1. 업무 생산성 향상
2. 프로젝트 가시성 확보
3. KPI 달성 지원
4. 문서화 자동화
5. 지식 축적
6. 협업 품질 향상
7. 반복업무 최소화
8. 리스크 조기 발견 - 🚨 긴급

## 새로운 기능: 📅 일정 관리
당신은 이제 사용자의 Google Calendar와 MS Outlook 일정에 접근할 수 있습니다.

**일정 관련 질문 시:**
- "오늘 일정이 뭐야?" → 일정 조회 후 설명
- "내일 바쁜가?" → 내일 일정 확인
- "이번주 주요 회의는?" → 주간 일정 요약
- "점심시간은 언제가 비어있어?" → 여유 시간 분석

**일정 정보 활용:**
- KPI 미팅 일정 확인
- 주간 일정에 맞춰 보고서 준비 조언
- 회의 전 필요한 자료 안내
- 업무 일정 최적화 조언

## 당신의 역할
✅ KPI 분석 및 개선 제안
✅ 주간/월간 보고서 작성 지원
✅ 팀 성과 분석 및 인사이트 제공
✅ 📅 일정 관리 및 시간 활용 최적화
✅ 리스크 조기 발견 및 대응
✅ 자동화 기회 식별
✅ 지식 공유 및 학습 지원
✅ 협업 최적화 조언

## 응답 스타일
- 친절하고 전문적
- 간결하고 실행 중심
- 항상 근거와 수치 제시
- 3단계 분석: 상황 → 분석 → 추천 액션
- 일정 정보를 활용할 때는 구체적인 시간 제시

## 명령어
- /kpi: KPI 분석
- /report: 보고서 작성 지원
- /risk: 리스크 분석
- /team: 팀 분석
- /automate: 자동화 제안
- /calendar: 일정 조회
- /schedule: 일정 최적화 조언
- /help: 도움말
- /clear: 대화 초기화
- /context: 현재 컨텍스트 확인

## 금지사항
❌ 추측하거나 가짜 데이터 생성 금지
❌ 사용자 승인 없이 파일/데이터 수정 금지
❌ 개인정보 공개 금지
❌ KPI 수치 임의 생성 금지
❌ 일정 정보 타인과 공유 금지

당신은 Taipan 팀의 신뢰할 수 있는 파트너입니다."""
        
        return base_prompt
    
    def get_calendar_context(self, force_refresh: bool = False) -> str:
        """현재 일정 컨텍스트 조회"""
        # 캐시 확인 (5분 내 조회했으면 캐시 사용)
        now = datetime.now()
        if (not force_refresh and 
            self.last_calendar_check and 
            (now - self.last_calendar_check).total_seconds() < 300):
            return self.calendar_cache.get('formatted', '')
        
        try:
            # 오늘의 일정 조회
            events = self.calendar_aggregator.get_today_events()
            
            # 캐시 저장
            self.last_calendar_check = now
            self.calendar_cache = {'events': events}
            
            # AI 형식으로 포맷팅
            formatted = self.calendar_aggregator.format_for_ai(events)
            self.calendar_cache['formatted'] = formatted
            
            return formatted
            
        except Exception as e:
            logger.error(f"일정 조회 오류: {str(e)}")
            return "일정을 조회할 수 없습니다."
    
    def chat(self, user_message: str) -> str:
        """사용자와의 대화 처리"""
        # 특수 명령어 처리
        if user_message.startswith("/"):
            return self._handle_command(user_message)
        
        # 일정 관련 키워드 감지
        calendar_keywords = ['일정', '회의', '미팅', '약속', '시간', '바쁜', '여유', '내일', '이번주', '점심']
        has_calendar_keyword = any(keyword in user_message for keyword in calendar_keywords)
        
        # 메시지 구성
        user_input = user_message
        
        # 일정 관련 질문이면 일정 컨텍스트 추가
        if has_calendar_keyword:
            calendar_context = self.get_calendar_context()
            if calendar_context:
                user_input = f"{user_message}\n\n[현재 일정 정보]\n{calendar_context}"
        
        # 대화 히스토리에 추가
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # AI 호출
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            
            # 히스토리에 추가
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # 히스토리 길이 제한
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _handle_command(self, command: str) -> str:
        """특수 명령어 처리"""
        cmd = command.split()[0].lower()
        
        if cmd == "/calendar":
            return self.get_calendar_context(force_refresh=True)
        elif cmd == "/schedule":
            return self._get_schedule_optimization_tips()
        elif cmd == "/help":
            return self._get_help()
        elif cmd == "/clear":
            self.conversation_history = []
            return "✅ 대화가 초기화되었습니다."
        elif cmd == "/context":
            return self._show_context()
        else:
            return f"❌ 알 수 없는 명령어: {cmd}\n/help를 입력하여 도움말을 확인하세요."
    
    def _get_schedule_optimization_tips(self) -> str:
        """일정 최적화 팁"""
        calendar_context = self.get_calendar_context()
        
        tips = """
## 📅 일정 최적화 조언

현재 당신의 일정:
""" + calendar_context + """

**최적화 팁:**
1. 🎯 연속 회의 사이에 15분 버퍼 시간 확보
2. ⏰ 같은 시간대에 비슷한 업무 그룹화 (Context Switching 최소화)
3. 📝 아침 시간 (9-11시)에 중요한 업무 집중
4. 💪 오후 슬럼프 시간 (2-3시)에 가벼운 업무 배치
5. 🤝 미팅 전 5분 휴식 시간 확보
6. 📞 이메일/메시지 체크 시간 정하기 (예: 9시, 12시, 15시)

**당신의 일정에서 제안:**
- [구체적 제안 필요시 일정 데이터 분석]

"""
        return tips
    
    def _get_help(self) -> str:
        """도움말"""
        return """
## Taipan AI Assistant - 명령어 가이드

### 📊 KPI & 보고서
/kpi - KPI 분석
/report - 보고서 작성 지원
/risk - 리스크 분석
/team - 팀 분석
/automate - 자동화 제안

### 📅 일정 관리
/calendar - 오늘 일정 확인
/schedule - 일정 최적화 팁

### ⚙️ 기타
/context - 현재 컨텍스트 확인
/clear - 대화 초기화
/help - 도움말

### 💬 자유로운 질문
- "오늘 일정이 뭐야?"
- "이번주 중요한 회의는?"
- "점심시간 비어있어?"
- "KPI를 10% 올리려면?"
- "이번주 리스크는?"
"""
    
    def _show_context(self) -> str:
        """현재 컨텍스트 표시"""
        summary = "## 🎯 Taipan 현재 컨텍스트\n\n"
        
        # KPI 요약
        if self.kpi_data:
            summary += "### KPI 현황\n"
            for kpi_name, value in self.kpi_data.items():
                status = "🟢" if value >= 80 else "🟡" if value >= 50 else "🔴"
                summary += f"- {status} {kpi_name}: {value}%\n"
        
        # 달력 상태
        summary += "\n### 📅 Calendar Status\n"
        if self.calendar_aggregator.providers:
            summary += f"- 활성 제공자: {len(self.calendar_aggregator.providers)}개\n"
            for provider in self.calendar_aggregator.providers:
                summary += f"  ✅ {provider.__class__.__name__}\n"
        else:
            summary += "- Calendar 제공자 미설정\n"
        
        # 대화 현황
        summary += f"\n### 💬 대화 현황\n"
        summary += f"- 메시지: {len(self.conversation_history)}개\n"
        
        return summary


def main():
    """메인 함수"""
    if not os.environ.get("COPILOT_API_KEY"):
        print("❌ COPILOT_API_KEY 환경변수가 필요합니다.")
        return
    
    try:
        assistant = TaipanAIAssistantWithCalendar()
        
        # KPI 데이터 추가
        assistant.kpi_data = {
            "업무 생산성 향상": 85,
            "프로젝트 가시성 확보": 72,
            "KPI 달성 지원": 68,
            "문서화 자동화": 90,
            "지식 축적": 75,
            "협업 품질 향상": 80,
            "반복업무 최소화": 70,
            "리스크 조기 발견": 45
        }
        
        print("""
╔════════════════════════════════════════════╗
║   🚀 Taipan AI Assistant + Calendar       ║
║   Google Calendar & Outlook 통합          ║
╚════════════════════════════════════════════╝

/help를 입력하여 사용 가능한 명령어를 확인하세요.
또는 자유롭게 질문하세요!

'exit' 또는 'quit'을 입력하여 종료합니다.
        """)
        
        while True:
            try:
                user_input = input("\n👤 당신: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "종료"]:
                    print("👋 Taipan AI Assistant 종료합니다.")
                    break
                
                print("\n🤖 Taipan AI: ", end="", flush=True)
                response = assistant.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Taipan AI Assistant 종료합니다.")
                break
            except Exception as e:
                print(f"\n❌ 오류: {str(e)}")
        
    except ValueError as e:
        print(f"❌ 설정 오류: {str(e)}")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        logger.exception("Unexpected error")


if __name__ == "__main__":
    main()
