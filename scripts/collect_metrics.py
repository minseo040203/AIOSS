#!/usr/bin/env python3
"""
GitHub 스프린트 메트릭 수집 및 분석 스크립트
Cycle Time, Velocity, Burndown Chart를 계산합니다.
"""

import json
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
import statistics

class GitHubMetricsCollector:
    def __init__(self, owner: str = "minseo040203", repo: str = "AIOSS"):
        self.owner = owner
        self.repo = repo
        self.issues = []
        self.pull_requests = []
        
    def run_command(self, cmd: str) -> str:
        """GitHub CLI 명령 실행"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️  경고: {result.stderr}")
            return result.stdout.strip()
        except Exception as e:
            print(f"❌ 오류: {e}")
            return ""
    
    # ============================================================================
    # 데이터 수집
    # ============================================================================
    def fetch_issues(self) -> List[Dict]:
        """모든 이슈 가져오기"""
        print("📥 이슈 데이터 수집 중...")
        
        cmd = (
            f'gh issue list --repo {self.owner}/{self.repo} '
            f'--state all --limit 100 --json '
            f'number,title,state,createdAt,updatedAt,closedAt,milestone,labels'
        )
        
        output = self.run_command(cmd)
        if not output:
            print("  ⚠️  이슈를 불러올 수 없음")
            return []
        
        try:
            self.issues = json.loads(output)
            print(f"  ✓ {len(self.issues)}개 이슈 로드 완료")
            return self.issues
        except json.JSONDecodeError:
            print("  ⚠️  JSON 파싱 오류")
            return []
    
    def fetch_pull_requests(self) -> List[Dict]:
        """모든 PR 가져오기"""
        print("📥 Pull Request 데이터 수집 중...")
        
        cmd = (
            f'gh pr list --repo {self.owner}/{self.repo} '
            f'--state all --limit 100 --json '
            f'number,title,state,createdAt,updatedAt,mergedAt,reviews,labels'
        )
        
        output = self.run_command(cmd)
        if not output:
            print("  ⚠️  PR을 불러올 수 없음")
            return []
        
        try:
            self.pull_requests = json.loads(output)
            print(f"  ✓ {len(self.pull_requests)}개 PR 로드 완료")
            return self.pull_requests
        except json.JSONDecodeError:
            print("  ⚠️  JSON 파싱 오류")
            return []
    
    # ============================================================================
    # Cycle Time 계산
    # ============================================================================
    def calculate_cycle_time(self) -> Dict[str, float]:
        """Cycle Time 계산
        (시간 = close까지 걸린 시간)
        """
        print("\n⏱️  Cycle Time 계산 중...")
        
        cycle_times = []
        
        for issue in self.issues:
            if issue['state'] == 'CLOSED' and issue['closedAt']:
                created = datetime.fromisoformat(issue['createdAt'].replace('Z', '+00:00'))
                closed = datetime.fromisoformat(issue['closedAt'].replace('Z', '+00:00'))
                
                cycle_time_hours = (closed - created).total_seconds() / 3600
                cycle_times.append(cycle_time_hours)
        
        if not cycle_times:
            return {
                "count": 0,
                "average": 0,
                "median": 0,
                "min": 0,
                "max": 0,
                "std_dev": 0,
            }
        
        result = {
            "count": len(cycle_times),
            "average": statistics.mean(cycle_times),
            "median": statistics.median(cycle_times),
            "min": min(cycle_times),
            "max": max(cycle_times),
            "std_dev": statistics.stdev(cycle_times) if len(cycle_times) > 1 else 0,
        }
        
        print(f"  ✓ 평균 Cycle Time: {result['average']:.1f}시간")
        print(f"  ✓ 중앙값: {result['median']:.1f}시간")
        print(f"  ✓ 범위: {result['min']:.1f}h ~ {result['max']:.1f}h")
        
        return result
    
    # ============================================================================
    # Velocity 계산
    # ============================================================================
    def calculate_velocity(self) -> Dict[str, any]:
        """Velocity 계산
        (스프린트당 완료된 이슈 수)
        """
        print("\n🚀 Velocity 계산 중...")
        
        # 마일스톤별로 그룹화
        milestone_issues = defaultdict(lambda: {"total": 0, "closed": 0})
        
        for issue in self.issues:
            if issue['milestone']:
                milestone_name = issue['milestone']['title']
                milestone_issues[milestone_name]["total"] += 1
                
                if issue['state'] == 'CLOSED':
                    milestone_issues[milestone_name]["closed"] += 1
        
        # PR 기반 velocity도 계산
        pr_velocity = {
            "total_prs": len(self.pull_requests),
            "merged_prs": len([pr for pr in self.pull_requests if pr['state'] == 'MERGED']),
            "closed_prs": len([pr for pr in self.pull_requests if pr['state'] == 'CLOSED']),
        }
        
        result = {
            "by_milestone": dict(milestone_issues),
            "pr_metrics": pr_velocity,
            "current_velocity": pr_velocity['merged_prs'],  # 현재 속도는 merged PR 수
        }
        
        print(f"  ✓ 전체 생성 이슈: {sum(m['total'] for m in milestone_issues.values())}")
        print(f"  ✓ 완료된 이슈: {sum(m['closed'] for m in milestone_issues.values())}")
        print(f"  ✓ Merge된 PR: {pr_velocity['merged_prs']}/{pr_velocity['total_prs']}")
        
        return result
    
    # ============================================================================
    # Lead Time 계산
    # ============================================================================
    def calculate_lead_time(self) -> Dict[str, float]:
        """Lead Time 계산
        (PR 생성 ~ Merge까지 시간)
        """
        print("\n⚡ Lead Time 계산 중...")
        
        lead_times = []
        
        for pr in self.pull_requests:
            if pr['state'] == 'MERGED' and pr['mergedAt']:
                created = datetime.fromisoformat(pr['createdAt'].replace('Z', '+00:00'))
                merged = datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00'))
                
                lead_time_hours = (merged - created).total_seconds() / 3600
                lead_times.append(lead_time_hours)
        
        if not lead_times:
            return {
                "count": 0,
                "average": 0,
                "median": 0,
            }
        
        result = {
            "count": len(lead_times),
            "average": statistics.mean(lead_times),
            "median": statistics.median(lead_times),
            "min": min(lead_times),
            "max": max(lead_times),
        }
        
        print(f"  ✓ 평균 Lead Time: {result['average']:.1f}시간")
        print(f"  ✓ Merge된 PR: {len(lead_times)}개")
        
        return result
    
    # ============================================================================
    # Throughput 계산
    # ============================================================================
    def calculate_throughput(self) -> Dict[str, any]:
        """Throughput 계산
        (주/월별 완료 이슈 수)
        """
        print("\n📊 Throughput 계산 중...")
        
        # 일주일 단위로 그룹화
        weekly_closed = defaultdict(int)
        
        for issue in self.issues:
            if issue['state'] == 'CLOSED' and issue['closedAt']:
                closed_date = datetime.fromisoformat(
                    issue['closedAt'].replace('Z', '+00:00')
                )
                # 주의 시작일(월요일)을 기준으로
                week_start = closed_date - timedelta(days=closed_date.weekday())
                week_key = week_start.strftime("%Y-W%V")
                weekly_closed[week_key] += 1
        
        # 월별로도 그룹화
        monthly_closed = defaultdict(int)
        for issue in self.issues:
            if issue['state'] == 'CLOSED' and issue['closedAt']:
                closed_date = datetime.fromisoformat(
                    issue['closedAt'].replace('Z', '+00:00')
                )
                month_key = closed_date.strftime("%Y-%m")
                monthly_closed[month_key] += 1
        
        result = {
            "weekly": dict(sorted(weekly_closed.items())),
            "monthly": dict(sorted(monthly_closed.items())),
            "total_closed": len([i for i in self.issues if i['state'] == 'CLOSED']),
        }
        
        print(f"  ✓ 완료된 총 이슈: {result['total_closed']}개")
        if result['weekly']:
            avg_weekly = statistics.mean(result['weekly'].values())
            print(f"  ✓ 주당 평균: {avg_weekly:.1f}개")
        
        return result
    
    # ============================================================================
    # Burndown Chart 데이터
    # ============================================================================
    def generate_burndown_data(self, milestone: Optional[str] = None) -> Dict[str, any]:
        """Burndown Chart 데이터 생성"""
        print("\n📉 Burndown Chart 데이터 생성 중...")
        
        # 마일스톤별 이슈 필터링
        if milestone:
            milestone_issues = [
                i for i in self.issues
                if i['milestone'] and i['milestone']['title'] == milestone
            ]
        else:
            milestone_issues = self.issues
        
        total_issues = len(milestone_issues)
        
        if not milestone_issues:
            return {
                "milestone": milestone,
                "total_issues": 0,
                "closed_issues": 0,
                "remaining_issues": 0,
                "burndown_percentage": 0,
            }
        
        closed_issues = len([i for i in milestone_issues if i['state'] == 'CLOSED'])
        remaining = total_issues - closed_issues
        
        result = {
            "milestone": milestone,
            "total_issues": total_issues,
            "closed_issues": closed_issues,
            "remaining_issues": remaining,
            "burndown_percentage": (closed_issues / total_issues * 100) if total_issues > 0 else 0,
        }
        
        print(f"  ✓ {milestone or 'All'}: {closed_issues}/{total_issues} 완료 ({result['burndown_percentage']:.1f}%)")
        
        return result
    
    # ============================================================================
    # 레포트 생성
    # ============================================================================
    def generate_report(self) -> str:
        """종합 분석 리포트 생성"""
        
        print("\n" + "=" * 70)
        print("📊 스프린트 메트릭 분석 리포트")
        print("=" * 70)
        
        self.fetch_issues()
        self.fetch_pull_requests()
        
        cycle_time = self.calculate_cycle_time()
        velocity = self.calculate_velocity()
        lead_time = self.calculate_lead_time()
        throughput = self.calculate_throughput()
        
        # 마일스톤별 Burndown
        milestones_set = set()
        for issue in self.issues:
            if issue['milestone']:
                milestones_set.add(issue['milestone']['title'])
        
        burndown_data = []
        for milestone in sorted(milestones_set):
            burndown_data.append(self.generate_burndown_data(milestone))
        
        # JSON 리포트 생성
        report = {
            "generated_at": datetime.now().isoformat(),
            "repository": f"{self.owner}/{self.repo}",
            "metrics": {
                "cycle_time": cycle_time,
                "velocity": velocity,
                "lead_time": lead_time,
                "throughput": throughput,
                "burndown": burndown_data,
            },
            "summary": {
                "total_issues": len(self.issues),
                "closed_issues": len([i for i in self.issues if i['state'] == 'CLOSED']),
                "open_issues": len([i for i in self.issues if i['state'] == 'OPEN']),
                "total_prs": len(self.pull_requests),
                "merged_prs": len([pr for pr in self.pull_requests if pr['state'] == 'MERGED']),
            }
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def save_report(self, filename: str = "sprint_metrics.json"):
        """리포트를 파일로 저장"""
        report = self.generate_report()
        
        file_path = f"reports/{filename}"
        
        # reports 디렉토리가 없으면 생성
        import os
        os.makedirs("reports", exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 리포트 저장: {file_path}")
        return file_path


def main():
    """메인 함수"""
    print("🚀 GitHub 스프린트 메트릭 수집 시작\n")
    
    collector = GitHubMetricsCollector()
    
    try:
        collector.save_report()
        
        print("\n" + "=" * 70)
        print("✅ 메트릭 수집 완료!")
        print("=" * 70)
        print("\n📈 생성된 메트릭:")
        print("  • Cycle Time: 이슈 생성 → 종료까지 시간")
        print("  • Lead Time: PR 생성 → Merge까지 시간")
        print("  • Velocity: 마일스톤별 완료 이슈 수")
        print("  • Throughput: 기간별 완료 이슈 수")
        print("  • Burndown: 마일스톤별 진행 상황")
        print("\n📁 리포트 위치: reports/sprint_metrics.json")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()
