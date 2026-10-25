"""
Taipan AI Assistant - 테스트 및 데모
"""

from taipan_ai_chat import TaipanAIAssistant
import json


def test_kpi_analysis():
    """KPI 분석 테스트"""
    print("\n" + "="*50)
    print("🧪 KPI 분석 테스트")
    print("="*50)
    
    # 하드코딩된 KPI 데이터로 테스트 (API 키 불필요)
    kpi_data = {
        "업무 생산성 향상": 85,
        "프로젝트 가시성 확보": 72,
        "KPI 달성 지원": 68,
        "문서화 자동화": 90,
        "지식 축적": 75,
        "협업 품질 향상": 80,
        "반복업무 최소화": 70,
        "리스크 조기 발견": 45
    }
    
    print("\n📊 KPI 현황:")
    green_count = 0
    yellow_count = 0
    red_count = 0
    
    for kpi_name, value in kpi_data.items():
        if value >= 80:
            status = "🟢 GREEN"
            green_count += 1
        elif value >= 50:
            status = "🟡 YELLOW"
            yellow_count += 1
        else:
            status = "🔴 RED"
            red_count += 1
        
        print(f"{status} {kpi_name:20s} {value:3d}%")
    
    avg = sum(kpi_data.values()) / len(kpi_data)
    print(f"\n📈 평균: {avg:.1f}%")
    print(f"🟢 Green: {green_count}개 | 🟡 Yellow: {yellow_count}개 | 🔴 Red: {red_count}개")
    
    # 리스크 분석
    critical_kpis = [k for k, v in kpi_data.items() if v < 50]
    if critical_kpis:
        print(f"\n⚠️  긴급 주의: {', '.join(critical_kpis)}")
    
    return kpi_data


def test_weekly_report_structure():
    """주간 보고서 구조 테스트"""
    print("\n" + "="*50)
    print("📋 주간 보고서 구조 테스트")
    print("="*50)
    
    report_template = {
        "metadata": {
            "week": "2026-10-20 ~ 2026-10-26",
            "reporter": "[팀원명]",
            "status": "작성중"
        },
        "sections": [
            "주간 요약",
            "완료 사항",
            "진행 중",
            "지연 사항",
            "KPI 연계",
            "학습 및 개선",
            "다음주 계획",
            "이슈 및 리스크",
            "협업 현황",
            "성과 지표"
        ],
        "kpi_contributions": {
            "업무 생산성 향상": "+3%",
            "프로젝트 가시성 확보": "+2%",
            "리스크 조기 발견": "+2%"
        }
    }
    
    print("\n📑 보고서 섹션:")
    for i, section in enumerate(report_template["sections"], 1):
        print(f"{i:2d}. {section}")
    
    print("\n💰 KPI 기여도:")
    for kpi, contribution in report_template["kpi_contributions"].items():
        print(f"   {kpi:20s} {contribution:>4s}")
    
    return report_template


def test_risk_analysis():
    """리스크 분석 테스트"""
    print("\n" + "="*50)
    print("🚨 리스크 분석 테스트")
    print("="*50)
    
    risks = [
        {
            "id": "risk_001",
            "title": "리스크 조기 발견 체계 부족",
            "impact": "높음",
            "probability": 0.7,
            "severity": "높음",
            "mitigation": "리스크 대시보드 구축, 주간 검토 미팅"
        },
        {
            "id": "risk_002",
            "title": "프로젝트 일정 지연 가능성",
            "impact": "중간",
            "probability": 0.5,
            "severity": "중간",
            "mitigation": "리소스 재배치, 우선순위 조정"
        },
        {
            "id": "risk_003",
            "title": "팀원 업무 과부하",
            "impact": "중간",
            "probability": 0.4,
            "severity": "중간",
            "mitigation": "업무 분배 재검토, 자동화 추진"
        }
    ]
    
    print("\n위험 등급별 분류:")
    
    high_risks = [r for r in risks if r["severity"] == "높음"]
    medium_risks = [r for r in risks if r["severity"] == "중간"]
    low_risks = [r for r in risks if r["severity"] == "낮음"]
    
    print(f"\n🔴 높음 위험: {len(high_risks)}개")
    for risk in high_risks:
        print(f"   - {risk['title']}")
        print(f"     확률: {risk['probability']*100:.0f}% | 대응: {risk['mitigation']}")
    
    print(f"\n🟡 중간 위험: {len(medium_risks)}개")
    for risk in medium_risks:
        print(f"   - {risk['title']}")
        print(f"     확률: {risk['probability']*100:.0f}% | 대응: {risk['mitigation']}")
    
    print(f"\n⚪ 낮은 위험: {len(low_risks)}개")
    
    return risks


