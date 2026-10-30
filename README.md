# Product Skill Trees

담당자 인터뷰 → 문제 정의 → 요구사항 → 해결안 선택 → 구현·검증을 돕는 **업무·제품 문제 해결 스킬 모음**입니다. 필요한 단계부터 사용하며, 문제 발굴만 요청됐다면 그 근거를 검증하고 마무리합니다.

## 설치와 업데이트

저장소를 복제한 뒤 **기존 과제 폴더**를 대상으로 실행합니다. Bash를 사용하며 패키지 설치나 네트워크 요청은 없습니다.

```bash
# 저장소 폴더에서 대상 지정
bash setup.sh "/실제/과제 폴더"

# 또는 실제 작업 폴더에서 실행
bash /복제한/경로/product-skill-trees/setup.sh
```

셋업은 대상을 확인한 뒤 과제용 `AGENTS.md`, `docs/PLAN.md`, `docs/WORKLOG.md`, 재사용 양식 3개, `PROMPTS.md`까지 **7개 파일을 복사하고 종료**합니다. 새 PLAN은 초안, Worklog는 기록 행이 없는 양식입니다. 스킬 설치·서버 실행·Codex 실행·계획 작성은 수행하지 않습니다.

**기존 파일·디렉터리·심볼릭 링크는 덮어쓰지 않습니다.** `docs`·`templates` 자체가 파일/링크이면 설치 전에 중단하며, 이 저장소 자체에는 설치하지 않습니다. 재실행으로 기존 규칙이 갱신되지는 않으므로 [최신 과제용 규칙](templates/AGENTS.template.md)과 비교해 필요한 부분을 반영하세요. 과제 원문·기존 기록을 우선하고 보존합니다.

과제 폴더에서 새 Codex 세션을 시작하고 [요청 문구](PROMPTS.md)를 사용하세요. 이미 등록한 스킬을 호출하거나 복제한 저장소의 `SKILL.md` 경로를 지정합니다. 웹 과제는 [Browser 확인 규칙](templates/AGENTS.template.md#browser에서-서비스-확인)을 따릅니다.

```text
/복제한/경로/product-skill-trees/skills/discovery-interview/SKILL.md를 읽고,
첨부한 과제와 실제 담당자 응답으로 인터뷰를 도와줘.
근거·가설·미확인을 구분하고 다음에 물을 핵심 질문 하나를 제안해줘.
```

## 어떤 스킬을 쓸까?

| 상황 | 스킬 | 결과 MD |
| --- | --- | --- |
| 불만은 있지만 구체적인 사건·부담을 모를 때 | [discovery-interview](skills/discovery-interview/SKILL.md) | `01-discovery.md` |
| 문제·원인·바꿀 행동이나 구조를 좁힐 때 | [define-problem](skills/define-problem/SKILL.md) | `02-problem-definition.md` |
| 성공 조건·제약·예외·검증 기준을 정할 때 | [clarify-requirements](skills/clarify-requirements/SKILL.md) | `03-requirements.md` |
| 대안의 효과·부담·위험을 비교하고 선택할 때 | [evaluate-solutions](skills/evaluate-solutions/SKILL.md) | `04-solution-evaluation.md` |
| 주장·계산·산출물을 원자료와 대조할 때 | [verify-work-results](skills/verify-work-results/SKILL.md) | `05-verification.md` |

기본 출력 위치는 `artifacts/<작업명>/`입니다. **Problem Space → Pain → Mechanism → Opportunity → Solution**의 판단을 문서 링크·버전·항목 ID로 연결합니다. 직접 자료로 시작할 수 있고, 수행하지 않은 단계는 만들지 않습니다. 검증은 중간에도 사용합니다.

## 분석에서 개발까지

```text
과제 원문 + 단계별 결과 + Worklog의 실제 결정
  → PLAN: 목표·타겟·문제·요구·선택한 솔루션·제외 범위·우선순위·산출물과 검증 방법
  → 요청·확정 범위의 구현 → 실제 결과 검증 → 필요한 계획 수정
```

`docs/PLAN.md`는 개발에 착수할 최종 업무 계획입니다. `docs/WORKLOG.md`에는 에이전트가 **별도 요청 없이 실제 협업·작업·검증 결과를 응답 종료 전에 기록**합니다. 셋업의 백그라운드 기능이 아니라 AGENTS 지침에 따른 기록이며, 배포본에는 과거 대화가 들어 있지 않습니다. [개발 착수 안내](docs/development-handoff.md)

## 스킬맵과 양식

- [통합 스킬맵](docs/skill-map.md): 전체 흐름·사용 시점·스킬 내부 순서·입출력·검토 기준·호출 문구
- [입력·출력 규약](docs/handoff-contract.md)
- [과제용 작업 규칙](templates/AGENTS.template.md) · [PLAN 양식](templates/PLAN.template.md) · [Worklog 양식](templates/WORKLOG.template.md)

## 후속 연계 스킬: 디자인

| 외부 스킬 | 사용할 때 |
| --- | --- |
| [frontend-design · Anthropic](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 새 화면 설계·구현 또는 디자인 방향 변경 |
| [web-design-guidelines · Vercel](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | 구현한 화면의 사용성·접근성 점검 |

필요할 때 원본에서 선택 설치합니다. [설치 명령·입출력 연결·요청 예시](skills/design-skills.md)

과제의 목표·필수 조건·제출 형식·허용 도구를 우선합니다. 가상 과제의 응답을 실제 기업의 현장 증거로 표현하지 않습니다. 설치 검사는 `bash -n setup.sh`와 `python3 scripts/test_setup.py`로 실행하며, 테스트는 임시 폴더를 사용합니다.

[MIT License](LICENSE)
