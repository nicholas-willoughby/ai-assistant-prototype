"""
Taipan AI Assistant - Calendar Integration Module
MS Outlook & Google Calendar 연동 모듈

주요 기능:
- Google Calendar API 연동
- MS Outlook Calendar API 연동
- 오늘의 일정 조회
- AI Assistant에 일정 정보 제공
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalendarProvider(ABC):
    """달력 제공자 추상 클래스"""
    
    @abstractmethod
    def get_today_events(self) -> List[Dict[str, Any]]:
        """오늘의 일정 조회"""
        pass
    
    @abstractmethod
    def get_events_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """특정 기간의 일정 조회"""
        pass
    
    @abstractmethod
    def authenticate(self) -> bool:
        """인증"""
        pass


class GoogleCalendarProvider(CalendarProvider):
    """Google Calendar API 제공자"""
    
    def __init__(self, credentials_file: str = "google_credentials.json"):
        """
        Initialize Google Calendar Provider
        
        Args:
            credentials_file: Google OAuth 인증 파일 경로
        """
        self.credentials_file = credentials_file
        self.service = None
        self.authenticated = False
        self.calendar_id = "primary"  # 기본 달력
        
    def authenticate(self) -> bool:
        """
        Google Calendar API 인증
        
        세팅 방법:
        1. Google Cloud Console에서 프로젝트 생성
        2. Calendar API 활성화
        3. OAuth 2.0 클라이언트 ID 생성
        4. 인증 파일 다운로드 후 google_credentials.json으로 저장
        
        참고: https://developers.google.com/calendar/api/quickstart/python
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from google.oauth2 import service_account
            from google_auth_oauthlib.flow import InstalledAppFlow
            import google.auth
            from googleapiclient.discovery import build
        except ImportError:
            logger.error("Google API 라이브러리 필요: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return False
        
        try:
            # 인증 파일 확인
            if not os.path.exists(self.credentials_file):
                logger.error(f"인증 파일 없음: {self.credentials_file}")
                return False
            
            # OAuth 2.0 flow로 인증
            SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Calendar API 클라이언트 생성
            self.service = build('calendar', 'v3', credentials=creds)
            self.authenticated = True
            logger.info("✅ Google Calendar 인증 성공")
            return True
            
        except Exception as e:
            logger.error(f"Google Calendar 인증 실패: {str(e)}")
            return False
    
    def get_today_events(self) -> List[Dict[str, Any]]:
        """오늘의 일정 조회"""
        if not self.authenticated:
            if not self.authenticate():
                return []
        
        try:
            # 오늘 날짜
            today = datetime.utcnow().date()
            time_min = datetime.combine(today, datetime.min.time()).isoformat() + 'Z'
            time_max = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'
            
            # API 호출
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=20,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # 형식 변환
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'provider': 'Google Calendar',
                    'id': event.get('id'),
                    'title': event.get('summary', '(제목 없음)'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                    'location': event.get('location', ''),
                    'description': event.get('description', ''),
                    'attendees': len(event.get('attendees', [])),
                    'url': event.get('htmlLink', '')
                })
            
            logger.info(f"✅ Google Calendar에서 {len(formatted_events)}개 일정 조회")
            return formatted_events
            
        except Exception as e:
            logger.error(f"Google Calendar 일정 조회 실패: {str(e)}")
            return []
    
    def get_events_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """특정 기간의 일정 조회"""
        if not self.authenticated:
            if not self.authenticate():
                return []
        
        try:
            time_min = start_date.isoformat() + 'Z'
            time_max = end_date.isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'provider': 'Google Calendar',
                    'id': event.get('id'),
                    'title': event.get('summary', '(제목 없음)'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                    'location': event.get('location', ''),
                    'description': event.get('description', ''),
                    'attendees': len(event.get('attendees', [])),
                    'url': event.get('htmlLink', '')
                })
            
            return formatted_events
            
        except Exception as e:
            logger.error(f"Google Calendar 기간 조회 실패: {str(e)}")
            return []


