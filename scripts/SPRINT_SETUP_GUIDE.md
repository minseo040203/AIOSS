# 🚀 GitHub Project 스프린트 설정 및 메트릭 수집 가이드

## 📋 개요

이 가이드는 칸반 기반 GitHub Project를 생성하고, 스프린트 운영을 위한 백로그를 구성하며, DORA 메트릭을 수집하는 전체 과정을 설명합니다.

---

## 🎯 주요 기능

### ✅ 기본 설정
- ✓ 칸반 기반 GitHub Project 생성 (Backlog, To Do, In Progress, Review, Done)
- ✓ 10개 이상의 스프린트 이슈 생성
- ✓ 이슈 템플릿 (Bug/Feature) 설정
- ✓ 체계적인 라벨 시스템 구성
- ✓ 2개 마일스톤 생성

### 📊 메트릭 분석 (선택과제)
- ✓ **Cycle Time**: 이슈 생성부터 종료까지의 시간
- ✓ **Velocity**: 마일스톤별 완료된 이슈 수
- ✓ **Lead Time**: PR 생성부터 Merge까지의 시간
- ✓ **Throughput**: 주/월별 완료 이슈 수
- ✓ **Burndown Chart**: 스프린트 진행 상황 시각화

---

## 🔧 설치 및 준비

### 1. 필수 도구 설치

#### GitHub CLI 설치
```bash
# Windows (PowerShell)
# 또는 https://cli.github.com에서 직접 다운로드

# macOS
brew install gh

# Linux
sudo apt-get install gh
```

#### GitHub 인증
```bash
gh auth login
# 프롬프트 따라서:
# 1. GitHub.com 선택
# 2. HTTPS selected
# 3. 인증 방식 선택 (Personal Access Token 또는 OAuth)
```

#### Python 패키지 설치
```bash
cd c:\AIOSS
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
# 또는
source .venv/bin/activate           # macOS/Linux

pip install PyGithub matplotlib
```

---

## 📝 Step 1: 이슈 템플릿 및 라벨 설정

이미 다음 파일들이 생성되었습니다:

```
.github/
├── issue_template/
│   ├── bug_report.md          # 버그 리포트 템플릿
│   ├── feature_request.md     # 기능 요청 템플릿
│   └── config.yml             # 템플릿 설정
```

### 자동 설정에 포함된 라벨 체계

#### 우선순위 레이블
- `priority/critical` - 긴급 (즉시 작업)
- `priority/high` - 높음 (다음 스프린트)
- `priority/medium` - 중간
- `priority/low` - 낮음 (백로그)

#### 타입 레이블
- `type/bug` - 버그 수정
- `type/feature` - 새 기능
- `type/enhancement` - 기능 개선
- `type/documentation` - 문서
- `type/refactor` - 코드 리팩토링
- `type/test` - 테스트

#### 상태 레이블
- `status/backlog` - 백로그
- `status/ready` - 준비됨
- `status/in-progress` - 진행 중
- `status/review` - 리뷰 대기
- `status/blocked` - 블로킹됨

#### 영역 레이블
- `area/ai-core` - AI 코어
- `area/rag-system` - RAG 시스템
- `area/ui-ux` - UI/UX
- `area/infrastructure` - 인프라
- `area/documentation` - 문서

---

## 🚀 Step 2: 자동 설정 스크립트 실행

### 2.1 프로젝트, 라벨, 마일스톤, 이슈 생성

```bash
cd scripts
python setup_github_project.py
```

**생성되는 항목:**
- ✓ 20+ 라벨 생성/업데이트
- ✓ 2개 마일스톤 생성:
  - Sprint 1: AI Core 구축 (2026-04-15)
  - Sprint 2: UI 및 통합 (2026-05-15)
- ✓ 12개 이슈 생성:
  - Sprint 1: 5개 필수 이슈
  - Sprint 2: 5개 필수 이슈
  - 추가: 2개 선택 이슈

