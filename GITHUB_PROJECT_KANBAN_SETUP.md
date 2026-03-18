# 📊 GitHub 칸반 프로젝트 스프린트 설정 완료

> **칸반 기반 GitHub Project 설정 및 DORA 메트릭 분석 시스템 구축**

---

## ✨ 완료된 작업

### ✅ Phase 1: 기본 설정 (완료)

#### 1. 이슈 템플릿 시스템
- ✓ Bug Report 템플릿 (`.github/issue_template/bug_report.md`)
- ✓ Feature Request 템플릿 (`.github/issue_template/feature_request.md`)
- ✓ Template Config 설정 (`.github/issue_template/config.yml`)

#### 2. 라벨 체계 (20+ 레이블)
```
우선순위: priority/critical, high, medium, low
타입: type/bug, feature, enhancement, documentation, refactor, test
상태: status/backlog, ready, in-progress, review, blocked
영역: area/ai-core, rag-system, ui-ux, infrastructure, documentation
스프린트: sprint/essential, nice-to-have
기타: good-first-issue, help-wanted, wontfix
```

#### 3. 마일스톤
- Sprint 1: AI Core 구축 (2026-04-15)
- Sprint 2: UI 및 통합 (2026-05-15)

#### 4. 이슈 (최소 10개 이상)
- Sprint 1: 5개 필수 이슈
- Sprint 2: 5개 필수 이슈
- 추가: 2개 선택 이슈

**총 12개 이슈** - 팀 역량에 따라 추가 가능

---

### ✅ Phase 2: 자동화 스크립트 (완료)

#### `scripts/setup_github_project.py`
GitHub CLI를 사용한 자동 설정 스크립트
```bash
python scripts/setup_github_project.py
```

#### `scripts/setup_github_project_api.py`
PyGithub를 사용한 GitHub API 기반 설정 스크립트
```bash
GITHUB_TOKEN=ghp_xxx python scripts/setup_github_project_api.py
```

**생성 내용:**
- 라벨 생성/업데이트
- 마일스톤 생성
- 이슈 생성 및 라벨/마일스톤 연결

---

### ✅ Phase 3: 메트릭 수집 시스템 (완료)

#### `scripts/collect_metrics.py`
GitHub 데이터를 수집하여 DORA 메트릭 계산
```bash
python scripts/collect_metrics.py
```

**수집 메트릭:**
- **Cycle Time**: 이슈 생성 → 완료까지 시간
- **Lead Time**: PR 생성 → Merge까지 시간
- **Velocity**: 마일스톤별 완료 이슈 수
- **Throughput**: 주/월별 완료 이슈 수
- **Burndown**: 마일스톤별 진행 상황

**출력:** `reports/sprint_metrics.json`

---

### ✅ Phase 4: 시각화 대시보드 (완료)

#### `scripts/visualize_metrics.py`
메트릭을 시각화한 대시보드 생성
```bash
python scripts/visualize_metrics.py
```

**생성 산출물:**
- `reports/visualizations/dashboard.html` - 📊 메인 대시보드
- `reports/visualizations/burndown_chart.png` - 📉 번다운 차트
- `reports/visualizations/velocity_chart.png` - 🚀 속도 차트
- `reports/visualizations/cycle_time_stats.png` - ⏱️ 사이클 타임
- `reports/visualizations/throughput_chart.png` - 📈 처리량 차트

---

### ✅ Phase 5: 설정 가이드 문서 (완료)

- `scripts/SPRINT_SETUP_GUIDE.md` - 상세 설정 가이드
- `SPRINT_SETUP_EXECUTION_GUIDE.md` - 실행 단계별 가이드
- `GITHUB_PROJECT_KANBAN_SETUP.md` - 칸반 설정 가이드 (이 문서)

---

## 🚀 빠른 시작 (Quick Start)

### 1단계: GitHub Token 설정
```powershell
$env:GITHUB_TOKEN='ghp_your_token_here'
```

### 2단계: 자동 설정 실행
```bash
cd c:\AIOSS
python scripts/setup_github_project_api.py
```

### 3단계: GitHub Project 칸반 보드 생성
수동으로 https://github.com/minseo040203/AIOSS/projects 에서 생성

