"""
Taipan AI Assistant - Text-based Chat Interface
GitHub Copilot API를 기반으로 한 Taipan 팀 관리 어시스턴트

주요 기능:
- KPI 분석 및 조언
- 주간 보고서 작성 보조
- 팀 성과 분석
- 리스크 조기 발견
- 자동화 제안
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# GitHub Copilot API 클라이언트 설정
try:
    from anthropic import Anthropic  # GitHub Copilot uses Claude
except ImportError:
    print("Required: pip install anthropic")
    exit(1)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaipanAIAssistant:
    """Taipan AI Assistant - KPI 및 팀 관리 어시스턴트"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Taipan AI Assistant
        
        Args:
            api_key: GitHub Copilot API Key (defaults to COPILOT_API_KEY env)
        """
        self.api_key = api_key or os.environ.get("COPILOT_API_KEY")
        if not self.api_key:
            raise ValueError("COPILOT_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = self._build_system_prompt()
        self.kpi_data: Dict[str, Any] = {}
        self.team_context: Dict[str, Any] = {}
        
    def _build_system_prompt(self) -> str:
        """Taipan 시스템을 위한 시스템 프롬프트 생성"""
        return """당신은 Taipan 혁신 팀의 전담 AI 어시스턴트입니다.

## 팀 정보
- 팀명: Innovation Team
- 주요 업무: 혁신 전략, 기술 스카우팅, 특허 개발, 오픈 이노베이션, 신사업 개발
- 핵심 원칙: 데이터 기반 의사결정, 실행 가능한 조치

## 8가지 우선순위 (KPI)
1. 업무 생산성 향상 (현황: 85%)
2. 프로젝트 가시성 확보 (현황: 72%)
3. KPI 달성 지원 (현황: 68%)
4. 문서화 자동화 (현황: 90%)
5. 지식 축적 (현황: 75%)
6. 협업 품질 향상 (현황: 80%)
7. 반복업무 최소화 (현황: 70%)
8. 리스크 조기 발견 (현황: 45%) - 🚨 긴급

## 당신의 역할
✅ KPI 분석 및 개선 제안
✅ 주간/월간 보고서 작성 지원
✅ 팀 성과 분석 및 인사이트 제공
✅ 리스크 조기 발견 및 대응
✅ 자동화 기회 식별
✅ 지식 공유 및 학습 지원
✅ 협업 최적화 조언

## 응답 스타일
- 친절하고 전문적
- 간결하고 실행 중심
- 항상 근거와 수치 제시
- 3단계 분석: 상황 → 분석 → 추천 액션

## 응답 형식
사용자의 요청 유형에 따라:

### KPI 질문
1. 상황 요약
2. 현황 분석 (Green/Yellow/Red)
3. 리스크 평가
4. 구체적 액션 3개

### 보고서 작성
1. 구조 제안
2. 핵심 포인트
3. 작성 팁
4. 템플릿 제공

### 팀 분석
1. 데이터 요약
2. 트렌드 분석
3. 병목 식별
4. 개선 방안

## 금지사항
❌ 추측하거나 가짜 데이터 생성 금지
❌ 사용자 승인 없이 파일/데이터 수정 금지
❌ 개인정보 공개 금지
❌ KPI 수치 임의 생성 금지

## 명령어
- /kpi: KPI 분석
- /report: 보고서 작성 지원
- /risk: 리스크 분석
- /team: 팀 분석
- /automate: 자동화 제안
- /help: 도움말
- /clear: 대화 초기화
- /context: 현재 컨텍스트 확인

