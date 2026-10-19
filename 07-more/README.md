# 7. 추가 실습

> 이 파일은 [워크숍 실습 가이드북](https://yoonlee78.github.io/ai-agent-workshop-2026/#7) 7장과 같은 내용이다. 애니메이션과 최신 화면은 [웹 가이드북](https://yoonlee78.github.io/ai-agent-workshop-2026/#7)에서 볼 수 있다. 원본: [GUIDE.md](../GUIDE.md#7-추가-실습)

**목표**: 실습 결과의 검증과 개인 연구 업무 적용

| | 내용 | 자료 |
| --- | --- | --- |
| 7-1 | 에이전트 결과의 오류 검출 | `07-more/verify/` |
| 7-2 | 연구 업무 맞춤 수정 | 실습에서 만든 스킬·서브에이전트 |

### 7-1. 에이전트 결과 검증

근거 표기(`파일:줄`)나 "(확인 전)" 표시가 있어도 에이전트 결과에는 오류가 남을 수 있고, 원자료 대조 같은 별도 검증을 거쳐야 드러난다. `07-more/verify/`에 실습 서브에이전트의 결과 형식을 따른 검증용 자료 3건이 있으며, 각 자료에 의도적 오류가 들어 있다.

| 과제 | 검증 대상 | 원자료 | 오류 수 |
| --- | --- | --- | --- |
| A. 미팅 노트 | `07-more/verify/a-meeting-notes.md` | `03-subagents/materials/2026-10-08-pilot-debrief.md` | 4 |
| B. 온보딩 버디 답변 | `07-more/verify/b-buddy-answers.md` | `03-subagents/handbook/01-onboarding.md` | 3 |
| C. 질문 리포트 | `07-more/verify/c-question-report.md` | `05-report/data/lab-help-2026-09.log` | 5 |

**검증 기준**

1. **수치**: 원자료 재집계 결과와의 일치 여부
2. **근거**: 표기된 `파일:줄`과 실제 내용의 일치 여부
3. **단정**: 원자료의 "미정"·"??"의 확정 표현 변환 여부
4. **누락·추가**: 원자료 대비 누락 또는 추가된 내용

**진행 순서**

1. 에이전트 없이 두 파일을 대조해 오류를 찾고 기록함.
2. 같은 과제를 에이전트에게 요청함.
3. `07-more/verify/answer/answers.md`와 결과를 비교함.

```text
07-more/verify/c-question-report.md 를 05-report/data/lab-help-2026-09.log 와 03-subagents/handbook/ 에 대조해서 틀린 곳을 모두 찾아줘. 07-more/verify/answer/answers.md 는 열지 마. 틀린 곳마다 근거 파일:줄을 달아줘.
```

**확인**: 사람이 놓친 오류, 에이전트가 놓친 오류, 에이전트의 오탐을 구분해 기록함. 양쪽 모두 놓친 오류가 가장 중요함. 에이전트 결과를 에이전트로만 검증하면 같은 오류가 반복될 수 있음.[^7]

### 7-2. 연구 업무 맞춤 수정

실습에서 만든 스킬·서브에이전트를 개인 연구 업무에 맞게 수정함. 수정은 자연어 요청으로 함(1-3 참고).

| 대상 | 요청 예시 |
| --- | --- |
| 미팅 노트 양식 | "meeting-notes 양식에 '실험 진행 상황' 칸을 추가해줘" |
| 온보딩 버디 | "우리 연구실 위키를 03-subagents/handbook/ 에 넣었어. onboarding-buddy가 이걸 근거로 답하는지 시험해줘" |
| 리포트 양식 | "report-format에 우리 학과 보고서 양식(표지, 목차)을 넣어줘" |
| 점검 기준 | "ethics-checker 기준에 생명윤리법(보건복지부)의 '연구 기록 보관' 항목을 추가해줘" |
| 논문 검색 (선택) | 2-3의 유의 사항 확인 후 Google Drive·Gmail 커넥터 연결, "이번 주 공유된 논문 PDF 목록을 정리해줘" |

[^7]: 정답 파일이 저장소 안에 있어 에이전트가 열람할 수 있으므로 프롬프트에 "열지 마"를 넣었다. 열람 여부는 화면의 `Read(...)` 줄로 확인함.

## 폴더 구성

| 폴더·파일 | 내용 |
| --- | --- |
| `verify/` | 의도적 오류를 넣은 검증용 자료 3건. 정답은 `verify/answer/answers.md` (직접 찾은 뒤에 연다) |
| `data/eyetracker-test.asc` | 시선추적 장비 점검용 시험 기록 (가상 자료) |

안내서: [웹으로 보기](https://yoonlee78.github.io/ai-agent-workshop-2026/#7) · [GUIDE.md](../GUIDE.md#7-추가-실습)
