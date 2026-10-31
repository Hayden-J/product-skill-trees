# 후속 연계 스킬: 디자인

해결안에 웹 화면이나 제품 UI가 포함될 때 함께 쓰는 외부 스킬입니다. 이 저장소는 두 스킬의 원문·설치 방법·연결 지점을 안내합니다. 저장소를 복제한 뒤 원문을 확인하고, 필요할 때 아래 명령으로 사용하는 프로젝트에 추가할 수 있습니다.

| 스킬 · 제작자 | 사용하기 좋은 시점 | 입력 → 결과 | 원문·설치 현황 |
| --- | --- | --- | --- |
| **frontend-design · Anthropic** | 새 화면을 만들거나 디자인 방향을 바꿀 때 | 대상 사용자·요구사항·선택한 해결안·기존 디자인 → 색상·서체·레이아웃 방향, 화면 코드, 시각적 검토 | [공식 스킬](https://github.com/anthropics/skills/tree/main/skills/frontend-design) · [skills.sh](https://skills.sh/anthropics/skills/frontend-design) |
| **web-design-guidelines · Vercel** | 만든 화면의 사용성과 접근성을 점검할 때 | 화면 코드·검토 범위·최신 지침 → 키보드 조작·포커스·폼·반응형 등의 문제를 `파일:행` 단위로 보고 | [공식 스킬](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) · [skills.sh](https://skills.sh/vercel-labs/agent-skills/web-design-guidelines) |

## 기존 스킬과 연결하기

```text
docs/PLAN.md의 개발 범위·우선순위 + 03의 R-ID + 04의 선택한 S-ID
  → frontend-design: 요구와 선택한 방법에 맞춰 화면 설계·구현
  → web-design-guidelines: 화면 코드의 UI 품질 점검 → ui-review.md
  → 사용 가능한 브라우저 도구로 실제 조작 확인 → browser-test-results.md
  → 발견한 문제 수정·재점검
  → verify-work-results: 요구사항·원자료와 결과를 대조해 05-verification.md 작성
```

`frontend-design`에는 요구·제약과 실제 선택 상태를 전달합니다. `web-design-guidelines`는 검토할 파일·범위를 지정하며, 실행할 때 원본 저장소의 최신 지침을 가져옵니다. UI 점검의 통과와 업무 효과 입증은 구분합니다.

앞 단계 파일이 없으면 확인된 요구·선택과 직접 자료를 전달합니다. 디자인을 위해 01~04 문서를 모두 새로 만들 필요는 없습니다.

외부 스킬의 기본 결과 형식은 각각 다릅니다. 작업 대상은 PLAN의 R/S-ID(해당 시 U-ID·부모 S-ID)에 연결하고, 화면 검토와 브라우저 테스트는 [공통 AGENTS의 정형 Markdown 양식](../templates/AGENTS.template.md#웹-제품의-화면-검토브라우저-테스트-기록)으로 저장합니다. 각 항목에 시나리오·기대 결과·실제 결과·증거·미확인을 남기며, 코드 검토만으로 실제 조작을 확인했다고 하지 않습니다.

`05-verification.md`에는 검토 문서·리비전·확인 ID와 R/S-ID를 연결해 판단과 한계를 요약합니다. 디자인 결정·변경 이유는 `docs/WORKLOG.md`의 D-ID에 연결하고, PLAN의 범위·기준이 달라지면 함께 갱신합니다. [기록 위치와 연결 흐름](../docs/development-handoff.md#웹-제품의-검토-결과-연결)

## 필요할 때 설치하기

아래 명령은 **실제로 디자인 작업을 할 프로젝트 폴더**에서 실행합니다. 이 두 외부 스킬은 `setup.sh`의 핵심 스킬 설치 대상에 포함되지 않습니다. 네트워크 사용이 허용된 환경에서 필요할 때 설치하고, Node.js 요구 버전은 공식 설치 안내를 확인합니다. [설치 안내](https://github.com/vercel-labs/skills#install-a-skill)

```bash
npx skills add anthropics/skills --skill frontend-design -a codex
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex
```

기본 설치 범위는 해당 프로젝트이며 Codex의 프로젝트 스킬 경로는 `.agents/skills/`입니다. 여러 프로젝트에서 공통으로 쓰려면 각 명령에 `-g`를 추가합니다. [설치 옵션](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) · [Codex 설치 경로](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)

설치 후에는 다음과 같이 요청할 수 있습니다. 경로는 실제 작업 폴더에 맞게 바꿉니다.

```text
$frontend-design
docs/PLAN.md와 연결된 03-requirements.md, 04-solution-evaluation.md를 읽고,
선택된 해결안의 화면을 요청·확정된 범위와 우선순위에 따라 설계·구현해줘.
대상 사용자·기존 디자인·R-ID의 요구와 제약을 보존하고,
디자인 결정과 연결된 R/S-ID, 구현 파일 경로, 확인한 범위를
artifacts/고객온보딩/design-notes.md에 남겨줘.
실제 결정·변경 이유는 docs/WORKLOG.md의 D-ID에 연결해줘.
```

```text
$web-design-guidelines
구현한 화면 파일을 최신 지침으로 검토해줘.
PLAN의 R/S-ID와 연결하고 공통 AGENTS의 웹 검토 양식으로
시나리오·기대 결과·실제 결과·파일과 행 등 증거·미확인을
artifacts/고객온보딩/ui-review.md에 남겨줘.
검증 판단은 같은 작업의 05-verification.md에,
실제 결정·변경 이유는 docs/WORKLOG.md의 D-ID에 연결해줘.
직접 조작하지 않은 항목은 브라우저 테스트 통과로 표시하지 마.
```

```text
PLAN의 R/S-ID와 연결된 화면·기능을 사용 가능한 브라우저 도구로 확인해줘.
과제 환경의 Browser 접속 규칙을 따르고 버튼·입력·이동을 실제로 조작해줘.
공통 AGENTS의 웹 검토 양식으로 시나리오·기대 결과·실제 결과·증거·미확인을
artifacts/고객온보딩/browser-test-results.md에 남겨줘.
검증 판단은 같은 작업의 05-verification.md에,
실제 결정·변경 이유는 docs/WORKLOG.md의 D-ID에 연결해줘.
실행하지 못한 검사는 미실행과 이유를 남겨줘.
```

[최종 계획과 개발 착수](../docs/development-handoff.md) · [README로 돌아가기](../README.md)
