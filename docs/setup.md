# 설치와 업데이트

과제 폴더에서 아래 명령을 실행하면 작업 규칙과 빈 양식을 준비합니다. 저장소를 복제한 실제 경로로 바꿔 주세요. Bash만 사용하며 패키지 설치나 네트워크 요청은 없습니다.

```bash
# 현재 작업 폴더에 설치
bash /복제한/경로/product-skill-trees/setup.sh

# 또는 저장소에서 기존 작업 폴더를 지정
bash setup.sh "/실제/과제 폴더"
```

| 설치할 파일 | 역할 |
| --- | --- |
| `AGENTS.md` | [과제용 작업 규칙](../templates/AGENTS.template.md): 원문 우선, 단계별 실행·확인·보고, 협업 기록과 커밋 규칙 |
| `docs/PLAN.md` | [최종 업무 계획 양식](../templates/PLAN.template.md): 앞 단계 결과를 종합해 개발 착수에 사용할 문서 |
| `docs/COLLABORATION.md` | [협업·결정 기록 양식](../templates/COLLABORATION.template.md): 시각·상대·내용·결정·근거의 다섯 열 |
| `templates/*.template.md` | 위 세 문서의 재사용 양식 |
| `PROMPTS.md` | [협업 시작·최종 계획 작성·구현 요청 문구](../PROMPTS.md) |

**기존 항목은 덮어쓰지 않습니다.** 기존 `AGENTS.md`·문서·양식과 심볼릭 링크는 그대로 두고 없는 파일만 추가합니다. `docs`나 `templates` 자체가 파일 또는 심볼릭 링크이면 쓰기 전에 중단합니다. 저장소 자체에는 설치하지 않으며, 별도의 기존 작업 폴더를 사용합니다. 저장소 루트의 [AGENTS.md](../AGENTS.md)는 저장소 유지보수 규칙이고, 설치되는 규칙은 과제용 양식입니다.

새로 설치한 PLAN은 **초안·미검토**, 협업 기록은 빈 상태입니다. 제공된 과제의 파일명·규칙·양식을 우선하고, 실제 근거와 결정을 바탕으로 채웁니다. 설치 후 새 Codex 세션에서 작업 폴더의 `AGENTS.md` 적용을 확인합니다. 이미 실행 중인 세션은 다시 시작합니다. 이 셋업은 스킬 자체를 등록하지 않으므로, 이미 등록한 스킬을 호출하거나 복제한 저장소의 `skills/<스킬명>/SKILL.md`를 지정합니다.

## 기존 프로젝트에 새 규칙 적용하기

셋업을 다시 실행해도 기존 파일은 갱신하지 않습니다. 규칙이 추가된 버전을 적용하려면 과제의 `AGENTS.md`와 [최신 과제용 양식](../templates/AGENTS.template.md)을 비교해 필요한 부분만 반영합니다. 과제에서 제공한 규칙과 실제 합의는 유지합니다.

## 다음 작업과 저장소 관리

- [요청 문구](../PROMPTS.md)로 협업을 시작하고, [최종 계획 안내](development-handoff.md)에 따라 PLAN을 작성합니다.
- 왼쪽 Browser 미리보기를 제공하는 과제에서는 [Browser 확인 규칙](../templates/AGENTS.template.md#browser에서-서비스-확인)을 따릅니다.
- 스킬 원문·출력 양식·예제를 수정하면 `python3 scripts/build_skill_guide.py`로 HTML을 갱신합니다. 흐름 요약은 `scripts/build_skill_guide.py`의 `STAGES`, 화면 구성은 `scripts/templates/skill-guide.html`에 있습니다.
- 설치 검사는 `bash -n setup.sh`와 `python3 scripts/test_setup.py`로 실행합니다. 테스트는 임시 폴더를 사용합니다.
