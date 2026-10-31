# 후속 연계 스킬·도구: 개발

스킬 트리로 계획을 세운 뒤 **새 프로젝트의 코드를 만들고 검증할 때** 함께 쓰는 외부 스킬·도구입니다. 이 저장소는 원문·설치 방법·연결 지점을 안내합니다. 기술 선택과 초기 구현에는 Context7과 해당 기술의 스킬을, 웹 화면 검증에는 사용 가능한 브라우저 도구를 활용합니다. Serena는 코드가 쌓여 함수·참조 관계를 추적할 때 추가할 수 있습니다.

| 도구·스킬 · 제작자 | 사용하기 좋은 시점 | 입력 → 결과 | 원문·설치 안내 |
| --- | --- | --- | --- |
| **Context7 · Upstash** — 플러그인/MCP | 라이브러리·SDK의 초기 설정이나 버전별 API 사용법을 확인할 때 | 라이브러리명·사용 버전·질문 → 관련 문서·코드 예제 | [공식 저장소](https://github.com/upstash/context7) · [Codex 연결](https://context7.com/docs/resources/all-clients) |
| **vercel-react-best-practices · Vercel** — 스킬 | React/Next.js로 기능을 구현하거나 성능을 점검할 때 | 컴포넌트·데이터 요청·렌더링 코드 → 요청 순서·번들·재렌더링 등의 개선 | [공식 스킬](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) · [skills.sh](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) |
| **supabase-postgres-best-practices · Supabase** — 스킬 | PostgreSQL 스키마·SQL·접근 권한을 설계·검토할 때 | 데이터 요구·스키마·쿼리·실행 계획 → 인덱스·연결·RLS·SQL 점검 | [공식 스킬](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices) · [skills.sh](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices) |
| **Playwright · Microsoft** — CLI+스킬/MCP | 웹 화면이 실행되고 입력·클릭·이동을 실제로 확인할 때 | 실행 URL·시나리오·기대 결과 → 실제 조작 결과·스크린샷·로그 | [CLI+스킬](https://github.com/microsoft/playwright-cli) · [MCP](https://github.com/microsoft/playwright-mcp) |
| **Serena · Oraios** — MCP | 여러 파일의 함수·참조 관계와 변경 영향을 추적할 때 | 프로젝트 코드·변경 대상 → 심볼·참조 조회, 심볼 단위 편집 | [공식 저장소](https://github.com/oraios/serena) · [Codex 연결](https://oraios.github.io/serena/02-usage/030_clients.html#codex-cli-and-app) |
| **systematic-debugging · obra/Superpowers** — 스킬 | 오류·테스트 실패·예상 밖 동작의 원인을 찾을 때 | 재현 절차·오류·최근 변경 → 원인 조사·가설 시험·수정·재검사 | [공식 스킬](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) · [skills.sh](https://skills.sh/obra/superpowers/systematic-debugging) |

React/Next.js와 PostgreSQL 스킬은 해당 기술을 선택한 프로젝트에서 사용합니다. PostgreSQL 스킬은 Supabase 이외의 PostgreSQL에도 적용할 수 있으며, DB 접속·실행 도구는 별도로 필요합니다. 웹 화면의 설계와 UI 품질 점검은 [디자인 스킬 안내](design-skills.md)와 연결합니다.

## 기존 스킬과 연결하기

```text
docs/PLAN.md의 개발 범위·우선순위 + 03의 R-ID + 04의 선택한 S-ID
  → Context7: 선택한 기술·버전의 초기 설정과 API 근거 확인
  → 프로젝트 초기화·작은 기능 단위 구현
      ├─ React/Next.js: vercel-react-best-practices
      ├─ PostgreSQL: supabase-postgres-best-practices
      └─ 코드가 쌓여 참조 추적이 필요할 때: Serena
  → 요구·예외 조건에 맞는 테스트 실행
      └─ 웹 화면: 사용 가능한 브라우저 도구/Playwright → browser-test-results.md
  → 오류 발생 시 systematic-debugging: 재현·원인 조사·수정·재검사
  → verify-work-results: 요구사항·원자료와 결과를 대조해 05-verification.md 작성
```

앞 단계 파일이 없으면 확인된 요구·선택과 직접 자료를 전달합니다. 개발 도구를 쓰기 위해 01~04 문서를 모두 새로 만들 필요는 없습니다. Context7에서 찾은 문서의 버전은 실제 의존성과 대조하고, 확인하지 못한 API·버전은 미확인으로 남깁니다. Serena의 프로젝트 메모리는 PLAN·WORKLOG의 결정 기록과 연결해 사용합니다.

작업 대상은 PLAN의 R/S-ID(해당 시 U-ID·부모 S-ID)에 연결합니다. 구현·문서 근거는 `artifacts/<작업명>/development-notes.md`, 오류 조사와 재검사는 `debugging-notes.md`에 남길 수 있습니다. 과제 지정 경로와 기존 문서를 우선하며, 수행한 작업의 기록만 작성합니다.

브라우저 검증은 [공통 AGENTS의 정형 Markdown 양식](../templates/AGENTS.template.md#웹-제품의-화면-검토브라우저-테스트-기록)으로 `browser-test-results.md`에 저장합니다. 시나리오·기대 결과·실제 결과·증거·미확인을 남기고, 화면 표시나 코드 검토만으로 실제 조작을 확인했다고 하지 않습니다. 반복 실행할 기능 검사는 테스트 코드와 실행 결과도 함께 남깁니다.

`05-verification.md`에는 사용한 기록·리비전·확인 ID와 R/S-ID를 연결해 판단과 한계를 요약합니다. 구현 결정·변경 이유는 `docs/WORKLOG.md`의 D-ID에 연결하고, 범위·기준이 달라지면 PLAN도 갱신합니다. 도구 연결, 테스트 통과, 업무 효과 입증은 각각 구분합니다. [기록 위치와 연결 흐름](../docs/development-handoff.md#웹-제품의-검토-결과-연결)

## 필요할 때 설치하기

아래는 **Codex에서 실제 개발할 프로젝트**를 기준으로 한 선택 설치 안내입니다. 외부 도구와 스킬은 `setup.sh`의 핵심 스킬 설치 대상에 포함되지 않습니다. 과제의 허용 도구·네트워크 조건을 먼저 따르고, 이미 같은 기능을 사용할 수 있으면 기존 연결을 활용합니다.

`npx skills add ... -a codex`는 기본적으로 프로젝트의 `.agents/skills/`에 설치하며, 여러 프로젝트에서 공통으로 쓰려면 `-g`를 추가합니다. 플러그인·MCP 설정과 CLI의 전역 설치는 이 프로젝트 스킬 경로와 구분합니다. [설치 옵션](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) · [Codex 스킬 경로](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) · [MCP 설정 범위](https://learn.chatgpt.com/docs/extend/mcp)

### Context7

공식 Codex 플러그인은 호스팅 MCP와 문서 조회 스킬을 함께 제공합니다. 아래 명령으로 설치하고 안내에 따라 OAuth 로그인을 완료한 뒤 새 Codex 대화에서 사용합니다. 플러그인으로 연결했다면 같은 서버를 별도 MCP로 중복 등록하지 않습니다. [공식 설치 안내](https://context7.com/docs/resources/all-clients)

```bash
codex plugin marketplace add upstash/context7
codex plugin add context7@context7-marketplace
```

설치 후에는 실제 사용할 라이브러리 하나의 문서를 조회해 연결을 확인합니다. 플러그인을 사용할 수 없는 환경에서는 공식 안내의 직접 MCP 연결 방식을 선택하고, 해당 방식의 인증·사용량 조건을 확인합니다.

### 선택한 기술의 스킬

아래 명령 중 실제 사용하는 기술의 스킬만 설치합니다. 설치 도구의 Node.js 요구 버전은 [공식 안내](https://github.com/vercel-labs/skills)를 확인합니다.

```bash
# React/Next.js 프로젝트
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -a codex

# PostgreSQL 프로젝트
npx skills add supabase/agent-skills --skill supabase-postgres-best-practices -a codex
```

설치된 `SKILL.md`와 보조 규칙 파일을 읽을 수 있는지 확인합니다. 실제 SQL 실행·테스트에는 프로젝트의 DB 환경과 실행 명령이 필요합니다.

### Playwright

기존 브라우저 도구로 필요한 시나리오를 확인할 수 있으면 그 도구를 사용합니다. 추가 설치를 선택한다면 아래는 CLI를 전역 설치하고 스킬을 Codex 프로젝트에 추가하는 방법입니다. Playwright CLI는 Node.js 18 이상을 요구합니다. [CLI 설치](https://github.com/microsoft/playwright-cli) · [스킬 설치](https://skills.sh/microsoft/playwright-cli/playwright-cli)

```bash
npm install -g @playwright/cli@latest
npx skills add microsoft/playwright-cli --skill playwright-cli -a codex
playwright-cli --help
```

브라우저 실행 의존성을 갖춘 뒤 프로젝트의 실제 URL에서 짧은 입력·클릭 시나리오를 실행해 확인합니다. 과제 환경의 Browser 접속 규칙을 우선합니다. CLI 대신 MCP 연결이 필요한 환경에서는 [공식 MCP 안내](https://github.com/microsoft/playwright-mcp)를 따릅니다. CLI와 MCP를 모두 설치해야 하는 것은 아닙니다.

### Serena

직접 새로 만든 코드에도 사용할 수 있습니다. 이 안내에서는 함수·참조 관계를 추적할 코드가 생긴 뒤 연결합니다. `uv`를 먼저 준비하고 기본 LSP 백엔드와 사용하는 언어의 추가 의존성을 확인합니다. [공식 설치 안내](https://github.com/oraios/serena#quick-start)

```bash
uv tool install -p 3.13 serena-agent
serena init
serena setup codex
```

도구 설치와 Codex 설정, 프로젝트 활성화는 별개입니다. 공식 Codex 연결 안내의 사용자 설정 범위를 확인하고, 새 대화에서 `/mcp`로 연결 상태를 확인한 뒤 **실제 프로젝트 경로를 활성화**합니다. 함수 하나와 그 참조를 조회해 대상 프로젝트가 맞는지 확인합니다. 언어 서버·인덱싱·온보딩은 [프로젝트 안내](https://oraios.github.io/serena/02-usage/040_workflow.html)를 따릅니다. JetBrains 백엔드는 별도 플러그인이 필요하며 LSP와 기능·요금 조건이 다릅니다.

### systematic-debugging

이 스킬을 선택하면 원문이 참조하는 `test-driven-development`와 `verification-before-completion`도 함께 확인합니다. 아래는 전체 Superpowers 플러그인 대신 이 세 스킬을 프로젝트에 설치하는 명령입니다. [원문](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) · [TDD 규칙](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md) · [완료 전 검증 규칙](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)

```bash
npx skills add obra/superpowers --skill systematic-debugging test-driven-development verification-before-completion -a codex
```

TDD 원문은 실패하는 테스트를 먼저 확인하고, 테스트보다 먼저 작성한 코드는 다시 구현하도록 요구합니다. 이 작업 방식을 적용할 범위를 프로젝트 지침에 명시하고, 사용자의 실제 요청·기존 합의를 우선합니다. 원문의 `superpowers:...` 참조가 개별 설치에서 자동 인식되지 않으면 `.agents/skills/<스킬명>/SKILL.md`를 직접 지정합니다. `verification-before-completion`의 실행 증거 확인 뒤에도 업무 요구·원자료와의 대조는 기존 `verify-work-results`로 수행합니다.

### 설치 확인 후 요청하기

설치 안내 확인일은 2026-10-31입니다. 이 저장소에서 외부 도구 설치·인증·기동을 시험한 결과는 아니므로, 사용할 환경에서 설치 상태와 실제 동작을 확인합니다. 설치 확인 후에는 다음과 같이 요청할 수 있습니다. 경로는 실제 작업 폴더에 맞게 바꿉니다.

```text
docs/PLAN.md와 연결된 요구·선택 자료를 읽고 첫 구현 단위를 진행해줘.
Context7으로 선택한 라이브러리의 실제 사용 버전과 API 근거를 확인하고,
설치한 기술 스킬 중 이번 작업에 해당하는 SKILL.md를 읽어 적용해줘.
PLAN의 R/S-ID·해당 시 U-ID, 변경 파일, 문서 출처·버전,
실행 명령·결과·미확인을 artifacts/고객온보딩/development-notes.md에 남겨줘.
검증 판단은 05-verification.md에, 실제 결정·변경 이유는 WORKLOG의 D-ID에 연결해줘.
```

```text
$playwright-cli
PLAN의 R/S-ID와 연결된 웹 기능을 실제로 조작해줘.
과제 환경의 Browser 접속 규칙을 따르고 실제 서버 주소·포트를 확인해줘.
정상 입력·오류 입력·화면 이동의 기대 결과를 PLAN에서 가져와 대조하고,
공통 AGENTS의 웹 검토 양식으로 시나리오·실제 결과·증거·미확인을
artifacts/고객온보딩/browser-test-results.md에 남겨줘.
05-verification.md에 판단을 연결하고, 실행하지 못한 검사는 미실행과 이유를 적어줘.
```

```text
Serena로 현재 작업 프로젝트의 실제 경로를 활성화하고 초기 안내를 읽어줘.
PLAN에서 이번에 변경할 R/S-ID의 구현 함수와 참조 관계를 찾아 영향 범위를 확인해줘.
요청·확정 범위의 변경 후 관련 테스트를 실행하고,
파일·심볼·변경 이유·실행 결과를 artifacts/고객온보딩/development-notes.md에 남겨줘.
검증 판단은 05-verification.md에, 결정·변경 이유는 WORKLOG의 D-ID에 연결해줘.
```

```text
$systematic-debugging
실패한 R-ID의 테스트·오류 로그와 재현 절차를 읽고 원인을 조사해줘.
수정 전에 정상 사례와 비교해 가설을 검증하고, 참조하는 TDD·완료 전 검증 스킬도 읽어줘.
재현 조건·원인 근거·수정·재검사 결과·미확인을
artifacts/고객온보딩/debugging-notes.md에 남겨줘.
05-verification.md에 검증 판단을 연결하고, 실제 결정·변경 이유는 WORKLOG에 기록해줘.
```

[디자인 스킬과 연계](design-skills.md) · [최종 계획과 개발 착수](../docs/development-handoff.md) · [README로 돌아가기](../README.md)
