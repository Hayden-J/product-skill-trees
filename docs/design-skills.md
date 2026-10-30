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
  → web-design-guidelines: 화면 코드의 UI 품질 점검
  → 발견한 문제 수정·재점검
  → verify-work-results: 요구사항·원자료와 결과를 대조해 05-verification.md 작성
```

`frontend-design`에는 요구·제약과 실제 선택 상태를 전달합니다. `web-design-guidelines`는 검토할 파일·범위를 지정하며, 실행할 때 원본 저장소의 최신 지침을 가져옵니다. UI 점검의 통과와 업무 효과 입증은 구분합니다.

외부 스킬의 기본 결과 형식은 각각 다릅니다. 이 저장소의 MD 흐름과 연결할 때는 디자인 결정·화면 파일 경로·UI 점검 결과·미확인을 남기고, `05-verification.md`의 입력표에 해당 자료와 관련 R/S-ID를 연결합니다.

## 필요할 때 설치하기

아래 명령은 **실제로 디자인 작업을 할 프로젝트 폴더**에서 실행합니다. 이 저장소 자체의 HTML을 개선할 경우에는 복제한 `product-skill-trees` 폴더에서 실행하면 됩니다. 현재 Skills CLI는 Node.js 22.20 이상을 요구합니다. [설치 안내](https://github.com/vercel-labs/skills#install-a-skill)

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
```

```text
$web-design-guidelines
구현한 화면 파일을 최신 지침으로 검토해줘.
파일·행별 문제와 검토 범위·미확인을
artifacts/고객온보딩/ui-review.md에 남겨줘.
```

[최종 계획과 개발 착수](development-handoff.md) · [README로 돌아가기](../README.md)