def test_automation_suggestions():
    """자동화 제안 테스트"""
    print("\n" + "="*50)
    print("🤖 자동화 기회 분석 테스트")
    print("="*50)
    
    automation_opportunities = [
        {
            "task": "주간 보고서 데이터 수집",
            "frequency": "주 1회",
            "time_saved_per_week": 2.0,
            "complexity": "낮음",
            "priority": "높음",
            "tools": ["Power Automate", "Zapier", "IFTTT"]
        },
        {
            "task": "KPI 계산 및 집계",
            "frequency": "매일",
            "time_saved_per_week": 5.0,
            "complexity": "중간",
            "priority": "높음",
            "tools": ["Python 스크립트", "Power BI", "Tableau"]
        },
        {
            "task": "Teams 알림 발송",
            "frequency": "주 3회",
            "time_saved_per_week": 1.5,
            "complexity": "낮음",
            "priority": "중간",
            "tools": ["Teams Webhook", "Power Automate"]
        },
        {
            "task": "문서 자동 생성",
            "frequency": "월 1회",
            "time_saved_per_week": 4.0,
            "complexity": "높음",
            "priority": "높음",
            "tools": ["Python", "Docx", "Markdown Generator"]
        }
    ]
    
    print("\n⏱️  시간 절감 기회 (주간):")
    total_hours = 0
    
    for opp in sorted(automation_opportunities, 
                       key=lambda x: x["time_saved_per_week"], 
                       reverse=True):
        priority = "🔴" if opp["priority"] == "높음" else "🟡"
        print(f"{priority} {opp['task']:25s} {opp['time_saved_per_week']:>3.1f}시간")
        total_hours += opp["time_saved_per_week"]
    
    print(f"\n총 절감 가능 시간: {total_hours}시간/주 = {total_hours*52:.0f}시간/년")
    
    print("\n💡 추천 우선순위:")
    high_priority = [o for o in automation_opportunities if o["priority"] == "높음"]
    for i, opp in enumerate(high_priority, 1):
        print(f"{i}. {opp['task']} ({opp['complexity']} 난이도)")
        print(f"   권장 도구: {', '.join(opp['tools'])}")
    
    return automation_opportunities


def test_team_collaboration():
    """팀 협업 분석 테스트"""
    print("\n" + "="*50)
    print("👥 팀 협업 분석 테스트")
    print("="*50)
    
    team_data = {
        "전체 팀원": 10,
        "미팅 참석률": 95,
        "피드백 응답시간": "평균 2시간",
        "협업 도구 사용률": 85,
        "만족도": 4.5,
        "강점": [
            "높은 팀 응집력",
            "빠른 커뮤니케이션",
            "적극적인 참여"
        ],
        "개선 영역": [
            "문서화 체계",
            "역할 명확화",
            "지식 공유 활성화"
        ]
    }
    
    print(f"\n📊 팀 협업 지표:")
    print(f"   팀원 수: {team_data['전체 팀원']}명")
    print(f"   미팅 참석률: {team_data['미팅 참석률']}%")
    print(f"   피드백 응답시간: {team_data['피드백 응답시간']}")
    print(f"   도구 사용률: {team_data['협업 도구 사용률']}%")
    print(f"   만족도: {team_data['만족도']:.1f}/5.0 ⭐")
    
    print(f"\n💪 팀의 강점:")
    for strength in team_data["강점"]:
        print(f"   ✅ {strength}")
    
    print(f"\n🎯 개선 영역:")
    for improvement in team_data["개선 영역"]:
        print(f"   📌 {improvement}")
    
    return team_data


def generate_summary_report():
    """종합 요약 리포트 생성"""
    print("\n" + "="*50)
    print("📊 Taipan 주간 종합 리포트")
    print("="*50)
    
    # 데이터 수집
    kpi_data = test_kpi_analysis()
    report_data = test_weekly_report_structure()
    risks = test_risk_analysis()
    automations = test_automation_suggestions()
    team_data = test_team_collaboration()
    
    # 최종 요약
    print("\n\n" + "="*50)
    print("📈 주간 종합 분석")
    print("="*50)
    
    avg_kpi = sum(kpi_data.values()) / len(kpi_data)
    print(f"\n🎯 전체 KPI 평균: {avg_kpi:.1f}%")
    
    if avg_kpi >= 80:
        status = "🟢 우수"
    elif avg_kpi >= 50:
        status = "🟡 주의"
    else:
        status = "🔴 긴급"
    
    print(f"   상태: {status}")
    
    print(f"\n⚠️  주요 이슈:")
    print(f"   - 리스크 조기 발견이 가장 낮음 (45%)")
    print(f"   - 프로젝트 가시성도 개선 필요 (72%)")
    
    print(f"\n💡 권장 액션:")
    print(f"   1. 리스크 대시보드 즉시 구축")
    print(f"   2. 주간 리스크 검토 미팅 실시")
    print(f"   3. 자동화로 {sum(o['time_saved_per_week'] for o in automations):.1f}시간/주 절감")
    
    print(f"\n✅ 우점 유지:")
    print(f"   - 문서화 자동화: 90% (계획대로 진행)")
    print(f"   - 협업 품질: 80% (현 상태 유지)")
    
    # JSON 형식으로 저장
    summary = {
        "timestamp": "2026-10-26T10:00:00Z",
        "week": "2026-10-20 ~ 2026-10-26",
        "overall_kpi": avg_kpi,
        "status": status,
        "kpi_summary": kpi_data,
        "risk_summary": {
            "total_risks": len(risks),
            "high_priority": len([r for r in risks if r["severity"] == "높음"]),
            "medium_priority": len([r for r in risks if r["severity"] == "중간"])
        },
        "automation_summary": {
            "total_opportunities": len(automations),
            "weekly_time_savings": sum(a["time_saved_per_week"] for a in automations),
            "yearly_time_savings": sum(a["time_saved_per_week"] for a in automations) * 52
        },
        "team_satisfaction": team_data["만족도"]
    }
    
    print("\n\n📄 JSON 형식 요약:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    return summary


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════╗
║   🧪 Taipan AI Assistant - Test Suite     ║
║   Demo & Testing Module                   ║
╚════════════════════════════════════════════╝
    """)
    
    # 모든 테스트 실행
    generate_summary_report()
    
    print("\n\n" + "="*50)
    print("✅ 모든 테스트 완료")
    print("="*50)
    print("\n다음 단계:")
    print("1. API 키 설정: COPILOT_API_KEY 환경변수 설정")
    print("2. 채팅 시작: python taipan_ai_chat.py")
    print("3. 문서 참고: AI-CHAT-GUIDE.md 읽기")
