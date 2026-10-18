#!/usr/bin/env python3
"""원자료 검사 (8-4 프롬프트 인젝션, 넣기 전 검사). 위키에 넣기 전에 AI에게 내리는 지시처럼 보이는 문장을 찾는다.

    python3 .claude/skills/lab-wiki/raw_check.py 09-advanced/raw/2026-10-05-lab-meeting.md
    python3 .claude/skills/lab-wiki/raw_check.py 09-advanced/raw/   폴더 안의 .md 를 모두 본다

찾으면 줄 번호와 이유를 보여 주고 종료 코드 1로 끝난다. 없으면 0.
흔한 문구만 잡는 단순한 검사다. 통과했다고 안전한 것은 아니고, 걸렸다고 꼭 공격인 것도 아니다. 사람이 읽고 정한다.
"""
import re
import sys
from pathlib import Path

RULES = [
    ("지시 무시", r"(이전|위의?|앞의?|모든|기존)\s*(지시|규칙|명령|지침)\S*\s*(을|를)?\s*(무시|잊|따르지)|ignore\s+(all\s+|any\s+)?(previous|prior|above)|disregard\s+(all|previous|the)"),
    ("역할 바꾸기", r"너는\s*이제|지금부터\s*너는|역할을\s*바꿔|you\s+are\s+now|act\s+as\s+(an?\s+)?(admin|developer|system)"),
    ("시스템 프롬프트", r"시스템\s*프롬프트|system\s*prompt|개발자\s*모드|developer\s+mode"),
    ("AI에게 내리는 명령", r"(AI|에이전트|어시스턴트|Claude|claude|봇)\s*(는|은|에게|들은|들에게)[^.\n]{0,40}(알려\s*줘라|알려\s*줄\s*것|하라|해라|할\s*것|하십시오)"),
    ("비밀값 요구·노출", r"(비밀번호|패스워드|토큰|API\s*키|api[_ ]?key|secret|password)[^.\n]{0,30}(알려|보내|공유|출력|말해|send|reveal|print)"),
    ("밖으로 보내기", r"(curl|wget)\s+https?://|https?://\S+\?(token|key|data)="),
    ("숨긴 글", r"[​‌‍⁠﻿]|<!--.*?-->"),
]


def check(path: Path) -> list[str]:
    found = []
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for name, pattern in RULES:
            if re.search(pattern, line, re.IGNORECASE):
                found.append(f"{path}:{n}: [{name}] {line.strip()[:120]}")
    return found


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    target = Path(sys.argv[1])
    files = sorted(target.rglob("*.md")) if target.is_dir() else [target]
    found = [f for p in files for f in check(p)]
    for f in found:
        print(f)
    print(f"검사한 파일 {len(files)}개, 의심 문장 {len(found)}개" + (" → 위키에 넣기 전에 사람이 읽고 정한다" if found else ""))
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