당신은 Taipan 팀의 신뢰할 수 있는 파트너입니다. 항상 정직하고, 데이터에 기반하고, 행동 지향적으로 응답하세요."""
    
    def add_kpi_data(self, kpi_data: Dict[str, Any]) -> None:
        """KPI 데이터 추가"""
        self.kpi_data = kpi_data
        logger.info("KPI data updated")
    
    def add_team_context(self, context: Dict[str, Any]) -> None:
        """팀 컨텍스트 정보 추가"""
        self.team_context = context
        logger.info("Team context updated")
    
    def chat(self, user_message: str) -> str:
        """
        사용자와의 대화 처리
        
        Args:
            user_message: 사용자 메시지
            
        Returns:
            AI 어시스턴트 응답
        """
        # 특수 명령어 처리
        if user_message.startswith("/"):
            return self._handle_command(user_message)
        
        # 대화 히스토리에 사용자 메시지 추가
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # GitHub Copilot API 호출
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # GitHub Copilot uses Claude
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            # 응답 추출
            assistant_message = response.content[0].text
            
            # 대화 히스토리에 AI 응답 추가
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # 대화 히스토리 길이 제한 (최근 20개 메시지만 유지)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error communicating with AI: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _handle_command(self, command: str) -> str:
        """특수 명령어 처리"""
        cmd = command.split()[0].lower()
        
        if cmd == "/help":
            return self._get_help()
        elif cmd == "/clear":
            self.conversation_history = []
            return "✅ 대화가 초기화되었습니다."
        elif cmd == "/context":
            return self._show_context()
        elif cmd == "/kpi":
            return self._analyze_kpis()
        elif cmd == "/risk":
            return self._analyze_risks()
        elif cmd == "/team":
            return self._analyze_team()
        elif cmd == "/automate":
            return self._suggest_automation()
        elif cmd == "/report":
            return self._guide_report_writing()
        else:
            return f"❌ 알 수 없는 명령어: {cmd}\n/help를 입력하여 도움말을 확인하세요."
    
    def _get_help(self) -> str:
        """도움말 표시"""
        return """
## Taipan AI Assistant - 명령어 가이드

### 📊 KPI 관련
/kpi - KPI 분석 및 현황 파악
/risk - 리스크 분석 및 대응 방안

### 📋 보고서 관련
/report - 주간/월간 보고서 작성 지원

### 👥 팀 관련
/team - 팀 성과 분석
/automate - 반복업무 자동화 제안

### ⚙️ 기타
/context - 현재 팀/KPI 컨텍스트 확인
/clear - 대화 초기화
/help - 도움말 (현재 명령어)

### 💬 자유로운 질문
명령어가 없어도 다음 주제로 자유롭게 질문 가능:
- "KPI를 10% 올리려면 어떻게 해야 할까?"
- "이번주 리스크가 뭘까?"
- "팀의 협업 품질을 개선하려면?"
- "어떤 업무를 자동화할 수 있을까?"
- "이 문제를 어떻게 해결할까?"

### 📞 필요한 경우
데이터가 필요한 경우 구체적으로 요청하세요:
- "KPI 데이터를 알려줄래?"
- "지난주 보고서 있어?"
- "팀원의 역할 정보를 보여줄래?"
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
        else:
            summary += "- KPI 데이터 없음\n"
        
        # 팀 컨텍스트
        if self.team_context:
            summary += "\n### 팀 정보\n"
            for key, value in self.team_context.items():
                summary += f"- {key}: {value}\n"
        else:
            summary += "\n### 팀 정보\n- 기본 정보만 설정됨\n"
        
        # 대화 히스토리
        summary += f"\n### 대화 현황\n- 메시지: {len(self.conversation_history)}개\n"
        
        return summary
    
    def _analyze_kpis(self) -> str:
        """KPI 분석"""
        msg = "KPI를 분석해주세요. 분석할 KPI 이름을 말씀해주세요.\n\n예시:\n- 업무 생산성 향상\n- 프로젝트 가시성 확보\n- 리스크 조기 발견\n- 전체 KPI 분석"
        return msg
    
    def _analyze_risks(self) -> str:
        """리스크 분석"""
        return "🚨 리스크 분석 모드\n\n현재 주요 리스크는 '리스크 조기 발견'(45%)입니다.\n\n구체적인 리스크를 말씀해주세요:\n- 프로젝트 리스크\n- 팀 리스크\n- 기술 리스크\n- 기타 리스크"
    
    def _analyze_team(self) -> str:
        """팀 분석"""
        return "👥 팀 분석 모드\n\n다음 항목을 분석해드릴 수 있습니다:\n- 팀 협업 현황\n- 팀원 역할 및 책임\n- 팀 성과 지표\n- 팀 강점 및 약점\n\n구체적으로 알고 싶은 부분이 있으신가요?"
    
    def _suggest_automation(self) -> str:
        """자동화 제안"""
        return "🤖 반복업무 자동화 제안\n\n다음 영역에서 자동화 기회를 찾을 수 있습니다:\n- 보고서 작성 자동화\n- 데이터 수집 자동화\n- Teams/Slack 알림 자동화\n- KPI 계산 자동화\n- 문서 생성 자동화\n\n자동화하고 싶은 업무를 설명해주세요."
    
    def _guide_report_writing(self) -> str:
        """보고서 작성 지원"""
        return "📋 보고서 작성 지원\n\n다음 보고서를 작성하는 데 도움을 드릴 수 있습니다:\n- 주간 보고서\n- 월간 리뷰\n- KPI 분석 보고서\n- 리스크 보고서\n- 팀 성과 보고서\n\n어떤 보고서를 작성하고 싶으신가요?"
    
    def save_conversation(self, filepath: str) -> None:
        """대화 내용 저장"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "conversation": self.conversation_history,
            "kpi_data": self.kpi_data,
            "team_context": self.team_context
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Conversation saved to {filepath}")
    
    def load_conversation(self, filepath: str) -> None:
        """대화 내용 불러오기"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.conversation_history = data.get("conversation", [])
        self.kpi_data = data.get("kpi_data", {})
        self.team_context = data.get("team_context", {})
        logger.info(f"Conversation loaded from {filepath}")


