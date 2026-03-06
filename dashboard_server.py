#!/usr/bin/env python3
"""
DORA Metrics Dashboard API Server
GraphQL/REST API를 사용하여 메트릭 데이터를 수집하고 제공합니다.
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime, timedelta
import statistics
import os

app = Flask(__name__)
CORS(app)

METRICS_DIR = Path('.github/metrics')


def load_json_file(filename: str) -> dict:
    """JSON 파일 로드"""
    filepath = METRICS_DIR / filename
    if not filepath.exists():
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def get_cycle_time_data() -> dict:
    """Cycle Time 데이터"""
    data = load_json_file('cycle-time-metrics.json')
    if not data:
        return {
            'avg': 0,
            'change': 0,
            'trend': []
        }
    
    stats = data.get('statistics', {})
    trend_file = load_json_file('cycle-time-trends.json')
    trend_data = trend_file.get('weekly_average', {})
    
    # 추세 데이터 생성
    trend = []
    for week, values in sorted(trend_data.items()):
        trend.append({
            'date': week,
            'value': values.get('avg_cycle_time_minutes', 0) / 60  # 시간으로 변환
        })
    
    change = 0
    if len(trend) > 1:
        change = trend[-1]['value'] - trend[-2]['value']
    
    return {
        'avg': stats.get('avg_cycle_time_minutes', 0) / 60,  # 시간으로 변환
        'median': stats.get('median_cycle_time_minutes', 0) / 60,
        'change': change,
        'dates': [t['date'] for t in trend],
        'values': [t['value'] for t in trend],
        'average': sum([t['value'] for t in trend]) / len(trend) if trend else 0
    }


def get_deployment_frequency_data() -> dict:
    """Deployment Frequency 데이터"""
    data = load_json_file('deployment-frequency.json')
    if not data:
        return {
            'frequency': 0,
            'change': 0,
            'by_day': []
        }
    
    metrics = data.get('metrics', {})
    frequency = metrics.get('avg_deployments_per_day', 0) * 7  # 주당 배포 횟수
    
    # 일별 데이터 (샘플)
    by_day = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        by_day.append({
            'date': date,
            'count': int(frequency / 7) + (1 if i % 2 == 0 else 0)
        })
    
    return {
        'frequency': frequency,
        'change': 0,
        'by_day': by_day,
        'success_rate': metrics.get('success_rate', 100)
    }


def get_mttr_data() -> dict:
    """MTTR 데이터"""
    data = load_json_file('mttr-analysis.json')
    if not data:
        return {
            'avg': 0,
            'change': 0,
            'history': []
        }
    
    metrics = data.get('metrics', {})
    avg_mttr = metrics.get('avg_recovery_minutes', 0)
    
    # 히스토리 데이터 (샘플)
    history = []
    for i in range(10):
        date = (datetime.now() - timedelta(days=10-i)).strftime('%Y-%m-%d')
        history.append({
            'date': date,
            'mttr': avg_mttr + (i % 3 * 10 - 10)
        })
    
    return {
        'avg': avg_mttr,
        'min': metrics.get('min_recovery_minutes', 0),
        'max': metrics.get('max_recovery_minutes', 0),
        'change': 0,
        'history': history
    }


def get_cfr_data() -> dict:
    """Change Failure Rate 데이터"""
    data = load_json_file('change-failure-rate.json')
    if not data:
        return {
            'rate': 0,
            'change': 0
        }
    
    metrics = data.get('metrics', {})
    return {
        'rate': float(metrics.get('failure_rate_percent', 0)),
        'change': 0,
        'rollback_rate': float(metrics.get('rollback_rate_percent', 0))
    }


def get_stage_breakdown() -> dict:
    """단계별 구성 데이터"""
    data = load_json_file('stage-analysis.json')
    if not data:
        return {}
    
    stage_stats = data.get('stage_statistics', {})
    result = {}
    
    for stage_name, stats in stage_stats.items():
        result[stage_name] = stats.get('total_percentage', 0)
    
    return result


def get_health_status() -> dict:
    """시스템 건강 상태"""
    cycle_time = get_cycle_time_data()
    deployment = get_deployment_frequency_data()
    mttr = get_mttr_data()
    cfr = get_cfr_data()
    
    # 상태 판정
    def get_status(value, thresholds):
        if value <= thresholds['healthy']:
            return 'healthy'
        elif value <= thresholds['warning']:
            return 'warning'
        else:
            return 'critical'
    
    return {
        'lead_time_status': get_status(cycle_time['avg'] * 60, 
                                      {'healthy': 1440, 'warning': 2880}),
        'lead_time_message': f"{cycle_time['avg']:.1f} 시간 (목표: 24시간)",
        
        'deployment_status': get_status(deployment['frequency'], 
                                       {'healthy': 10, 'warning': 5}),
        'deployment_message': f"주당 {deployment['frequency']:.1f}회 배포",
        
        'mttr_status': get_status(mttr['avg'], 
                                {'healthy': 60, 'warning': 240}),
        'mttr_message': f"{mttr['avg']:.0f}분 (목표: 1시간)",
        
        'cfr_status': get_status(cfr['rate'], 
                               {'healthy': 15, 'warning': 30}),
        'cfr_message': f"{cfr['rate']:.1f}% (목표: < 15%)"
    }


def get_time_series_data() -> dict:
    """시계열 데이터"""
    cycle_time = get_cycle_time_data()
    deployment = get_deployment_frequency_data()
    cfr = get_cfr_data()
    
    # 날짜 통일
    dates = cycle_time.get('dates', [])
    if not dates:
        dates = [(datetime.now() - timedelta(days=6-i)).strftime('%Y-W%U') 
                 for i in range(7)]
    
    return {
        'dates': dates,
        'lead_time': [v * 60 for v in cycle_time.get('values', [])],  # 분으로 변환
        'deploy_freq': [deployment['frequency'] / 7] * len(dates),  # 일별로 평준화
        'cfr': [cfr['rate']] * len(dates)
    }


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """메인 메트릭 API"""
    return jsonify({
        'cycle_time': get_cycle_time_data(),
        'deployment': get_deployment_frequency_data(),
        'mttr': get_mttr_data(),
        'cfr': get_cfr_data(),
        'cycle_time_trend': {
            'dates': get_cycle_time_data().get('dates', []),
            'values': get_cycle_time_data().get('values', []),
            'average': get_cycle_time_data().get('average', 0)
        },
        'deployment_by_day': get_deployment_frequency_data().get('by_day', []),
        'stage_breakdown': get_stage_breakdown(),
        'mttr_history': get_mttr_data().get('history', []),
        'health': get_health_status(),
        'time_series': get_time_series_data(),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/cycle-time', methods=['GET'])
def get_cycle_time_endpoint():
    """Cycle Time 상세 API"""
    return jsonify(get_cycle_time_data())


@app.route('/api/deployment-frequency', methods=['GET'])
def get_deployment_frequency_endpoint():
    """Deployment Frequency 상세 API"""
    return jsonify(get_deployment_frequency_data())


@app.route('/api/mttr', methods=['GET'])
def get_mttr_endpoint():
    """MTTR 상세 API"""
    return jsonify(get_mttr_data())


@app.route('/api/cfr', methods=['GET'])
def get_cfr_endpoint():
    """CFR 상세 API"""
    return jsonify(get_cfr_data())


@app.route('/api/health', methods=['GET'])
def get_health_endpoint():
    """시스템 상태 API"""
    return jsonify(get_health_status())


@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/', methods=['GET'])
def dashboard():
    """대시보드 페이지 제공"""
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            html = f.read()
        return html
    except FileNotFoundError:
        return '<h1>Dashboard not found</h1>', 404


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     📊 DORA Metrics Dashboard Server                       ║
    ║                                                            ║
    ║     Start at http://localhost:5000                        ║
    ║     API: http://localhost:5000/api/metrics                ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
