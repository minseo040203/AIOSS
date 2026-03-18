# 🚀 GitHub Project 스프린트 설정 - 실행 가이드

## 📌 현재 상태

✅ 완료된 작업:
- [x] 이슈 템플릿 생성 (Bug, Feature)
- [x] 20+ 라벨 체계 설정
- [x] 설정 자동화 스크립트 준비
- [x] 메트릭 수집 스크립트 준비
- [x] 시각화 대시보드 스크립트 준비

⏳ 실행 필요:
- [ ] GitHub Token 설정
- [ ] 스크립트 실행 (마일스톤, 이슈 생성)
- [ ] GitHub Project 칸반 보드 생성
- [ ] 메트릭 수집 및 시각화

---

## 🔑 Step 1: GitHub Personal Access Token 생성

### 1.1 GitHub 토큰 생성하기

1. GitHub 계정으로 로그인: https://github.com/settings/tokens/new
2. 다음 권한(scopes) 선택:
   - `repo` - 저장소 전체 접근
   - `project` - 프로젝트 접근
3. "Generate token" 클릭
4. 토큰을 안전한 곳에 복사 (다시 보내지 않음)

### 1.2 환경 변수 설정

#### Windows (PowerShell)
```powershell
$env:GITHUB_TOKEN='ghp_your_token_here'

# 확인
echo $env:GITHUB_TOKEN
```

#### Windows (Command Prompt)
```cmd
set GITHUB_TOKEN=ghp_your_token_here

# 확인
echo %GITHUB_TOKEN%
```

#### macOS/Linux
```bash
export GITHUB_TOKEN='ghp_your_token_here'

# 확인
echo $GITHUB_TOKEN

# 영구 설정 (선택)
echo "export GITHUB_TOKEN='ghp_your_token_here'" >> ~/.bashrc
source ~/.bashrc
```

---

## ⚡ Step 2: 자동 설정 스크립트 실행

### 2.1 GitHub API를 통한 설정

```bash
cd c:\AIOSS
python scripts/setup_github_project_api.py
```

**생성되는 항목:**
- ✓ 20+ 라벨 (우선순위, 타입, 상태, 영역, 스프린트)
- ✓ 2개 마일스톤 (Sprint 1, Sprint 2)
- ✓ 12개 이슈 (스프린트 필수/선택 항목)

**예상 출력:**
```
======================================================================
🚀 GitHub Project 스프린트 설정 시작
======================================================================

📌 라벨 체계 생성 중...
  ✓ 'priority/critical' 생성
  ✓ 'priority/high' 생성
  ...
✅ 라벨 설정 완료 (20 생성)

🎯 마일스톤 생성 중...
  ✓ 'Sprint 1: AI Core 구축' 마일스톤 생성
  ✓ 'Sprint 2: UI 및 통합' 마일스톤 생성
✅ 마일스톤 설정 완료 (2 생성)

📝 이슈 생성 중...
  ✓ Issue: Llama 모델 Raspberry Pi에 통합
  ✓ Issue: ChromaDB 벡터 데이터베이스 구성
  ...
✅ 이슈 설정 완료 (12 생성)

🎉 모든 설정이 완료되었습니다!
```

### 2.2 GitHub CLI 설정 (대안)

GitHub CLI가 설치되어있다면:
```bash
cd c:\AIOSS
python scripts/setup_github_project.py
```

---

## 📊 Step 3: GitHub Project 칸반 보드 생성 (수동)

GitHub API/CLI는 아직 Project 생성을 완벽히 지원하지 않으므로 수동 생성이 필요합니다.

### 3.1 Project 생성

1. GitHub 저장소로 이동:
   https://github.com/minseo040203/AIOSS

2. **Projects** 탭 클릭 (메뉴에서 찾기)

3. **New project** 버튼 클릭

4. 프로젝트 설정:
   ```
   이름: AIOSS Development Sprint
   설명: 스프린트 기반 칸반 보드
   템플릿: Kanban (칸반)
   공개도: Public
   ```

5. **Create project** 클릭

### 3.2 칸반 컬럼 설정

Project 생성 후 기본 컬럼을 다음과 같이 설정합니다:

| 순번 | 컬럼명 | 역할 | 마지막 아이템 |
|------|--------|------|------------|
| 1 | 📦 Backlog | 향후 계획 | Auto-add drafts |
| 2 | 📋 To Do | 스프린트 계획됨 | - |
| 3 | 🔨 In Progress | 현재 작업 중 | - |
| 4 | 👀 Review | 리뷰 대기 | - |
| 5 | ✅ Done | 완료됨 | Auto-add closed |