class OutlookCalendarProvider(CalendarProvider):
    """MS Outlook Calendar API 제공자"""
    
    def __init__(self, tenant_id: str = "common", client_id: str = "", client_secret: str = ""):
        """
        Initialize Outlook Calendar Provider
        
        Args:
            tenant_id: Azure Tenant ID
            client_id: Azure Application Client ID
            client_secret: Azure Application Client Secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """
        MS Outlook API 인증 (OAuth 2.0)
        
        세팅 방법:
        1. Azure Portal에서 앱 등록
        2. Calendar.Read 권한 추가
        3. Client ID와 Secret 생성
        4. 인증 코드 받기
        
        참고: https://learn.microsoft.com/en-us/graph/auth-v2-user
        """
        try:
            import requests
        except ImportError:
            logger.error("Requests 라이브러리 필요: pip install requests")
            return False
        
        try:
            # 1단계: 인증 코드 받기 (사용자가 수동으로 해야함)
            auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize"
            auth_params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'scope': 'Calendars.Read',
                'redirect_uri': 'http://localhost:8000/callback'
            }
            
            logger.info(f"🔗 다음 URL에서 인증 코드를 받으세요:")
            logger.info(f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in auth_params.items()])}")
            
            # 2단계: 인증 코드로 액세스 토큰 받기 (사용자가 코드 입력 후)
            auth_code = input("인증 코드 입력: ").strip()
            
            token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            token_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': auth_code,
                'redirect_uri': 'http://localhost:8000/callback',
                'grant_type': 'authorization_code',
                'scope': 'Calendars.Read'
            }
            
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()
            
            token_result = response.json()
            self.access_token = token_result.get('access_token')
            
            if self.access_token:
                self.authenticated = True
                logger.info("✅ Outlook Calendar 인증 성공")
                return True
            else:
                logger.error("액세스 토큰을 받지 못했습니다")
                return False
                
        except Exception as e:
            logger.error(f"Outlook Calendar 인증 실패: {str(e)}")
            return False
    
    def get_today_events(self) -> List[Dict[str, Any]]:
        """오늘의 일정 조회"""
        if not self.authenticated:
            if not self.authenticate():
                return []
        
        try:
            import requests
        except ImportError:
            logger.error("Requests 라이브러리 필요: pip install requests")
            return []
        
        try:
            # 오늘 날짜
            today = datetime.utcnow().date()
            tomorrow = today + timedelta(days=1)
            
            # Microsoft Graph API 호출
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # 필터: 오늘의 일정만
            filter_query = f"start/dateTime ge '{today.isoformat()}T00:00:00' and end/dateTime le '{tomorrow.isoformat()}T00:00:00'"
            
            url = f"https://graph.microsoft.com/v1.0/me/calendarview"
            params = {
                '$filter': filter_query,
                '$orderby': 'start/dateTime',
                '$top': 20
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            events_data = response.json()
            events = events_data.get('value', [])
            
            # 형식 변환
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'provider': 'Outlook Calendar',
                    'id': event.get('id'),
                    'title': event.get('subject', '(제목 없음)'),
                    'start': event.get('start', {}).get('dateTime', ''),
                    'end': event.get('end', {}).get('dateTime', ''),
                    'location': event.get('location', {}).get('displayName', ''),
                    'description': event.get('bodyPreview', ''),
                    'attendees': len(event.get('attendees', [])),
                    'organizer': event.get('organizer', {}).get('emailAddress', {}).get('name', '')
                })
            
            logger.info(f"✅ Outlook Calendar에서 {len(formatted_events)}개 일정 조회")
            return formatted_events
            
        except Exception as e:
            logger.error(f"Outlook Calendar 일정 조회 실패: {str(e)}")
            return []
    
    def get_events_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """특정 기간의 일정 조회"""
        if not self.authenticated:
            if not self.authenticate():
                return []
        
        try:
            import requests
        except ImportError:
            logger.error("Requests 라이브러리 필요: pip install requests")
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # 필터: 지정된 기간의 일정
            filter_query = f"start/dateTime ge '{start_date.isoformat()}' and end/dateTime le '{end_date.isoformat()}'"
            
            url = f"https://graph.microsoft.com/v1.0/me/calendarview"
            params = {
                '$filter': filter_query,
                '$orderby': 'start/dateTime',
                '$top': 50
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            events_data = response.json()
            events = events_data.get('value', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'provider': 'Outlook Calendar',
                    'id': event.get('id'),
                    'title': event.get('subject', '(제목 없음)'),
                    'start': event.get('start', {}).get('dateTime', ''),
                    'end': event.get('end', {}).get('dateTime', ''),
                    'location': event.get('location', {}).get('displayName', ''),
                    'description': event.get('bodyPreview', ''),
                    'attendees': len(event.get('attendees', [])),
                    'organizer': event.get('organizer', {}).get('emailAddress', {}).get('name', '')
                })
            
            return formatted_events
            
        except Exception as e:
            logger.error(f"Outlook Calendar 기간 조회 실패: {str(e)}")
            return []


class CalendarAggregator:
    """여러 달력 제공자에서 일정을 집계하는 클래스"""
    
    def __init__(self):
        """Initialize Calendar Aggregator"""
        self.providers: List[CalendarProvider] = []
        
    def add_provider(self, provider: CalendarProvider, enable: bool = True) -> None:
        """달력 제공자 추가"""
        if enable:
            if provider.authenticate():
                self.providers.append(provider)
                logger.info(f"✅ 제공자 추가: {provider.__class__.__name__}")
            else:
                logger.warning(f"⚠️  제공자 인증 실패: {provider.__class__.__name__}")
        else:
            logger.info(f"⏭️  제공자 건너뜀: {provider.__class__.__name__}")
    
    def get_today_events(self) -> Dict[str, List[Dict[str, Any]]]:
        """모든 제공자에서 오늘의 일정 조회"""
        all_events = {}
        
        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                events = provider.get_today_events()
                all_events[provider_name] = events
            except Exception as e:
                logger.error(f"오류 ({provider_name}): {str(e)}")
                all_events[provider_name] = []
        
        return all_events
    
    def get_events_range(self, start_date: datetime, end_date: datetime) -> Dict[str, List[Dict[str, Any]]]:
        """모든 제공자에서 기간별 일정 조회"""
        all_events = {}
        
        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                events = provider.get_events_range(start_date, end_date)
                all_events[provider_name] = events
            except Exception as e:
                logger.error(f"오류 ({provider_name}): {str(e)}")
                all_events[provider_name] = []
        
        return all_events
    
    def format_for_ai(self, events: Dict[str, List[Dict[str, Any]]]) -> str:
        """AI Assistant를 위해 일정을 포맷팅"""
        formatted = "📅 **오늘의 일정**\n\n"
        
        total_events = 0
        
        for provider_name, event_list in events.items():
            if event_list:
                formatted += f"### {provider_name}\n"
                
                for i, event in enumerate(event_list, 1):
                    formatted += f"\n**{i}. {event['title']}**\n"
                    
                    # 시간
                    start_time = event.get('start', '').split('T')[1][:5] if 'T' in event.get('start', '') else event.get('start', '')
                    end_time = event.get('end', '').split('T')[1][:5] if 'T' in event.get('end', '') else event.get('end', '')
                    
                    if start_time and end_time:
                        formatted += f"   🕐 {start_time} ~ {end_time}\n"
                    
                    # 위치
                    if event.get('location'):
                        formatted += f"   📍 위치: {event['location']}\n"
                    
                    # 참가자
                    if event.get('attendees', 0) > 0:
                        formatted += f"   👥 참가자: {event['attendees']}명\n"
                    
                    # 설명
                    if event.get('description'):
                        desc = event['description'][:100]  # 처음 100자만
                        formatted += f"   📝 {desc}...\n" if len(event['description']) > 100 else f"   📝 {desc}\n"
                    
                    total_events += 1
                
                formatted += "\n"
        
        if total_events == 0:
            formatted += "오늘은 일정이 없습니다! ✨\n"
        else:
            formatted += f"\n**총 {total_events}개의 일정**\n"
        
        return formatted
    
    def save_events_json(self, events: Dict[str, List[Dict[str, Any]]], filepath: str) -> None:
        """일정을 JSON 파일로 저장"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'events': events
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 일정이 저장되었습니다: {filepath}")