**생성된 이슈 목록:**

#### Sprint 1: AI Core 구축
1. Llama 모델 Raspberry Pi에 통합
2. ChromaDB 벡터 데이터베이스 구성
3. 재난 안전 정보 데이터셋 구축
4. LangChain RAG 파이프라인 구현
5. 오프라인 환경에서 모델 동작 테스트

#### Sprint 2: UI 및 통합
6. FastAPI 웹 서버 개발
7. 웹 대시보드 UI 구현
8. 다국어 지원 (한글, 영어) 추가
9. 응답 시간 최적화 및 벤치마크
10. 사용자 피드백 로깅 시스템
11. 배포 자동화 스크립트 작성
12. 통합 테스트 스위트 구축
13. 프로젝트 문서 및 튜토리얼 작성

---

## 📊 Step 3: GitHub Project 보드 설정 (수동)

> **주의**: GitHub CLI는 아직 Project 생성을 완벽히 지원하지 않으므로 수동 설정이 필요합니다.

### 3.1 칸반 보드 생성

1. GitHub 저장소로 이동: https://github.com/minseo040203/AIOSS
2. **Projects** 탭 클릭
3. **New project** 버튼 클릭
4. 프로젝트 설정:
   - **이름**: `AIOSS Development Sprint`
   - **설명**: `스프린트 기반 칸반 보드`
   - **템플릿**: `Kanban` 선택
   - **공개도**: `Public` 선택

### 3.2 컬럼 설정

기본 제공되는 컬럼을 다음과 같이 조정합니다:

1. **Backlog** - 백로그 (진행 예정)
2. **To Do** - 할 일 (스프린트에 포함됨)
3. **In Progress** - 진행 중 (현재 작업)
4. **Review** - 리뷰 (검토 대기)
5. **Done** - 완료 (종료됨)

#### 컬럼별 자동화 설정 (Draft)

각 컬럼에서 다음 자동화를 설정할 수 있습니다:

```
Backlog:
  - PR된 PR이 병합되면 완료로 표시

To Do:
  - 새 이슈/PR는 이 컬럼에 추가

In Progress:
  - 할당된 이슈는 이 컬럼으로 이동

Review:
  - PR이 생성되면 이 컬럼으로 이동

Done:
  - 문제가 해결되면 이 컬럼으로 이동
  - PR이 병합되면 이 컬럼으로 이동
```

### 3.3 이슈를 프로젝트에 추가

```bash
# 모든 이슈를 프로젝트 보드에 추가하는 명령:
gh project item-add <project-id> --issue <issue-number>
```

또는 Google Sheet/Excel에서:
1. 프로젝트 설정 → "Export items"
2. 스프레드시트로 추출

---

## 📈 Step 4: 메트릭 수집 (선택과제)

### 4.1 메트릭 데이터 수집

```bash
cd scripts
python collect_metrics.py
```

**생성 파일**: `reports/sprint_metrics.json`

**수집되는 메트릭:**
- Cycle Time 통계 (평균, 중앙값, 범위)
- Velocity (마일스톤별 완료 이슈)
- Lead Time (PR Merge 시간)
- Throughput (주/월별 완료 이슈)
- Burndown 상태 (마일스톤별 진행률)

### 4.2 시각화 대시보드 생성

```bash
python visualize_metrics.py
```

**생성 파일:**
```
reports/visualizations/
├── dashboard.html           # 📊 주 대시보드
├── burndown_chart.png       # 📉 Burndown Chart
├── velocity_chart.png       # 🚀 Velocity Chart
├── cycle_time_stats.png     # ⏱️ Cycle Time
└── throughput_chart.png     # 📈 Throughput
```

### 4.3 대시보드 확인

```bash
# HTML 대시보드를 브라우저에서 열기
start reports/visualizations/dashboard.html  # Windows
open reports/visualizations/dashboard.html   # macOS
xdg-open reports/visualizations/dashboard.html  # Linux
```