### 3.3 자동화 규칙 설정 (옵션)

각 컬럼에서 "Manage" → "Automate" 진행:

**Backlog 컬럼:**
- "Auto-add new issues and pull requests" 활성화
- Automatically sort items into this column

**Done 컬럼:**
- "Auto-add closed pull requests" 활성화
- Items closed by pull requests go here

---

## 📊 Step 4: 메트릭 수집 (선택과제)

### 4.1 메트릭 데이터 수집

```bash
cd c:\AIOSS
python scripts/collect_metrics.py
```

**생성 파일:** `reports/sprint_metrics.json`

**수집되는 메트릭:**
- **Cycle Time**: 이슈 생성 → 완료까지 (평균, 중앙값, 범위)
- **Velocity**: 마일스톤별 완료 이슈 수
- **Lead Time**: PR 생성 → Merge까지
- **Throughput**: 주/월별 완료 이슈 수
- **Burndown**: 마일스톤별 진행률

### 4.2 시각화 대시보드 생성

matplotlib 설치:
```bash
pip install matplotlib -q
```

대시보드 생성:
```bash
python scripts/visualize_metrics.py
```

**생성 파일:**
```
reports/visualizations/
├── dashboard.html           # 📊 메인 대시보드
├── burndown_chart.png       # 📉 Burndown 차트
├── velocity_chart.png       # 🚀 Velocity 차트
├── cycle_time_stats.png     # ⏱️ Cycle Time 통계
└── throughput_chart.png     # 📈 Throughput 차트
```

### 4.3 대시보드 브라우저에서 열기

```bash
# Windows
start reports/visualizations/dashboard.html

# macOS
open reports/visualizations/dashboard.html

# Linux
xdg-open reports/visualizations/dashboard.html
```

---

## 📋 생성된 이슈 목록

### Sprint 1: AI Core 구축 (2026-04-15)

| # | 이슈 제목 | 라벨 | 우선순위 |
|---|---------|------|--------|
| 1 | Llama 모델 Raspberry Pi에 통합 | type/feature, area/ai-core | 🔴 Critical |
| 2 | ChromaDB 벡터 데이터베이스 구성 | type/feature, area/rag-system | 🟠 High |
| 3 | 재난 안전 정보 데이터셋 구축 | type/feature, area/rag-system | 🟠 High |
| 4 | LangChain RAG 파이프라인 구현 | type/feature, area/rag-system | 🔴 Critical |
| 5 | 오프라인 환경에서 모델 동작 테스트 | type/test, area/ai-core | 🟠 High |

### Sprint 2: UI 및 통합 (2026-05-15)

| # | 이슈 제목 | 라벨 | 우선순위 |
|---|---------|------|--------|
| 6 | FastAPI 웹 서버 개발 | type/feature, area/ui-ux | 🟠 High |
| 7 | 웹 대시보드 UI 구현 | type/feature, area/ui-ux | 🟠 High |
| 8 | 다국어 지원 (한글, 영어) 추가 | type/enhancement, area/ui-ux | 🟡 Medium |
| 9 | 응답 시간 최적화 및 벤치마크 | type/refactor, area/ai-core | 🟡 Medium |
| 10 | 사용자 피드백 로깅 시스템 | type/feature, area/ui-ux | 🟢 Low |
| 11 | 배포 자동화 스크립트 작성 | type/feature, area/infrastructure | 🟠 High |
| 12 | 통합 테스트 스위트 구축 | type/test, area/infrastructure | 🟠 High |
| 13 | 프로젝트 문서 및 튜토리얼 작성 | type/documentation, area/documentation | 🟡 Medium |

---

## 📈 라벨 분류 체계

### 우선순위 (Priority)
- `priority/critical` 🔴 - 긴급 (즉시 작업)
- `priority/high` 🟠 - 높음 (다음 스프린트)
- `priority/medium` 🟡 - 중간 (계획 포함)
- `priority/low` 🟢 - 낮음 (백로그)

### 타입 (Type)
- `type/bug` - 버그 수정
- `type/feature` - 새 기능
- `type/enhancement` - 기능 개선
- `type/documentation` - 문서
- `type/refactor` - 코드 리팩토링
- `type/test` - 테스트

### 상태 (Status)
- `status/backlog` - 백로그
- `status/ready` - 준비됨
- `status/in-progress` - 진행 중
- `status/review` - 리뷰 대기
- `status/blocked` - 블로킹됨