class TaipanChatUI:
    """Taipan AI Assistant - CLI 인터페이스"""
    
    def __init__(self, assistant: TaipanAIAssistant):
        self.assistant = assistant
    
    def run(self) -> None:
        """대화식 채팅 실행"""
        print("""
╔════════════════════════════════════════════╗
║   🚀 Taipan AI Assistant - Chat Mode      ║
║   Innovation Team Management System        ║
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
                    self._show_goodbye()
                    break
                
                # AI 응답 생성
                print("\n🤖 Taipan AI: ", end="", flush=True)
                response = self.assistant.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                self._show_goodbye()
                break
            except Exception as e:
                print(f"\n❌ 오류 발생: {str(e)}")
    
    def _show_goodbye(self) -> None:
        """종료 메시지"""
        print("""
╔════════════════════════════════════════════╗
║      👋 Taipan AI Assistant 종료          ║
║      대화를 저장하시겠습니까?             ║
╚════════════════════════════════════════════╝

저장하려면 파일명을 입력하세요. (예: taipan_chat.json)
또는 'n'을 입력하여 저장하지 않고 종료합니다.
        """)
        
        save_input = input("저장 여부 (파일명 또는 n): ").strip()
        
        if save_input and save_input.lower() != "n":
            try:
                self.assistant.save_conversation(save_input)
                print(f"✅ 대화가 {save_input}에 저장되었습니다.")
            except Exception as e:
                print(f"❌ 저장 오류: {str(e)}")
        
        print("\n감사합니다! 👋")


def main():
    """메인 함수"""
    # API 키 확인
    if not os.environ.get("COPILOT_API_KEY"):
        print("❌ 오류: COPILOT_API_KEY 환경변수가 설정되지 않았습니다.")
        print("\n설정 방법:")
        print("Windows: set COPILOT_API_KEY=your_api_key")
        print("Mac/Linux: export COPILOT_API_KEY=your_api_key")
        return
    
    try:
        # AI 어시스턴트 초기화
        assistant = TaipanAIAssistant()
        
        # 샘플 데이터 로드 (선택사항)
        assistant.add_kpi_data({
            "업무 생산성 향상": 85,
            "프로젝트 가시성 확보": 72,
            "KPI 달성 지원": 68,
            "문서화 자동화": 90,
            "지식 축적": 75,
            "협업 품질 향상": 80,
            "반복업무 최소화": 70,
            "리스크 조기 발견": 45
        })
        
        assistant.add_team_context({
            "팀명": "Innovation Team",
            "주요 업무": "혁신 전략, 기술 스카우팅, 특허 개발",
            "팀원 수": "N명"
        })
        
        # CLI 인터페이스 실행
        ui = TaipanChatUI(assistant)
        ui.run()
        
    except ValueError as e:
        print(f"❌ 설정 오류: {str(e)}")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        logger.exception("Unexpected error")


if __name__ == "__main__":
    main()
