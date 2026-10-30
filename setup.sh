#!/usr/bin/env bash
# 작업 폴더에서: bash /복제한/경로/product-skill-trees/setup.sh
# 또는: bash setup.sh /기존/작업/폴더
# 기존 파일·디렉터리·심볼릭 링크는 덮어쓰지 않는다.
set -euo pipefail

usage() {
  echo "사용법: bash setup.sh [작업 폴더]"
  echo "폴더를 생략하면 현재 작업 폴더에 설치합니다."
}
fail() { echo "[오류] $*" >&2; exit 1; }

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi
[ "$#" -le 1 ] || { usage >&2; exit 1; }
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
DEST="${1:-.}"
[ -d "$DEST" ] || fail "작업 폴더를 먼저 만들어 주세요: $DEST"
DEST="$(cd "$DEST" && pwd -P)"
[ "$DEST" != "$SRC" ] || fail "스킬 저장소 자체에는 설치하지 않습니다. 별도 작업 폴더에서 실행하거나 대상 폴더를 지정하세요."

# 모든 입력·출력 디렉터리를 먼저 확인한다. 링크를 따라 다른 폴더에 쓰지 않는다.
for name in AGENTS PLAN WORKLOG; do
  [ -f "$SRC/templates/$name.template.md" ] || fail "필수 양식 없음: templates/$name.template.md"
done
[ -f "$SRC/PROMPTS.md" ] || fail "필수 파일 없음: PROMPTS.md"
for name in templates docs; do
  path="$DEST/$name"
  if [ -L "$path" ] || { [ -e "$path" ] && [ ! -d "$path" ]; }; then
    fail "$path 가 일반 디렉터리가 아닙니다. 기존 항목은 보존했으며 설치를 시작하지 않았습니다."
  fi
done

mkdir -p "$DEST/templates" "$DEST/docs"
copied=0
skipped=0
copy_new() {
  local source="$1" relative="$2" target
  target="$DEST/$relative"
  if [ -e "$target" ] || [ -L "$target" ]; then
    echo "[건너뜀] $relative (기존 항목 보존)"
    skipped=$((skipped + 1))
    return
  fi
  # noclobber는 검사 이후 같은 이름의 파일이 생겨도 덮어쓰지 않는다.
  if (set -C; cat "$source" > "$target"); then
    echo "[복사] $relative"
    copied=$((copied + 1))
  else
    fail "복사하지 못했습니다: $relative. 이미 설치된 항목은 보존됩니다."
  fi
}

# 저장소 유지보수용 AGENTS.md가 아닌, 실제 과제용 규칙을 설치한다.
copy_new "$SRC/templates/AGENTS.template.md" AGENTS.md
for name in AGENTS PLAN WORKLOG; do
  copy_new "$SRC/templates/$name.template.md" "templates/$name.template.md"
done
copy_new "$SRC/templates/PLAN.template.md" docs/PLAN.md
copy_new "$SRC/templates/WORKLOG.template.md" docs/WORKLOG.md
copy_new "$SRC/PROMPTS.md" PROMPTS.md

echo "harness ready — 복사 $copied, 건너뜀 $skipped"
echo "→ 작업 폴더: $DEST"
echo "→ 요청 문구: $DEST/PROMPTS.md 열기"
echo "→ 새로 만든 PLAN은 초안, 협업 기록은 빈 양식입니다. 실제 근거·결정으로 채워 주세요."
echo "→ Worklog는 AGENTS.md를 읽은 에이전트가 협업 중 기록합니다. 셋업은 기록 프로그램을 실행하지 않습니다."
echo "→ 기존 과제 규칙·양식을 우선합니다. 건너뛴 파일은 필요할 때 원본 양식을 참고하세요: $SRC/templates"
echo "→ 스킬 자체는 설치하지 않습니다. 등록된 스킬 또는 $SRC/skills/<스킬명>/SKILL.md를 사용하세요."
echo "→ 새 Codex 세션에서 작업 폴더의 AGENTS.md 적용을 확인하세요. 이미 실행 중이면 종료 후 다시 시작하세요."
