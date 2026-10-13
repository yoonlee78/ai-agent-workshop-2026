# ai-agent-workshop-2026

Hands-on workshop: build your own research assistant with Claude Code (skills, MCP, subagents)

## 수업 전 준비 · 30분

워크숍 당일 바로 실습할 수 있도록, 수업 전에 설치와 환경 점검을 마쳐 주세요.

강의와 실습은 주로 **Claude Code**와 **[Orca](https://github.com/stablyai/orca)**(여러 코딩 에이전트를 한 화면에서 쓰는 데스크톱 앱)로 진행합니다. 튜토리얼은 Codex 등 다른 모델로도 따라 할 수 있게 만들어 두었어요.

### 준비물 (모두 필수)

- **GitHub 계정**: 없으면 [github.com/signup](https://github.com/signup)에서 만들고 이메일 인증까지 마쳐 주세요. 만든 뒤에는 **GitHub 아이디를 강사에게 알려 주세요** (실습 저장소 초대에 필요해요).
- **유료로 쓸 수 있는 AI 코딩 도구 하나 이상**
  - **Claude Code**: Claude **Pro 이상** 구독 (실습에는 Pro로 충분해요). 무료 플랜으로는 Claude Code에 로그인할 수 없어요.
  - **Codex**: 서울대 계정으로 무료로 쓸 수 있어요.
  - 개인 무료 플랜은 실습 도중 사용량 한도에 걸려 멈출 수 있어요. 둘 중 하나는 꼭 유료(또는 서울대 계정)로 쓸 수 있게 준비해 주세요.
- 내 노트북 (macOS 또는 Windows)

### 1. 터미널 열기

- macOS: `Cmd` + `Space` → **터미널**. 성공: `이름@컴퓨터 ~ %`
- Windows: 시작 → **Windows PowerShell**. 성공: `PS C:\Users\이름>` (앞에 **PS**가 있어야 해요)
- 무언가를 설치한 뒤에는 터미널을 완전히 닫고 새로 열어 주세요. 명령 멈추기: `Ctrl` + `C`

### 2. AI 코딩 도구 설치·로그인

쓸 도구를 설치해 주세요. 둘 다 설치해도 괜찮아요.

**Claude Code**

```bash
# macOS
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows PowerShell (관리자 권한 필요 없음)
irm https://claude.ai/install.ps1 | iex
```

새 터미널에서 `claude` 실행 → 브라우저에서 claude.ai 로그인 → 승인

- "Do you trust the files in this folder?" → **Yes**
- "API 키를 쓸까요?"가 나오면 거절해 주세요 (API 요금이 따로 나가요)

**Codex**

```bash
# macOS
brew install --cask codex
```

```powershell
# Windows PowerShell (Node.js가 없으면 먼저 winget install --id OpenJS.NodeJS.LTS -e)
npm install -g @openai/codex
```

새 터미널에서 `codex` 실행 → **Sign in with ChatGPT** → 서울대 계정으로 로그인

**확인**: `안녕`에 답이 오면 성공이에요. Claude Code는 `/exit`, Codex는 `/quit`로 나올 수 있어요.

**Orca** (강의 화면과 같은 환경을 쓰고 싶을 때)

[github.com/stablyai/orca](https://github.com/stablyai/orca) Releases에서 내 운영체제용 설치 파일을 받아 주세요. Orca는 위에서 로그인한 Claude Code·Codex 계정을 그대로 사용해요.

### 3. 도구 설치

Claude Code 또는 Codex 창에 아래 내용을 붙여 넣으면, 필요한 도구를 대신 확인하고 설치해 줘요.

```text
나는 터미널이 처음인 초보자야. git, gh(GitHub CLI), Node.js(v22 이상), uv가 설치되어 있는지 확인하고,
없는 것만 내 운영체제에 맞게 하나씩 설명하고 허락받은 뒤 설치해줘.
macOS는 brew가 있으면 brew로, git이 없으면 xcode-select --install. Windows는 winget으로.
```

설치가 끝나면 Claude Code(또는 Codex)를 닫고 새 터미널을 열어 주세요.

### 4. GitHub 로그인

새 터미널에서 직접 실행해 주세요.

```bash
gh auth login --hostname github.com --git-protocol https --web
```

- 화면에 나온 8자리 코드를 복사 → 브라우저에서 붙여 넣기 → **Authorize**
- 이어서 `gh auth setup-git`도 실행해 주세요.

### 5. 실습 저장소 받기

초대 메일을 받으셨다면 먼저 수락해 주세요.

```bash
gh repo clone yoonlee78/ai-agent-workshop-2026 ~/ai-agent-workshop-2026
```

`Could not resolve to a Repository`가 나오면 아직 초대가 수락되지 않은 상태예요. 수락한 뒤에도 안 되면 강사에게 GitHub 아이디를 알려 주세요.

### 6. 환경 점검

새 터미널에 붙여 넣어 주세요.

```bash
git --version; node --version; gh --version; uvx --version; claude --version; codex --version; gh auth status
```

| 항목 | 통과 기준 | 실패하면 |
| --- | --- | --- |
| Git | `git version 2.x` | macOS `xcode-select --install`, Windows `winget install --id Git.Git -e` |
| Node.js | `v22` 이상 | macOS `brew install node`, Windows `winget install --id OpenJS.NodeJS.LTS -e` |
| GitHub CLI | `gh version 2.x` | macOS `brew install gh`, Windows `winget install --id GitHub.cli -e` |
| uv | `uvx 0.x` | macOS `curl -LsSf https://astral.sh/uv/install.sh \| sh`, Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Claude Code / Codex | `2.x (Claude Code)` 또는 `codex-cli 0.x` (쓰는 것 하나 이상) | 2번 설치 명령 |
| GitHub 로그인 | `Logged in to github.com account <아이디>` | 4번 다시 |

**확인**

- [ ] 점검 항목이 모두 통과했나요? (Claude Code·Codex는 쓰는 것만)
- [ ] `~/ai-agent-workshop-2026` 폴더가 있나요?
- [ ] 내 GitHub에 `lab-handbook` 저장소가 **아직 없나요?** (수업 중에 만들어요)

### 막히면

1. `command not found` / `인식되지 않습니다`: 터미널을 완전히 닫고 새로 열어 주세요. 그래도 안 되면 컴퓨터를 재시작해 주세요.
2. Windows `'irm' is not recognized`: CMD 창에서 실행한 경우예요. PowerShell에서 다시 해 주세요.
3. macOS `brew: command not found`: Homebrew 설치 끝에 나온 Next steps 줄을 실행해 주세요.
4. Windows `스크립트를 실행할 수 없으므로`: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 실행 후 Y를 눌러 주세요.
5. Windows에 `winget`이 없음: Microsoft Store에서 "앱 설치 관리자"를 업데이트해 주세요.
6. 학교 네트워크에서 멈춤: 휴대폰 핫스팟으로 바꿔 보세요.
7. 비밀번호를 물으면 컴퓨터 로그인 비밀번호를 입력해 주세요. 화면에 안 보이는 게 정상이에요.
8. 그 밖의 에러: 문구를 통째로 Claude Code나 Codex에 붙여 넣고 "초보자인데 어떻게 해?"라고 물어보세요. 그래도 해결되지 않으면 강사·조교에게 편하게 연락 주세요.