---

## 📊 메트릭 해석 가이드

### Cycle Time (사이클 타임)
- **정의**: 이슈 생성부터 완료까지 걸린 시간
- **목표**: 낮을수록 좋음 (개발 속도 향상)
- **개선**: 병목 제거, 작은 단위 이슈 분할

### Velocity (속도)
- **정의**: 스프린트당 완료된 이슈/포인트 수
- **목표**: 일정한 수준 유지 (예측 가능한 개발)
- **개선**: 스프린트 계획 개선, 팀 생산성 향상

### Lead Time (리드 타임)
- **정의**: PR 생성부터 Merge까지 걸린 시간
- **목표**: 짧을수록 좋음 (빠른 배포)
- **개선**: 코드 리뷰 프로세스 개선

### Throughput (처리량)
- **정의**: 기간별 완료된 이슈 수
- **목표**: 지속적 증가
- **개선**: 팀 효율성 및 프로세스 최적화

### Burndown Chart (번다운 차트)
- **정의**: 스프린트 진행 시간에 따른 남은 작업
- **목표**: 이상적 라인을 따라 선형 감소
- **신호**: 급격한 변화는 문제 발생 지표

---

## 🔄 주간 워크플로우

### 월요일: 스프린트 계획
1. 백로그에서 이슈 선택
2. 우선순위 설정 및 라벨 지정
3. Sprint 마일스톤에 추가
4. 팀원 할당

### 화-목: 개발 진행
1. "To Do" → "In Progress" 이동
2. PR 생성 시 Issue와 연결
3. "Review" 컬럼에서 코드 리뷰
4. 피드백 반영 후 Merge

### 금요일: 스프린트 리뷰
1. 완료된 이슈 확인
2. Burndown Chart 검토
3. Velocity 측정
4. 팀 회고 진행

### 매주: 메트릭 분석
```bash
python scripts/collect_metrics.py
python scripts/visualize_metrics.py
```

---

## 📝 이슈 작성 가이드

### Bug 이슈 생성
```bash
gh issue create \
  --title "[BUG] 문제 설명" \
  --label "type/bug,priority/high" \
  --milestone "Sprint 1: AI Core 구축"
```

### Feature 이슈 생성
```bash
gh issue create \
  --title "[FEATURE] 기능 설명" \
  --label "type/feature,area/ai-core" \
  --milestone "Sprint 1: AI Core 구축"
```

---

## 🐛 문제 해결

### GitHub CLI 인증 오류
```bash
# 기존 인증 제거 및 재로그인
gh auth logout
gh auth login
```

### 이미 존재하는 라벨 오류
```bash
# 오류 무시하고 계속 진행 (스크립트에 이미 처리됨)
# 기존 라벨 정보 조회
gh label list --repo minseo040203/AIOSS
```

### metrics 수집 안 됨
```bash
# 이슈/PR 확인
gh issue list --repo minseo040203/AIOSS --state all
gh pr list --repo minseo040203/AIOSS --state all
```

---

## 📚 추가 리소스

- [GitHub Projects 문서](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub CLI 가이드](https://cli.github.com/manual)
- [DORA Metrics 개요](https://cloud.google.com/blog/products/devops-sre/using-four-keys-to-measure-devops-performance)
- [칸반 보드 모범 사례](https://www.atlassian.com/agile/kanban)

---

## 💡 팁

1. **자동화 활용**: Project의 자동화 규칙을 설정해 수동 작업 최소화
2. **레이블 활용**: 다양한 라벨 조합으로 유연한 필터링
3. **마일스톤 활용**: 마일스톤으로 큰 목표 추적
4. **정기 리뷰**: 주 1회 메트릭 검토 및 팀 토론

---

**🎉 설정 완료! 이제 스프린트 개발을 시작합니다.**