### 4단계: 메트릭 수집
```bash
python scripts/collect_metrics.py
python scripts/visualize_metrics.py
```

### 5단계: 대시보드 확인
```bash
start reports/visualizations/dashboard.html
```

---

## 📁 프로젝트 구조

```
c:\AIOSS\
├── .github/
│   ├── issue_template/
│   │   ├── bug_report.md              ✓ 버그 보고 템플릿
│   │   ├── feature_request.md         ✓ 기능 요청 템플릿
│   │   └── config.yml                 ✓ 템플릿 설정
│   └── workflows/
│       └── dora-metrics-collection.yml (기존)
│
├── scripts/
│   ├── setup_github_project.py        ✓ GH CLI 기반 설정
│   ├── setup_github_project_api.py    ✓ GitHub API 기반 설정
│   ├── collect_metrics.py             ✓ 메트릭 수집
│   ├── visualize_metrics.py           ✓ 시각화 대시보드
│   ├── SPRINT_SETUP_GUIDE.md          ✓ 상세 가이드
│   └── GITHUB_PROJECT_KANBAN_SETUP.md ✓ 칸반 설정 가이드
│
├── reports/
│   ├── sprint_metrics.json            (생성 예정)
│   └── visualizations/
│       ├── dashboard.html             (생성 예정)
│       ├── burndown_chart.png         (생성 예정)
│       ├── velocity_chart.png         (생성 예정)
│       ├── cycle_time_stats.png       (생성 예정)
│       └── throughput_chart.png       (생성 예정)
│
└── SPRINT_SETUP_EXECUTION_GUIDE.md    ✓ 실행 가이드
```

---

## 📊 생성되는 이슈 목록

### Sprint 1: AI Core 구축

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|--------|
| 1 | Llama 모델 Raspberry Pi에 통합 | type/feature, area/ai-core, priority/critical | Sprint 1 |
| 2 | ChromaDB 벡터 데이터베이스 구성 | type/feature, area/rag-system, priority/high | Sprint 1 |
| 3 | 재난 안전 정보 데이터셋 구축 | type/feature, area/rag-system, priority/high | Sprint 1 |
| 4 | LangChain RAG 파이프라인 구현 | type/feature, area/rag-system, priority/critical | Sprint 1 |
| 5 | 오프라인 환경에서 모델 동작 테스트 | type/test, area/ai-core, priority/high | Sprint 1 |

### Sprint 2: UI 및 통합

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|--------|
| 6 | FastAPI 웹 서버 개발 | type/feature, area/ui-ux, priority/high | Sprint 2 |
| 7 | 웹 대시보드 UI 구현 | type/feature, area/ui-ux, priority/high | Sprint 2 |
| 8 | 다국어 지원 (한글, 영어) 추가 | type/enhancement, area/ui-ux, priority/medium | Sprint 2 |
| 9 | 응답 시간 최적화 및 벤치마크 | type/refactor, area/ai-core, priority/medium | Sprint 2 |
| 10 | 사용자 피드백 로깅 시스템 | type/feature, area/ui-ux, priority/low | Sprint 2 |
| 11 | 배포 자동화 스크립트 작성 | type/feature, area/infrastructure, priority/high | Sprint 2 |
| 12 | 통합 테스트 스위트 구축 | type/test, area/infrastructure, priority/high | Sprint 2 |
| 13 | 프로젝트 문서 및 튜토리얼 작성 | type/documentation, area/documentation, priority/medium | Sprint 2 |

---

## 🎨 칸반 보드 컬럼 설정

```
┌─────────────┬──────────────┬─────────────────┬────────┬───────┐
│ 📦 Backlog  │ 📋 To Do     │ 🔨 In Progress  │ 👀 Review │ ✅ Done │
├─────────────┼──────────────┼─────────────────┼────────┼───────┤
│ 향후 계획    │ 스프린트     │ 현재 작업 중    │ 검토   │ 완료  │
│ (자동 추가)  │ 계획된 이슈  │ (할당됨)        │ 대기   │(자동) │
└─────────────┴──────────────┴─────────────────┴────────┴───────┘
```

