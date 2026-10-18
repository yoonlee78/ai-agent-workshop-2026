# 9. 심화 예시

수업이 끝난 뒤 선택해서 한다. 안내: [GUIDE.md 9장](../GUIDE.md#9-심화-예시-위키--영상--로봇)

| 폴더·파일 | 내용 |
| --- | --- |
| `kit/lab-wiki/` | 9-1 위키 스킬(템플릿, GitHub Action 양식, 원자료 검사 `raw_check.py`). `.claude/skills/`(Codex는 `.agents/skills/`)에 복사해서 쓴다 |
| `raw/` | 9-1 위키의 원자료. 사람이 넣고, 에이전트는 고치지 않는다 |
| `wiki/` | 9-1 위키(OKF v0.2 번들). "위키 만들어줘"로 생긴다 |
| `kit/interview-transcriber.md` | 9-2 전사 담당. `.claude/agents/`에 복사해서 쓴다 |
| `video/` | 9-2 음성 뽑기·받아 적기 스크립트. 영상과 소리 파일은 올리지 않는다(`.gitignore`) |
| `robot/` | 9-3 가상 인큐베이터·로봇 팔, 드라이버와 시뮬레이터(`device_driver.py`), MCP 서버(`lab_devices.py`), 절차 파일(`protocols/`) |
