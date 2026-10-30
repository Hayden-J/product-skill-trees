#!/usr/bin/env python3
"""Build the offline guide from the repository's actual skill documents.

Run: python3 scripts/build_skill_guide.py
No third-party dependencies. Editorial flow summaries live in STAGES below;
the full instructions, output templates and examples are embedded verbatim.
"""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    {
        "slug": "discovery-interview",
        "title": "인터뷰로 근거 모으기",
        "short": "인터뷰",
        "concept": "Problem Space · Pain",
        "file": "01-discovery.md",
        "when": "불편하다는 말은 있지만, 실제로 어떤 일이 있었는지 아직 모를 때",
        "input": "과제 · 실제 담당자 응답 · 업무 자료 · 기존 인터뷰 기록",
        "ids": "E 근거 · C 사례",
        "steps": [
            ["탐색할 업무를 정한다", "누구의 어느 업무인지, 시작과 완료, 이번에 다룰 범위를 확인합니다."],
            ["최근 사례의 앞뒤를 따라간다", "계기 → 필요한 판단 → 행동·도구·인계 → 결과를 묻습니다. 질문은 한 번에 하나씩 합니다."],
            ["깊게 볼 문제와 다른 설명을 찾는다", "빈도·영향·부담을 근거로 우선순위를 좁히고, 문제가 없던 사례와 차이를 확인합니다."],
            ["사실·해석·미확인을 나누어 남긴다", "실제 발언·자료는 E-ID, 사건 흐름은 C-ID로 기록합니다. 다음 질문으로 어떤 판단이 달라질지도 적습니다."],
        ],
        "review": ["담당자의 말과 내 가설이 구분되어 있는가?", "직접 작업시간과 답변 대기시간을 나눴는가?", "다음 질문이 문제 범위나 원인 판단을 바꾸는가?"],
        "next": [["define-problem", "E/C 근거로 문제·원인·개입을 정리"], ["verify-work-results", "중요한 주장·수치를 먼저 확인"]],
        "return": "사례나 근거가 부족하면 같은 업무 장면의 실제 행동을 더 묻습니다. 지원 AI가 담당자 답변을 만들어 채우지 않습니다.",
    },
    {
        "slug": "define-problem",
        "title": "문제와 바꿀 지점 연결하기",
        "short": "문제·개입 정의",
        "concept": "Pain → Mechanism → Opportunity",
        "file": "02-problem-definition.md",
        "when": "응답과 자료는 모였지만 무엇이 문제이고 어디를 바꿔야 할지 불분명할 때",
        "input": "01의 E/C-ID · 업무 범위 · Pain · 추가 질문, 또는 직접 자료",
        "ids": "P 문제 · M 발생 과정 · O 개입 지점",
        "steps": [
            ["문제와 영향을 좁힌다", "누가 어떤 상황에서 어떤 판단·행동에 막히는지, 근거가 지지하는 범위만 P-ID로 진술합니다."],
            ["발생 과정을 설명한다", "사건·조건 → 행동·인계 → 중간 결과 → Pain을 M-ID로 연결합니다. 연결별 근거, 추정과 반례를 남깁니다."],
            ["개입할 역할·행동·구조를 찾는다", "누구의 어느 지점을 현재 상태에서 어떤 방향으로 바꿀지 O-ID로 정리합니다. 기능 이름이나 구현 방법은 별도로 둡니다."],
            ["잠정 판단과 뒤집힐 조건을 전달한다", "기대 변화·제약·미해결 질문을 넘깁니다. 원인이 잠정이면 개입 지점도 잠정으로 유지합니다."],
        ],
        "review": ["한 사례를 전체 업무의 문제로 일반화하지 않았는가?", "원인 이름만 쓰지 않고 실제 발생 과정을 연결했는가?", "개입 지점과 구체적인 해결책을 구분했는가?"],
        "next": [["clarify-requirements", "P/O를 달성할 결과·조건으로 연결"], ["evaluate-solutions", "조건이 충분하면 개입 방법 비교"], ["verify-work-results", "문제 발굴까지만 요청됐다면 근거 검증"]],
        "return": "어느 인과 연결의 증거가 부족한지 특정해 인터뷰로 돌아갑니다. 원인 입증이 끝나기 전에도 잠정 판단과 가능한 범위는 정리합니다.",
    },
    {
        "slug": "clarify-requirements",
        "title": "충족할 조건과 기준 정하기",
        "short": "요구사항",
        "concept": "기대 변화 → 충족 조건",
        "file": "03-requirements.md",
        "when": "해결안이 반드시 만족해야 할 결과·제약·검증 기준을 정할 때",
        "input": "02의 P/M/O-ID · 원하는 결과 · 원문 규정 · 실제 결정·제약",
        "ids": "R 요구 · P/O 연결 · 검증 기준",
        "steps": [
            ["목적·범위·기존 결정을 보존한다", "문제와 개입 방향을 읽고, 이미 정한 방식·도구·제출 형식을 입력 제약으로 유지합니다."],
            ["관찰 가능한 조건으로 쓴다", "명시 요구·필요 해석·AI 제안·미확정을 나누고, 각 R-ID에 P/O와 출처를 연결합니다."],
            ["완료 조건과 효과 조건을 나눈다", "산출물의 정확성과 실제 업무 부담 감소는 별도로 확인합니다. 기준값이 없으면 미확인으로 남깁니다."],
            ["누락·추가·충돌을 대조한다", "조건의 출처와 우선순위를 확인하고, 임의로 풀 수 없는 충돌과 그 영향을 전달합니다."],
        ],
        "review": ["AI의 개선 제안이 필수 요구로 바뀌지 않았는가?", "각 조건의 충족 여부를 어떤 자료로 판단하는가?", "산출물 완료를 업무 효과 입증과 구분했는가?"],
        "next": [["evaluate-solutions", "R-ID를 같은 비교 기준으로 사용"], ["verify-work-results", "완성된 산출물을 R-ID와 대조"]],
        "return": "조건이 충돌하면 영향을 받는 판단만 미확정으로 남깁니다. 자료가 충분한 조건 정리는 계속합니다.",
    },
    {
        "slug": "evaluate-solutions",
        "title": "해결안을 비교하고 선택 돕기",
        "short": "해결안 비교",
        "concept": "Opportunity → Solution → Experiment",
        "file": "04-solution-evaluation.md",
        "when": "여러 방법의 이점·비용·전제를 비교하거나 선택 전에 가정을 확인할 때",
        "input": "02의 P/M/O-ID · 03의 R-ID · 우선순위 · 선택·위임 범위",
        "ids": "S 대안 · X 실험 계획 · 실제 선택 상태",
        "steps": [
            ["서로 다른 방법을 만든다", "문제·원인·개입 지점에서 각 S-ID의 작동 방식과 기대 변화를 연결합니다. 후보 수를 억지로 맞추지 않습니다."],
            ["같은 기준으로 이점과 부담을 비교한다", "필수 조건 위반을 별도로 표시합니다. 누가 덜 일하고 누가 입력·갱신·예외 처리 업무를 더 맡는지 봅니다."],
            ["추천과 실제 선택을 구분한다", "AI 추천의 조건·대가를 밝히고 사용자 선택 또는 위임 근거를 적습니다. 선택에 의존하지 않는 문서 검증은 계속합니다."],
            ["가정을 확인할 작은 시험을 제안한다", "X-ID에 지표·대상·기간·담당·미완료 처리·판단 변경 조건을 남깁니다. 계획을 실행 결과로 기록하지 않습니다."],
        ],
        "review": ["도구 이름만 다른 대안으로 비교하지 않았는가?", "다른 역할에게 옮겨가는 업무까지 비교했는가?", "추천·사용자 선택·실험 계획·실행 결과가 구분되는가?"],
        "next": [["verify-work-results", "선택·요청 범위의 산출물과 근거 검증"], ["define-problem", "원인·개입 가설이 반박되면 재정의"]],
        "return": "효과가 불확실하면 필요한 증거를 남깁니다. 실제 선택이 필요한 실행은 선택을 기다리고, 이미 요청된 비교·근거 검증은 이어갑니다.",
    },
    {
        "slug": "verify-work-results",
        "title": "근거와 결과를 실제로 대조하기",
        "short": "검증·재검토",
        "concept": "근거 · 판단 · 실행 범위 확인",
        "file": "05-verification.md",
        "when": "인터뷰 주장·계산·분석·제안서·실행 결과가 근거에 맞는지 확인할 때",
        "input": "검토 대상·버전 · 원자료·기준 · 연결 ID · 실제 실행 증거",
        "ids": "V 대조 결과 · 한계 · 돌아갈 문서·항목",
        "steps": [
            ["대상·버전·검증 범위를 고정한다", "현재 문서가 어떤 입력 버전을 사용했는지 확인합니다. 원자료 대조·기능 시험·운영 효과를 나눕니다."],
            ["기대 판단을 별도로 도출한다", "원자료와 규칙으로 기대값을 만들고 실제 결과와 대조합니다. 개별 정확성과 전체 정합성을 따로 확인합니다."],
            ["연결과 상태를 추적한다", "E → P → M → O → R → S의 실제 참조와 가설 상태를 확인합니다. 수행하지 않은 단계까지 강제로 만들지 않습니다."],
            ["불일치·수정·한계를 남긴다", "V-ID로 판정·확인 주체·방법·범위를 기록합니다. 요청된 수정은 재검사하고, 미실행·판단 불가는 그대로 남깁니다."],
        ],
        "review": ["실제로 확인한 범위보다 결론을 넓히지 않았는가?", "AI 확인과 사용자의 직접 검토를 구분했는가?", "불일치를 고칠 문서·항목·다음 증거가 특정되어 있는가?"],
        "next": [["discovery-interview", "응답·원자료가 부족한 경우"], ["define-problem", "원인·개입 연결이 잘못된 경우"], ["clarify-requirements", "기준·조건이 충돌하는 경우"], ["evaluate-solutions", "대안 전제·개입 효과를 재검토할 경우"]],
        "return": "문제 발굴만 했다면 01·02만 검증해도 됩니다. 검증 결과를 사용자에게 전달하거나 실제 필요한 앞 단계로 돌아갑니다. 설명 연습은 요청된 경우에만 진행합니다.",
    },
]


def source(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    return {"path": "../" + path, "text": text,
            "sha256": hashlib.sha256(text.encode()).hexdigest()}


def build():
    stages = []
    for stage in STAGES:
        skill = "skills/" + stage["slug"]
        stages.append({**stage, "documents": {
            "rules": source(skill + "/SKILL.md"),
            "template": source(skill + "/assets/output-template.md"),
            "example": source("docs/examples/onboarding/" + stage["file"]),
        }})
    data = {"stages": stages, "source": source("docs/examples/onboarding/source.md")}
    # Escape '<' so document text can never close its JSON script element.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    shell = (ROOT / "scripts/templates/skill-guide.html").read_text(encoding="utf-8")
    assert shell.count("__SKILL_GUIDE_DATA__") == 1
    target = ROOT / "docs/skill-guide.html"
    target.write_text(shell.replace("__SKILL_GUIDE_DATA__", payload), encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)} from 16 Markdown files ({target.stat().st_size:,} bytes).")


if __name__ == "__main__":
    build()
