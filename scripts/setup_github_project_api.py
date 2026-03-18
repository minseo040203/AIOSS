#!/usr/bin/env python3
"""
GitHub API를 사용한 프로젝트 설정 스크립트
PyGithub 라이브러리로 라벨, 마일스톤, 이슈를 생성합니다.
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from github import Github
except ImportError:
    print("❌ PyGithub 라이브러리가 필요합니다")
    print("   설치: pip install PyGithub")
    exit(1)


class GitHubProjectSetupAPI:
    def __init__(self):
        # GitHub 토큰 설정 (환경 변수 또는 설정 파일에서)
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print("❌ GITHUB_TOKEN 환경 변수가 설정되어있지 않습니다.")
            print("   설정 방법:")
            print("   Windows: $env:GITHUB_TOKEN='your_token'")
            print("   Linux/Mac: export GITHUB_TOKEN='your_token'")
            exit(1)
        
        self.github = Github(token)
        self.repo = self.github.get_user("minseo040203").get_repo("AIOSS")
        print(f"✓ {self.repo.full_name} 저장소 연결 성공\n")
    
    # ============================================================================
    # 라벨 생성
    # ============================================================================
    def create_labels(self):
        """라벨 체계 생성"""
        print("📌 라벨 체계 생성 중...")
        
        labels = {
            # 우선순위
            "priority/critical": {"color": "FF0000", "description": "긴급 - 즉시 작업 필요"},
            "priority/high": {"color": "FF6B00", "description": "높음 - 다음 스프린트에 포함"},
            "priority/medium": {"color": "FFD700", "description": "중간 - 계획에 포함"},
            "priority/low": {"color": "90EE90", "description": "낮음 - 백로그에 유지"},
            
            # 타입
            "type/bug": {"color": "FC2929", "description": "버그 수정"},
            "type/feature": {"color": "0099FF", "description": "새 기능"},
            "type/enhancement": {"color": "3366FF", "description": "기존 기능 개선"},
            "type/documentation": {"color": "0366D6", "description": "문서 작업"},
            "type/refactor": {"color": "6B42BC", "description": "코드 리팩토링"},
            "type/test": {"color": "FFA500", "description": "테스트 추가"},
            
            # 상태
            "status/backlog": {"color": "CCCCCC", "description": "백로그"},
            "status/ready": {"color": "E0E0E0", "description": "작업 준비됨"},
            "status/in-progress": {"color": "B3D4FF", "description": "진행 중"},
            "status/review": {"color": "FFD4D4", "description": "리뷰 대기"},
            "status/blocked": {"color": "FF0000", "description": "블로킹됨"},
            
            # 영역
            "area/ai-core": {"color": "1F6FEB", "description": "AI 코어 로직"},
            "area/rag-system": {"color": "0969DA", "description": "RAG 시스템"},
            "area/ui-ux": {"color": "A371F7", "description": "UI/UX"},
            "area/infrastructure": {"color": "1A7F34", "description": "인프라"},
            "area/documentation": {"color": "256045", "description": "문서"},
            
            # 스프린트-관련
            "sprint/essential": {"color": "FF6B35", "description": "스프린트 필수"},
            "sprint/nice-to-have": {"color": "F7931E", "description": "있으면 좋은(선택사항)"},
            
            # 기타
            "good-first-issue": {"color": "7057FF", "description": "초보자 친화적"},
            "help-wanted": {"color": "0E7C86", "description": "도움 필요"},
            "wontfix": {"color": "FFFFFF", "description": "해결 안 함"},
        }
        
        created = 0
        updated = 0
        
        for label_name, label_info in labels.items():
            try:
                # 기존 라벨 업데이트
                label = self.repo.get_label(label_name)
                label.edit(
                    name=label_name,
                    color=label_info["color"],
                    description=label_info["description"]
                )
                updated += 1
                print(f"  ✓ '{label_name}' 업데이트")
            except:
                # 새 라벨 생성
                try:
                    self.repo.create_label(
                        name=label_name,
                        color=label_info["color"],
                        description=label_info["description"]
                    )
                    created += 1
                    print(f"  ✓ '{label_name}' 생성")
                except Exception as e:
                    print(f"  ⚠ '{label_name}' 생성 실패: {e}")
        
        print(f"✅ 라벨 설정 완료 ({created} 생성, {updated} 업데이트)\n")
    
    # ============================================================================
    # 마일스톤 생성
    # ============================================================================
    def create_milestones(self):
        """마일스톤 생성"""
        print("🎯 마일스톤 생성 중...")
        
        milestones = [
            {
                "title": "Sprint 1: AI Core 구축",
                "description": "로컬 LLM 및 기본 RAG 시스템 구축",
                "due_date": datetime.now() + timedelta(days=30)
            },
            {
                "title": "Sprint 2: UI 및 통합",
                "description": "웹 인터페이스 개발 및 전체 시스템 통합",
                "due_date": datetime.now() + timedelta(days=60)
            }
        ]
        
        created = 0
        
        # 기존 마일스톤 얻기
        existing_milestones = {m.title for m in self.repo.get_milestones()}
        
        for ms in milestones:
            if ms["title"] not in existing_milestones:
                try:
                    self.repo.create_milestone(
                        title=ms["title"],
                        description=ms["description"],
                        due_on=ms["due_date"]
                    )
                    created += 1
                    print(f"  ✓ '{ms['title']}' 마일스톤 생성")
                except Exception as e:
                    print(f"  ⚠ '{ms['title']}' 생성 실패: {e}")
            else:
                print(f"  ✓ '{ms['title']}' 이미 존재함")
        
        print(f"✅ 마일스톤 설정 완료 ({created} 생성)\n")
    
    # ============================================================================
    # 이슈 생성
    # ============================================================================
    def create_issues(self):
        """이슈 생성"""
        print("📝 이슈 생성 중...")
        
        issues = [
            # Sprint 1 - 필수
            {
                "title": "Llama 모델 Raspberry Pi에 통합",
                "body": "## 📋 작성 내용\nRaspberry Pi에서 Llama 모델 실행 환경 구축\n\n## ✅ 수락 기준\n- Ollama 설치 및 실행 확인\n- 메모리 최적화 완료\n- 응답 시간 < 5초 달성",
                "labels": ["type/feature", "area/ai-core", "priority/critical", "sprint/essential"],
                "milestone": "Sprint 1: AI Core 구축"
            },
            {
                "title": "ChromaDB 벡터 데이터베이스 구성",
                "body": "## 📋 작성 내용\nChromaDB를 사용한 벡터 데이터베이스 설계 및 구현\n\n## ✅ 수락 기준\n- ChromaDB 초기화 및 설정 완료\n- 벡터 저장 및 검색 기능 테스트",
                "labels": ["type/feature", "area/rag-system", "priority/high", "sprint/essential"],
                "milestone": "Sprint 1: AI Core 구축"
            },
            {
                "title": "재난 안전 정보 데이터셋 구축",
                "body": "## 📋 작성 내용\n재난 상황에 대한 안전 정보 데이터셋 수집 및 정제\n\n## ✅ 수락 기준\n- 최소 1000개 문서 수집\n- 데이터 품질 검증 완료",
                "labels": ["type/feature", "area/rag-system", "priority/high", "sprint/essential"],
                "milestone": "Sprint 1: AI Core 구축"
            },
            {
                "title": "LangChain RAG 파이프라인 구현",
                "body": "## 📋 작성 내용\nLangChain을 사용한 RAG 쿼리 파이프라인 구현\n\n## ✅ 수락 기준\n- 쿼리 입력 → 검색 → 응답 생성 완성\n- 관련도 높은 문서 검색 기능 검증",
                "labels": ["type/feature", "area/rag-system", "priority/critical", "sprint/essential"],
                "milestone": "Sprint 1: AI Core 구축"
            },
            {
                "title": "오프라인 환경에서 모델 동작 테스트",
                "body": "## 📋 작성 내용\n인터넷 연결 없이 모델이 정상 동작하는지 검증\n\n## ✅ 수락 기준\n- 오프라인 모드에서 완전히 동작\n- 모든 기능 작동 검증",
                "labels": ["type/test", "area/ai-core", "priority/high", "sprint/essential"],
                "milestone": "Sprint 1: AI Core 구축"
            },
            
            # Sprint 2 - 필수
            {
                "title": "FastAPI 웹 서버 개발",
                "body": "## 📋 작성 내용\nFastAPI를 사용한 REST API 서버 구현\n\n## ✅ 수락 기준\n- POST /query 엔드포인트 구현\n- GET /health 상태 확인 엔드포인트 구현\n- API 문서 자동 생성",
                "labels": ["type/feature", "area/ui-ux", "priority/high", "sprint/essential"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "웹 대시보드 UI 구현",
                "body": "## 📋 작성 내용\n사용자 친화적 웹 대시보드 개발\n\n## ✅ 수락 기준\n- 쿼리 입력 폼 구현\n- 응답 결과 표시\n- 반응형 디자인 적용",
                "labels": ["type/feature", "area/ui-ux", "priority/high", "sprint/essential"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            
            # 추가 기능 개선
            {
                "title": "다국어 지원 (한글, 영어) 추가",
                "body": "## 📋 작성 내용\n시스템이 한글과 영어를 모두 지원하도록 구현\n\n## ✅ 수락 기준\n- 한글 쿼리 처리\n- 영어 쿼리 처리\n- 언어 자동 감지",
                "labels": ["type/enhancement", "area/ui-ux", "priority/medium", "sprint/nice-to-have"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "응답 시간 최적화 및 벤치마크",
                "body": "## 📋 작성 내용\n시스템 응답 시간 개선 및 성능 측정\n\n## ✅ 수락 기준\n- 평균 응답 시간 < 3초 달성\n- 벤치마크 리포트 작성",
                "labels": ["type/refactor", "area/ai-core", "priority/medium"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "사용자 피드백 로깅 시스템",
                "body": "## 📋 작성 내용\n사용자의 피드백을 수집하여 모델 개선에 활용\n\n## ✅ 수락 기준\n- 피드백 저장 기능 구현\n- 피드백 분석 대시보드",
                "labels": ["type/feature", "area/ui-ux", "priority/low"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "배포 자동화 스크립트 작성",
                "body": "## 📋 작성 내용\nRaspberry Pi에 자동 배포하는 스크립트 구현\n\n## ✅ 수락 기준\n- 배포 스크립트 작동 검증\n- 배포 문서 작성",
                "labels": ["type/feature", "area/infrastructure", "priority/high"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "통합 테스트 스위트 구축",
                "body": "## 📋 작성 내용\n전체 시스템의 통합 테스트 작성\n\n## ✅ 수락 기준\n- 주요 기능 테스트 커버리지 > 80%\n- CI/CD 파이프라인 연동",
                "labels": ["type/test", "area/infrastructure", "priority/high"],
                "milestone": "Sprint 2: UI 및 통합"
            },
            {
                "title": "프로젝트 문서 및 튜토리얼 작성",
                "body": "## 📋 작성 내용\n설치, 사용, 개발 관련 상세 문서 작성\n\n## ✅ 수락 기준\n- 설치 가이드 완성\n- 사용 튜토리얼 작성\n- API 문서 작성",
                "labels": ["type/documentation", "area/documentation", "priority/medium"],
                "milestone": "Sprint 2: UI 및 통합"
            },
        ]
        
        created = 0
        
        # 기존 이콘 제목 얻기
        existing_titles = {issue.title for issue in self.repo.get_issues(state='all')}
        
        for issue in issues:
            if issue["title"] not in existing_titles:
                try:
                    # 마일스톤 ID 얻기
                    milestone = None
                    if issue.get("milestone"):
                        try:
                            for m in self.repo.get_milestones():
                                if m.title == issue["milestone"]:
                                    milestone = m
                                    break
                        except:
                            pass
                    
                    # 이슈 생성
                    new_issue = self.repo.create_issue(
                        title=issue["title"],
                        body=issue["body"],
                        milestone=milestone
                    )
                    
                    # 라벨 추가
                    if issue.get("labels"):
                        labels_objects = []
                        for label_name in issue["labels"]:
                            try:
                                labels_objects.append(self.repo.get_label(label_name))
                            except:
                                pass
                        if labels_objects:
                            new_issue.add_to_labels(*labels_objects)
                    
                    created += 1
                    print(f"  ✓ Issue: {issue['title']}")
                except Exception as e:
                    print(f"  ⚠ 생성 실패 '{issue['title']}': {e}")
            else:
                print(f"  ✓ Issue: {issue['title']} (이미 존재)")
        
        print(f"✅ 이슈 설정 완료 ({created} 생성)\n")
    
    def run_all(self):
        """모든 설정 실행"""
        print("=" * 70)
        print("🚀 GitHub Project 스프린트 설정 시작")
        print("=" * 70 + "\n")
        
        try:
            self.create_labels()
            self.create_milestones()
            self.create_issues()
            
            print("=" * 70)
            print("✅ 모든 설정이 완료되었습니다!")
            print("=" * 70)
            print("\n📊 다음 단계:")
            print("1. GitHub 저장소로 이동: https://github.com/minseo040203/AIOSS")
            print("2. 'Projects' 탭에서 칸반 프로젝트 생성")
            print("3. 생성된 이슈들을 프로젝트 칸반 보드에 추가")
            print("4. 메트릭 수집 스크립트 실행: python scripts/collect_metrics.py")
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            raise


def main():
    setup = GitHubProjectSetupAPI()
    setup.run_all()


if __name__ == "__main__":
    main()