### 영역 (Area)
- `area/ai-core` - AI 코어
- `area/rag-system` - RAG 시스템
- `area/ui-ux` - UI/UX
- `area/infrastructure` - 인프라
- `area/documentation` - 문서

### 스프린트 관련
- `sprint/essential` - 스프린트 필수
- `sprint/nice-to-have` - 선택사항

---

## 🔄 주간 워크플로우

### 월요일: Sprint 계획 회의
1. 백로그에서 우선순위 높은 이슈 선택
2. 팀 역량에 따라 스프린트 이슈 선정
3. 각 팀원에게 이슈 할당
4. 예상 완료일 설정

### 화-목: 개발 진행
1. "To Do" → "In Progress" 이동
2. 작업 시작
3. 커밋 메시지에 이슈 번호 포함 (`#1`, `#2` 등)
4. PR 생성 시 연결 이슈 명시
5. 코드 리뷰 → "Review" 컬럼
6. Merge 후 자동으로 "Done"으로 이동

### 금요일: Sprint 리뷰
1. 완료된 이슈 확인 및 검수
2. Velocity 측정
3. Burndown Chart 확인
4. 팀 회고

### 매주: 메트릭 분석
```bash
python scripts/collect_metrics.py
python scripts/visualize_metrics.py
```
- Cycle Time 추세 확인
- Throughput 분석
- Burndown 진행도 검토

---

## 🐛 문제 해결

### GitHub Token 오류
```
❌ GITHUB_TOKEN 환경 변수가 설정되어있지 않습니다.
```

**해결:**
```powershell
$env:GITHUB_TOKEN='ghp_your_token_here'
python scripts/setup_github_project_api.py
```

### 인증 오류
```
❌ Incorrect authentication credentials
```

**해결:**
1. Token 만료되지 않았는지 확인
2. Token 권한 (scopes) 확인
3. 새 Token 생성 후 재시도

### 마일스톤 없음
```
⚠ 마일스톤을 찾을 수 없음
```

**해결:**
먼저 스크립트 완전 실행:
```bash
python scripts/setup_github_project_api.py
```

### 이슈가 생성되지 않음
- 모든 라벨이 먼저 생성되었는지 확인
- Git hub 저장소 권한 확인
- 이슈 제목 중복 확인

---

## ✨ 완성된 설정 요소

```
✅ GitHub 저장소 (minseo040203/AIOSS)
   ├── 📋 이슈 템플릿
   │  ├── bug_report.md
   │  ├── feature_request.md
   │  └── config.yml
   │
   ├── 📝 라벨 체계 (20+)
   │  ├── 우선순위 (Critical, High, Medium, Low)
   │  ├── 타입 (Bug, Feature, Enhancement, etc.)
   │  ├── 상태 (Backlog, Ready, In Progress, Review, Blocked)
   │  ├── 영역 (AI-core, RAG-system, UI-UX, etc.)
   │  └── 스프린트 관련
   │
   ├── 🎯 마일스톤 (2개)
   │  ├── Sprint 1: AI Core 구축 (2026-04-15)
   │  └── Sprint 2: UI 및 통합 (2026-05-15)
   │
   ├── 📍 이슈 (12개+)
   │  ├── Sprint 1: 5개
   │  ├── Sprint 2: 5개
   │  └── 추가: 2개
   │
   ├── 🎨 GitHub Project (칸반)
   │  ├── 📦 Backlog
   │  ├── 📋 To Do
   │  ├── 🔨 In Progress
   │  ├── 👀 Review
   │  └── ✅ Done
   │
   └── 📊 메트릭 대시보드
      ├── Cycle Time 분석
      ├── Velocity 추적
      ├── Lead Time 측정
      ├── Throughput 계산
      └── Burndown Chart 시각화
```

---

## 🎓 학습 리소스

- [GitHub Projects 가이드](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [DORA Metrics 개요](https://cloud.google.com/blog/products/devops-sre/using-four-keys-to-measure-devops-performance)
- [칸반 보드 모범 사례](https://www.atlassian.com/agile/kanban)
- [PyGithub 문서](https://pygithub.readthedocs.io/)

---

## 🎉 설정 완료!

지금부터 스프린트 기반 개발을 시작할 수 있습니다!

**다음 단계:**
1. GitHub Token 설정
2. 설정 스크립트 실행
3. GitHub Project 칸반 보드 생성
4. 팀과 함께 첫 스프린트 시작
5. 정기적으로 메트릭 수집 및 분석

---

**질문이나 문제가 있으시면 GitHub Issues에서 문의하세요!** 😊