---

## 📈 메트릭 분석 가이드

### Cycle Time (사이클 타임)
- **계산**: 이슈 생성 → 완료까지 시간
- **목표**: 낮을수록 좋음 (개발 속도 향상)
- **개선**: 병목 제거, 작은 단위 분할

| 상황 | 진단 |
|------|------|
| Cycle Time 증가 | 병목 발생, 프로세스 개선 필요 |
| Cycle Time 감소 | 효율성 향상 |
| 높은 표준편차 | 이슈 크기 편차 큼 |

### Velocity (속도)
- **계산**: 스프린트당 완료 이슈 수
- **목표**: 일정한 수준 유지 (예측 가능)
- **개선**: 팀 생산성 향상

### Lead Time (리드 타임)
- **계산**: PR 생성 → Merge까지
- **목표**: 짧을수록 좋음 (빠른 배포)
- **개선**: 코드 리뷰 효율화

### Throughput (처리량)
- **계산**: 기간별 완료 이슈 수
- **목표**: 지속적 증가
- **개선**: 팀 효율 최적화

### Burndown Chart (번다운)
- **목표**: 선형 감소
- **신호**: 급격한 변화 = 문제 발생

---

## 🔧 필요한 도구 및 설정

### 필수 요구사항
- Python 3.8+
- GitHub 계정 및 저장소
- GitHub Personal Access Token

### 필수 패키지
```bash
pip install PyGithub matplotlib
```

### 선택사항
- GitHub CLI (`gh` 명령어)
- Git
- VS Code

---

## 💡 모범 사례

### 이슈 작성 팁
1. **명확한 제목** - 한눈에 이해되도록
2. **수락 기준 명시** - Acceptance Criteria 포함
3. **라벨 분류** - 재검색 용이하도록
4. **마일스톤 지정** - 스프린트 계획 반영

### PR 작성 팁
1. **이슈 연결** - `Closes #123` 포함
2. **설명 상세** - 변경사항 설명
3. **테스트 코드** - 함께 제출
4. **팀 리뷰** - 최소 1명 이상

### 스프린트 계획
1. **월요일**: 백로그 우선순위 검토
2. **화-목**: 활발한 개발 진행
3. **금요일**: 리뷰 및 회고
4. **매주**: 메트릭 수집 및 분석

---

## 🎓 추가 학습 자료

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [DORA Metrics Guide](https://cloud.google.com/blog/products/devops-sre/using-four-keys-to-measure-devops-performance)
- [Kanban Best Practices](https://www.atlassian.com/agile/kanban)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🎯 다음 단계

1. ✅ GitHub Token 생성 및 설정
2. ✅ 설정 스크립트 실행 (라벨, 마일스톤, 이슈)
3. ⏳ GitHub Project 칸반 보드 생성 (수동)
4. ⏳ 첫 스프린트 계획 회의 진행
5. ⏳ 정기 메트릭 수집 및 분석

---

## 📞 문제 해결

### Q: GitHub Token이 뭐죠?
**A**: Personal Access Token으로 GitHub API 접근 권한입니다. https://github.com/settings/tokens/new 에서 생성하세요.

### Q: Project를 자동으로 생성할 수 없나요?
**A**: GitHub API v3에서는 아직 지원하지 않습니다. v4(GraphQL)를 사용하면 가능하지만 복잡하므로 수동 생성을 추천합니다.

### Q: 메트릭은 언제부터 수집되나요?
**A**: GitHub에 이슈와 PR 데이터가 있으면 즉시 수집됩니다. 처음에는 데이터가 적을 수 있습니다.

### Q: 라벨을 추가하려면?
**A**: GitHub 저장소 → Settings → Labels 에서 직접 추가하거나, `setup_github_project_api.py` 스크립트를 수정하고 재실행하세요.

---

## 🎉 축하합니다!

인적 자원의 **칸반 기반 GitHub Project**와 **DORA 메트릭 분석 시스템**이 완성되었습니다!

이제 효율적인 스프린트 기반 개발을 시작할 수 있습니다. 🚀

---

**작성일**: 2026-03-18  
**버전**: 1.0  
**상태**: ✅ 완료