# AI Assistant와 통합하기 위한 헬퍼 함수
def get_calendar_context_for_ai() -> str:
    """AI Assistant를 위한 현재 일정 컨텍스트 생성"""
    aggregator = CalendarAggregator()
    
    # 환경 변수에서 설정 읽기
    google_enabled = os.environ.get("GOOGLE_CALENDAR_ENABLED", "false").lower() == "true"
    outlook_enabled = os.environ.get("OUTLOOK_CALENDAR_ENABLED", "false").lower() == "true"
    
    # Google Calendar 추가
    if google_enabled:
        google_calendar = GoogleCalendarProvider()
        aggregator.add_provider(google_calendar)
    
    # Outlook Calendar 추가
    if outlook_enabled:
        outlook_calendar = OutlookCalendarProvider(
            tenant_id=os.environ.get("OUTLOOK_TENANT_ID", "common"),
            client_id=os.environ.get("OUTLOOK_CLIENT_ID", ""),
            client_secret=os.environ.get("OUTLOOK_CLIENT_SECRET", "")
        )
        aggregator.add_provider(outlook_calendar)
    
    # 오늘의 일정 조회
    events = aggregator.get_today_events()
    
    # AI 형식으로 포맷팅
    calendar_context = aggregator.format_for_ai(events)
    
    return calendar_context


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════╗
║   📅 Taipan Calendar Integration          ║
║   Google Calendar & Outlook Connector     ║
╚════════════════════════════════════════════╝
    """)
    
    # 테스트: 환경 변수 설정 필요
    # GOOGLE_CALENDAR_ENABLED=true
    # OUTLOOK_CALENDAR_ENABLED=true
    # OUTLOOK_TENANT_ID=xxx
    # OUTLOOK_CLIENT_ID=xxx
    # OUTLOOK_CLIENT_SECRET=xxx
    
    print("📖 설정 방법:")
    print("\n1. Google Calendar:")
    print("   - google_credentials.json 파일 필요")
    print("   - GOOGLE_CALENDAR_ENABLED=true")
    print("\n2. Outlook Calendar:")
    print("   - OUTLOOK_CALENDAR_ENABLED=true")
    print("   - OUTLOOK_TENANT_ID, CLIENT_ID, CLIENT_SECRET")
    print("\n📚 예제:\n")
    
    # 예제 (실제 인증 없이)
    print("""
from calendar_integration import CalendarAggregator, GoogleCalendarProvider, OutlookCalendarProvider

# 집계기 생성
aggregator = CalendarAggregator()

# Google Calendar 추가
google = GoogleCalendarProvider()
aggregator.add_provider(google)

# Outlook Calendar 추가
outlook = OutlookCalendarProvider(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
aggregator.add_provider(outlook)

# 오늘의 일정 조회
events = aggregator.get_today_events()

# AI 형식으로 포맷팅
formatted = aggregator.format_for_ai(events)
print(formatted)

# JSON으로 저장
aggregator.save_events_json(events, "today_events.json")
    """)
