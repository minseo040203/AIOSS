#!/usr/bin/env python3
"""
GitHub 스프린트 메트릭 시각화 대시보드
Burndown Chart, Velocity Chart, Cycle Time 분석을 생성합니다.
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import rcParams
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib 미설치. 설치하려면: pip install matplotlib")


class MetricsDashboard:
    def __init__(self, report_file: str = "reports/sprint_metrics.json"):
        self.report_file = report_file
        self.report_data = None
        self.output_dir = "reports/visualizations"
        
        # 한글 폰트 설정
        if MATPLOTLIB_AVAILABLE:
            rcParams['font.family'] = 'sans-serif'
            rcParams['axes.unicode_minus'] = False
    
    def load_report(self) -> bool:
        """리포트 파일 로드"""
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                self.report_data = json.load(f)
            print(f"✓ {self.report_file} 로드 완료")
            return True
        except FileNotFoundError:
            print(f"⚠️  {self.report_file} 파일을 찾을 수 없습니다")
            return False
        except json.JSONDecodeError:
            print(f"⚠️  JSON 파싱 오류")
            return False
    
    def create_output_dir(self):
        """출력 디렉토리 생성"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    # ============================================================================
    # Burndown Chart
    # ============================================================================
    def plot_burndown_chart(self):
        """Burndown Chart 생성"""
        if not MATPLOTLIB_AVAILABLE or not self.report_data:
            return
        
        print("\n📉 Burndown Chart 생성 중...")
        
        burndown_data = self.report_data.get('metrics', {}).get('burndown', [])
        
        if not burndown_data:
            print("  ⚠️  Burndown 데이터 없음")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for milestone in burndown_data:
            if milestone['total_issues'] > 0:
                remaining = milestone['remaining_issues']
                total = milestone['total_issues']
                
                # 선형 이상적 Burndown 라인
                ideal_days = [0, total]
                actual_days = [milestone['closed_issues'], remaining]
                
                ax.plot([0, 1], ideal_days, 'r--', label='Ideal Burndown', linewidth=2)
                ax.plot([0, 1], actual_days, 'b-o', label='Actual Progress', linewidth=2, markersize=8)
        
        ax.set_xlabel('Sprint Progress', fontsize=12)
        ax.set_ylabel('Remaining Issues', fontsize=12)
        ax.set_title('Sprint Burndown Chart', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = f"{self.output_dir}/burndown_chart.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ {output_file} 저장")
        plt.close()
    
    # ============================================================================
    # Velocity Chart
    # ============================================================================
    def plot_velocity_chart(self):
        """Velocity Chart 생성"""
        if not MATPLOTLIB_AVAILABLE or not self.report_data:
            return
        
        print("🚀 Velocity Chart 생성 중...")
        
        velocity_data = self.report_data.get('metrics', {}).get('velocity', {})
        by_milestone = velocity_data.get('by_milestone', {})
        
        if not by_milestone:
            print("  ⚠️  Velocity 데이터 없음")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 마일스톤별 완료율
        milestones = list(by_milestone.keys())
        closed = [by_milestone[m]['closed'] for m in milestones]
        total = [by_milestone[m]['total'] for m in milestones]
        
        x = range(len(milestones))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], closed, width, label='Closed', color='#2ecc71')
        ax1.bar([i + width/2 for i in x], total, width, label='Total', color='#3498db')
        
        ax1.set_xlabel('Milestone', fontsize=11)
        ax1.set_ylabel('Issue Count', fontsize=11)
        ax1.set_title('Milestone Progress', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(milestones, rotation=15, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # PR 메트릭
        pr_metrics = velocity_data.get('pr_metrics', {})
        pr_labels = ['Total', 'Merged', 'Closed']
        pr_values = [
            pr_metrics.get('total_prs', 0),
            pr_metrics.get('merged_prs', 0),
            pr_metrics.get('closed_prs', 0)
        ]
        
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        ax2.bar(pr_labels, pr_values, color=colors)
        ax2.set_ylabel('Pull Request Count', fontsize=11)
        ax2.set_title('Pull Request Metrics', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = f"{self.output_dir}/velocity_chart.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ {output_file} 저장")
        plt.close()
    
    # ============================================================================
    # Cycle Time Distribution
    # ============================================================================
    def plot_cycle_time_stats(self):
        """Cycle Time 통계 시각화"""
        if not MATPLOTLIB_AVAILABLE or not self.report_data:
            return
        
        print("⏱️  Cycle Time 통계 생성 중...")
        
        cycle_time = self.report_data.get('metrics', {}).get('cycle_time', {})
        
        if cycle_time['count'] == 0:
            print("  ⚠️  Cycle Time 데이터 없음")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        metrics = ['Average', 'Median', 'Min', 'Max']
        values = [
            cycle_time.get('average', 0),
            cycle_time.get('median', 0),
            cycle_time.get('min', 0),
            cycle_time.get('max', 0)
        ]
        
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
        bars = ax.bar(metrics, values, color=colors)
        
        # 값을 바에 표시
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}h',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Time (hours)', fontsize=11)
        ax.set_title('Cycle Time Statistics', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # 통계 추가
        stats_text = f"Count: {cycle_time['count']}\nStd Dev: {cycle_time.get('std_dev', 0):.1f}h"
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        output_file = f"{self.output_dir}/cycle_time_stats.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ {output_file} 저장")
        plt.close()
    
    # ============================================================================
    # Throughput Chart
    # ============================================================================
    def plot_throughput_chart(self):
        """Throughput Chart 생성"""
        if not MATPLOTLIB_AVAILABLE or not self.report_data:
            return
        
        print("📊 Throughput Chart 생성 중...")
        
        throughput = self.report_data.get('metrics', {}).get('throughput', {})
        
        if not throughput.get('weekly'):
            print("  ⚠️  Throughput 데이터 없음")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 주단위 Throughput
        weekly = throughput.get('weekly', {})
        if weekly:
            weeks = list(weekly.keys())
            values = list(weekly.values())
            ax1.bar(range(len(weeks)), values, color='#3498db')
            ax1.set_xlabel('Week', fontsize=11)
            ax1.set_ylabel('Closed Issues', fontsize=11)
            ax1.set_title('Weekly Throughput', fontsize=12, fontweight='bold')
            ax1.set_xticks(range(len(weeks)))
            ax1.set_xticklabels(weeks, rotation=45, ha='right')
            ax1.grid(True, alpha=0.3, axis='y')
        
        # 월별 Throughput
        monthly = throughput.get('monthly', {})
        if monthly:
            months = list(monthly.keys())
            values = list(monthly.values())
            ax2.bar(range(len(months)), values, color='#2ecc71')
            ax2.set_xlabel('Month', fontsize=11)
            ax2.set_ylabel('Closed Issues', fontsize=11)
            ax2.set_title('Monthly Throughput', fontsize=12, fontweight='bold')
            ax2.set_xticks(range(len(months)))
            ax2.set_xticklabels(months, rotation=45, ha='right')
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = f"{self.output_dir}/throughput_chart.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ {output_file} 저장")
        plt.close()
    
    # ============================================================================
    # Summary Dashboard (HTML)
    # ============================================================================
    def generate_html_dashboard(self):
        """HTML 대시보드 생성"""
        print("\n🌐 HTML 대시보드 생성 중...")
        
        summary = self.report_data.get('summary', {})
        metrics = self.report_data.get('metrics', {})
        
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sprint Metrics Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .metric-label {{
            font-size: 0.95em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .charts-section {{
            margin-top: 40px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .chart-container {{
            background: #f9f9f9;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        
        .chart-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        
        footer {{
            background: #f9f9f9;
            padding: 20px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #eee;
        }}
        
        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .stats-table th,
        .stats-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .stats-table th {{
            background: #667eea;
            color: white;
        }}
        
        .stats-table tr:hover {{
            background: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Sprint Metrics Dashboard</h1>
            <div class="subtitle">AIOSS Development Sprint Analysis</div>
            <div class="subtitle" style="font-size: 0.9em; margin-top: 10px;">
                Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </header>
        
        <div class="content">
            <h2 style="margin-bottom: 20px; color: #333;">📈 Key Metrics</h2>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Issues</div>
                    <div class="metric-value">{summary.get('total_issues', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Closed Issues</div>
                    <div class="metric-value" style="color: #2ecc71;">{summary.get('closed_issues', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Open Issues</div>
                    <div class="metric-value" style="color: #e74c3c;">{summary.get('open_issues', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Pull Requests</div>
                    <div class="metric-value">{summary.get('total_prs', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Merged PRs</div>
                    <div class="metric-value" style="color: #2ecc71;">{summary.get('merged_prs', 0)}</div>
                </div>
            </div>
            
            <h2 style="margin: 40px 0 20px; color: #333;">⏱️ Cycle Time Analysis</h2>
            
            <table class="stats-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Average Cycle Time</td>
                    <td>{metrics.get('cycle_time', {}).get('average', 0):.1f} hours</td>
                </tr>
                <tr>
                    <td>Median Cycle Time</td>
                    <td>{metrics.get('cycle_time', {}).get('median', 0):.1f} hours</td>
                </tr>
                <tr>
                    <td>Min/Max Cycle Time</td>
                    <td>{metrics.get('cycle_time', {}).get('min', 0):.1f}h / {metrics.get('cycle_time', {}).get('max', 0):.1f}h</td>
                </tr>
                <tr>
                    <td>Lead Time (PR)</td>
                    <td>{metrics.get('lead_time', {}).get('average', 0):.1f} hours</td>
                </tr>
            </table>
            
            <h2 style="margin: 40px 0 20px; color: #333;">📊 Visualizations</h2>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <div class="chart-title">Burndown Chart</div>
                    <img src="burndown_chart.png" alt="Burndown Chart">
                </div>
                <div class="chart-container">
                    <div class="chart-title">Velocity Chart</div>
                    <img src="velocity_chart.png" alt="Velocity Chart">
                </div>
                <div class="chart-container">
                    <div class="chart-title">Cycle Time Statistics</div>
                    <img src="cycle_time_stats.png" alt="Cycle Time Stats">
                </div>
                <div class="chart-container">
                    <div class="chart-title">Throughput Chart</div>
                    <img src="throughput_chart.png" alt="Throughput Chart">
                </div>
            </div>
        </div>
        
        <footer>
            <p>Generated by GitHub Sprint Metrics Analyzer</p>
            <p>Repository: <strong>minseo040203/AIOSS</strong></p>
        </footer>
    </div>
</body>
</html>
"""
        
        output_file = f"{self.output_dir}/dashboard.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✓ {output_file} 저장")
    
    def generate_all(self):
        """모든 대시보드 생성"""
        if not self.load_report():
            return False
        
        self.create_output_dir()
        
        if MATPLOTLIB_AVAILABLE:
            self.plot_burndown_chart()
            self.plot_velocity_chart()
            self.plot_cycle_time_stats()
            self.plot_throughput_chart()
        else:
            print("⚠️  matplotlib가 설치되어 있지 않아 차트를 생성할 수 없습니다")
            print("     설치: pip install matplotlib")
        
        self.generate_html_dashboard()
        
        print("\n✅ 대시보드 생성 완료!")
        print(f"📁 출력 위치: {self.output_dir}/")
        print(f"🌐 Dashboard: {self.output_dir}/dashboard.html")


def main():
    print("🚀 메트릭 시각화 대시보드 생성 시작\n")
    
    dashboard = MetricsDashboard()
    dashboard.generate_all()


if __name__ == "__main__":
    main()
