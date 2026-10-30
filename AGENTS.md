# Product Skill Trees 추가 규칙

## 공통 규칙

작업 전에 [templates/AGENTS.template.md](templates/AGENTS.template.md) 전체를 읽고 공통 작업 규칙으로 적용한다. 공통 규칙을 바꿀 때는 그 파일을 수정하며, 이 문서에 같은 내용을 복제하지 않는다.

`setup.sh`는 공통 규칙 파일을 실제 과제 폴더의 `AGENTS.md`로 복사한다. 아래 저장소 전용 규칙은 설치하지 않는다.

## 저장소 정비 시 추가 규칙

아래 규칙은 이 저장소의 스킬·안내 문서·양식·셋업을 정비할 때 적용한다. 클론한 저장소를 활용해 실제 과제를 수행할 때는 공통 규칙에 따라 Worklog를 기록한다.

- 작업 전에 `README.md`와 변경 대상 스킬·양식·안내를 읽는다. 기존 다섯 스킬의 독립 실행과 필요한 단계부터 시작하는 방식을 보존한다.
- 스킬의 사용 시점·흐름·입출력 안내는 `docs/skill-map.md` 하나로 관리한다. 스킬·양식 변경 시 해당 안내와 링크도 일치시킨다.
- `setup.sh`를 바꾸면 `bash -n setup.sh`와 `python3 scripts/test_setup.py`를 실행해 빈 폴더 설치, 재실행, 기존 파일·심볼릭 링크 보존을 임시 폴더에서 확인한다.
- 배포용 `docs/WORKLOG.md`와 `templates/WORKLOG.template.md`는 기록 행 없는 양식으로 유지한다. 이 저장소의 배포본 정비 과정을 해당 파일에 채우지 않는다. 이 예외는 실제 과제의 Worklog 자동 기록을 중단하거나 기존 기록을 지울 근거가 아니다.
