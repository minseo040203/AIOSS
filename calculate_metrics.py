#!/usr/bin/env python3
"""
Cycle Time Metrics Calculator
DORA 메트릭: Cycle Time 측정 및 분석
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import statistics


class CycleTimeCalculator:
    """Cycle Time 계산 및 분석"""
    
    def __init__(self, metrics_dir: str = '.github/metrics'):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
    def load_json_file(self, filename: str) -> List[Dict]:
        """JSON 파일 로드"""
        filepath = self.metrics_dir / filename
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def save_json_file(self, filename: str, data: Dict) -> None:
        """JSON 파일 저장"""
        filepath = self.metrics_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {filename}")
        except IOError as e:
            print(f"Error saving {filename}: {e}")
    
    def parse_datetime(self, dt_string: str) -> datetime:
        """ISO 8601 문자열을 datetime으로 변환"""
        try:
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    def calculate_cycle_time(self) -> Dict:
        """
        Cycle Time 계산
        Issue 생성 → 배포까지의 시간
        """
        print("\n📊 Calculating Cycle Time...")
        
        lead_time_metrics = self.load_json_file('lead-time-metrics.json')
        cycle_times = []
        
        if not lead_time_metrics:
            print("No lead-time metrics found")
            return {}
        
        for metric in lead_time_metrics:
            if isinstance(metric, dict) and 'lead_time_minutes' in metric:
                cycle_times.append({
                    'issue_number': metric.get('issue_number'),
                    'cycle_time_minutes': metric.get('lead_time_minutes'),
                    'issue_created_at': metric.get('issue_created_at'),
                    'deployed_at': metric.get('deployed_at'),
                    'stages': metric.get('stages', {})
                })
        
        if not cycle_times:
            print("No cycle time data available")
            return {}
        
        # 통계 계산
        times = [ct['cycle_time_minutes'] for ct in cycle_times if ct['cycle_time_minutes']]
        
        if not times:
            return {}
        
        stats = {
            'total_cycles': len(times),
            'total_time_hours': round(sum(times) / 60, 2),
            'avg_cycle_time_minutes': round(statistics.mean(times), 2),
            'median_cycle_time_minutes': round(statistics.median(times), 2),
            'min_cycle_time_minutes': min(times),
            'max_cycle_time_minutes': max(times),
            'stddev_cycle_time_minutes': round(statistics.stdev(times), 2) if len(times) > 1 else 0,
            'p50_percentile': round(statistics.median(times), 2),
            'p95_percentile': round(sorted(times)[int(len(times) * 0.95) - 1], 2) if len(times) > 1 else times[0],
            'p99_percentile': round(sorted(times)[int(len(times) * 0.99) - 1], 2) if len(times) > 1 else times[0],
        }
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'cycle_times': cycle_times,
            'statistics': stats
        }
    
    def analyze_stages(self) -> Dict:
        """
        각 단계별 시간 분석
        Issue → PR, PR → Review, Review → Merge, Merge → Deploy
        """
        print("\n📈 Analyzing stage times...")
        
        lead_time_metrics = self.load_json_file('lead-time-metrics.json')
        if not lead_time_metrics:
            return {}
        
        stage_data = {
            'issue_to_pr_times': [],
            'review_merge_times': [],
            'merge_to_deploy_times': []
        }
        
        for metric in lead_time_metrics:
            if not isinstance(metric, dict):
                continue
            
            stages = metric.get('stages', {})
            
            if 'issue_to_pr_minutes' in stages and stages['issue_to_pr_minutes']:
                stage_data['issue_to_pr_times'].append(stages['issue_to_pr_minutes'])
            
            if 'review_merge_minutes' in stages and stages['review_merge_minutes']:
                stage_data['review_merge_times'].append(stages['review_merge_minutes'])
            
            if 'merge_to_deploy_minutes' in stages and stages['merge_to_deploy_minutes']:
                stage_data['merge_to_deploy_times'].append(stages['merge_to_deploy_minutes'])
        
        # 각 단계별 통계
        stage_stats = {}
        
        for stage_name, times in stage_data.items():
            if not times:
                continue
            
            stage_stats[stage_name] = {
                'count': len(times),
                'avg_minutes': round(statistics.mean(times), 2),
                'median_minutes': round(statistics.median(times), 2),
                'min_minutes': min(times),
                'max_minutes': max(times),
                'total_percentage': round((sum(times) / sum(
                    sum(v) for v in stage_data.values() if v
                )) * 100, 2) if any(stage_data.values()) else 0
            }
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'stage_statistics': stage_stats
        }
    
    def analyze_trends(self) -> Dict:
        """
        Cycle Time 추세 분석
        일, 주, 월 단위 변화 추적
        """
        print("\n📉 Analyzing trends...")
        
        lead_time_metrics = self.load_json_file('lead-time-metrics.json')
        if not lead_time_metrics:
            return {}
        
        # 날짜별로 그룹화
        by_date = {}
        
        for metric in lead_time_metrics:
            if not isinstance(metric, dict):
                continue
            
            deployed_at = metric.get('deployed_at')
            if not deployed_at:
                continue
            
            dt = self.parse_datetime(deployed_at)
            if not dt:
                continue
            
            date_key = dt.strftime('%Y-%m-%d')
            cycle_time = metric.get('lead_time_minutes')
            
            if date_key not in by_date:
                by_date[date_key] = []
            
            if cycle_time:
                by_date[date_key].append(cycle_time)
        
        # 날짜별 평균 계산
        daily_avg = {}
        for date_key in sorted(by_date.keys()):
            times = by_date[date_key]
            daily_avg[date_key] = {
                'count': len(times),
                'avg_cycle_time_minutes': round(statistics.mean(times), 2),
                'min': min(times),
                'max': max(times)
            }
        
        # 주간 평균
        by_week = {}
        for date_key, avg_data in daily_avg.items():
            dt = datetime.strptime(date_key, '%Y-%m-%d')
            week_key = dt.strftime('%Y-W%U')
            
            if week_key not in by_week:
                by_week[week_key] = []
            
            by_week[week_key].append(avg_data['avg_cycle_time_minutes'])
        
        weekly_avg = {}
        for week_key in sorted(by_week.keys()):
            times = by_week[week_key]
            weekly_avg[week_key] = {
                'avg_cycle_time_minutes': round(statistics.mean(times), 2),
                'min': min(times),
                'max': max(times),
                'days': len(times)
            }
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'daily_average': daily_avg,
            'weekly_average': weekly_avg,
            'trend': 'improving' if len(weekly_avg) > 1 and 
                    list(weekly_avg.values())[-1]['avg_cycle_time_minutes'] < 
                    list(weekly_avg.values())[0]['avg_cycle_time_minutes'] 
                    else 'stable'
        }
    
    def compare_with_goals(self, goal_minutes: int = 1440) -> Dict:
        """
        목표와 비교 (기본값: 24시간)
        """
        print("\n🎯 Comparing with goals...")
        
        lead_time_metrics = self.load_json_file('lead-time-metrics.json')
        if not lead_time_metrics:
            return {}
        
        cycle_times = [m.get('lead_time_minutes') for m in lead_time_metrics 
                       if isinstance(m, dict) and m.get('lead_time_minutes')]
        
        if not cycle_times:
            return {}
        
        within_goal = sum(1 for t in cycle_times if t <= goal_minutes)
        goal_compliance = (within_goal / len(cycle_times)) * 100 if cycle_times else 0
        
        return {
            'goal_minutes': goal_minutes,
            'goal_hours': goal_minutes / 60,
            'compliance_rate_percent': round(goal_compliance, 2),
            'within_goal': within_goal,
            'exceeding_goal': len(cycle_times) - within_goal,
            'avg_variance_minutes': round(
                statistics.mean([abs(t - goal_minutes) for t in cycle_times]), 2
            )
        }
    
    def generate_report(self, cycle_data: Dict, stage_data: Dict, 
                       trend_data: Dict, goal_data: Dict) -> str:
        """HTML/Markdown 리포트 생성"""
        print("\n📋 Generating report...")
        
        report = "# Cycle Time Analysis Report\n\n"
        report += f"**Generated**: {datetime.utcnow().isoformat()}\n\n"
        
        # 핵심 메트릭
        if cycle_data.get('statistics'):
            stats = cycle_data['statistics']
            report += "## 📊 Key Metrics\n\n"
            report += "| Metric | Value |\n"
            report += "|--------|-------|\n"
            report += f"| Average Cycle Time | {stats.get('avg_cycle_time_minutes', 0)} min |\n"
            report += f"| Median Cycle Time | {stats.get('median_cycle_time_minutes', 0)} min |\n"
            report += f"| Min Cycle Time | {stats.get('min_cycle_time_minutes', 0)} min |\n"
            report += f"| Max Cycle Time | {stats.get('max_cycle_time_minutes', 0)} min |\n"
            report += f"| Std Dev | {stats.get('stddev_cycle_time_minutes', 0)} min |\n"
            report += f"| P95 | {stats.get('p95_percentile', 0)} min |\n"
            report += f"| P99 | {stats.get('p99_percentile', 0)} min |\n"
            report += f"| Total Cycles | {stats.get('total_cycles', 0)} |\n\n"
        
        # 단계별 분석
        if stage_data.get('stage_statistics'):
            stages = stage_data['stage_statistics']
            report += "## 📈 Stage Breakdown\n\n"
            
            for stage_name, stage_stats in stages.items():
                clean_name = stage_name.replace('_', ' ').title()
                report += f"### {clean_name}\n"
                report += f"- Count: {stage_stats.get('count', 0)}\n"
                report += f"- Average: {stage_stats.get('avg_minutes', 0)} min\n"
                report += f"- Median: {stage_stats.get('median_minutes', 0)} min\n"
                report += f"- Range: {stage_stats.get('min_minutes', 0)}-{stage_stats.get('max_minutes', 0)} min\n"
                report += f"- % of Total: {stage_stats.get('total_percentage', 0)}%\n\n"
        
        # 목표 준수
        if goal_data:
            report += "## 🎯 Goal Compliance\n\n"
            report += f"- Target: {goal_data.get('goal_hours', 24)} hours\n"
            report += f"- Compliance Rate: {goal_data.get('compliance_rate_percent', 0)}%\n"
            report += f"- Within Goal: {goal_data.get('within_goal', 0)}\n"
            report += f"- Exceeding Goal: {goal_data.get('exceeding_goal', 0)}\n"
            report += f"- Avg Variance: {goal_data.get('avg_variance_minutes', 0)} min\n\n"
        
        # 추세
        if trend_data.get('weekly_average'):
            report += "## 📉 Trend\n\n"
            report += f"- Direction: {trend_data.get('trend', 'stable').upper()}\n"
            weekly = trend_data.get('weekly_average', {})
            if weekly:
                first_week = list(weekly.values())[0]['avg_cycle_time_minutes']
                last_week = list(weekly.values())[-1]['avg_cycle_time_minutes']
                change = last_week - first_week
                report += f"- First Week Avg: {first_week} min\n"
                report += f"- Last Week Avg: {last_week} min\n"
                report += f"- Change: {change:+.2f} min\n\n"
        
        report += "---\n"
        report += "*DORA Metrics: Cycle Time*\n"
        report += "*Cycle Time is the amount of time it takes for code to go from idea to production.*\n"
        
        return report
    
    def run_analysis(self) -> None:
        """전체 분석 실행"""
        print("\n🚀 Starting Cycle Time Analysis...\n")
        
        # 데이터 수집
        cycle_data = self.calculate_cycle_time()
        stage_data = self.analyze_stages()
        trend_data = self.analyze_trends()
        goal_data = self.compare_with_goals(goal_minutes=1440)
        
        # 결과 저장
        if cycle_data:
            self.save_json_file('cycle-time-metrics.json', cycle_data)
        
        if stage_data:
            self.save_json_file('stage-analysis.json', stage_data)
        
        if trend_data:
            self.save_json_file('cycle-time-trends.json', trend_data)
        
        if goal_data:
            self.save_json_file('cycle-time-goals.json', goal_data)
        
        # 리포트 생성
        if any([cycle_data, stage_data, trend_data, goal_data]):
            report = self.generate_report(cycle_data, stage_data, trend_data, goal_data)
            report_file = self.metrics_dir / 'cycle-time-report.md'
            
            try:
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✓ Report saved: {report_file}")
            except IOError as e:
                print(f"Error saving report: {e}")
        
        print("\n✅ Cycle Time Analysis Complete!\n")
        
        # 요약 출력
        if cycle_data.get('statistics'):
            stats = cycle_data['statistics']
            print(f"📊 Summary:")
            print(f"   Average Cycle Time: {stats.get('avg_cycle_time_minutes', 0)} minutes")
            print(f"   Total Cycles: {stats.get('total_cycles', 0)}")
            print(f"   Range: {stats.get('min_cycle_time_minutes', 0)}-{stats.get('max_cycle_time_minutes', 0)} min")


def generate_sample_data(metrics_dir: str = '.github/metrics') -> None:
    """테스트용 샘플 데이터 생성"""
    print("\n📝 Generating sample data for testing...\n")
    
    from datetime import datetime, timedelta
    import random
    
    metrics_path = Path(metrics_dir)
    metrics_path.mkdir(parents=True, exist_ok=True)
    
    # 샘플 lead-time 메트릭 생성
    sample_metrics = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i in range(1, 21):
        issue_date = base_date + timedelta(days=i-1)
        pr_date = issue_date + timedelta(hours=random.randint(2, 8))
        merge_date = pr_date + timedelta(hours=random.randint(2, 12))
        deploy_date = merge_date + timedelta(hours=random.randint(1, 6))
        
        issue_to_pr = int((pr_date - issue_date).total_seconds() / 60)
        pr_to_merge = int((merge_date - pr_date).total_seconds() / 60)
        merge_to_deploy = int((deploy_date - merge_date).total_seconds() / 60)
        lead_time = issue_to_pr + pr_to_merge + merge_to_deploy
        
        sample_metrics.append({
            'issue_number': 100 + i,
            'issue_created_at': issue_date.isoformat() + 'Z',
            'pr_created_at': pr_date.isoformat() + 'Z',
            'pr_merged_at': merge_date.isoformat() + 'Z',
            'deployed_at': deploy_date.isoformat() + 'Z',
            'lead_time_minutes': lead_time,
            'stages': {
                'issue_to_pr_minutes': issue_to_pr,
                'pr_to_merge_minutes': pr_to_merge,
                'review_merge_minutes': pr_to_merge,
                'merge_to_deploy_minutes': merge_to_deploy
            }
        })
    
    # 데이터 저장
    sample_file = metrics_path / 'lead-time-metrics.json'
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_metrics, f, indent=2)
    
    print(f"✓ Sample data created: {sample_file}")
    print(f"  - Generated {len(sample_metrics)} sample issues")
    print(f"  - Date range: {base_date.date()} to {base_date.date() + timedelta(days=20)}\n")


def main():
    """메인 함수"""
    import sys
    
    metrics_dir = '.github/metrics'
    generate_sample = False
    
    # 명령어 옵션 파싱
    if len(sys.argv) > 1:
        if sys.argv[1] == '--generate-sample' or sys.argv[1] == '-s':
            generate_sample = True
        else:
            metrics_dir = sys.argv[1]
    
    # 메트릭 디렉토리 확인
    metrics_path = Path(metrics_dir)
    lead_time_file = metrics_path / 'lead-time-metrics.json'
    
    # lead-time-metrics.json 파일이 없으면 자동으로 샘플 생성
    if not lead_time_file.exists() or generate_sample:
        generate_sample_data(metrics_dir)
    
    calculator = CycleTimeCalculator(metrics_dir)
    calculator.run_analysis()


if __name__ == '__main__':
    main()
