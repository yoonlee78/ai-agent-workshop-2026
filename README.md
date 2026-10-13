# ai-agent-workshop-2026

Hands-on workshop: build your own research assistant with Claude Code (skills, MCP, subagents)

## 수업 전 준비 · 15~30분

워크숍 당일 바로 실습할 수 있도록, 수업 전에 설치와 환경 점검을 마쳐 주세요. git·Homebrew·GitHub 계정이 이미 있으면 15분, 처음부터 설치하면 30분 정도 걸려요.

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

**Windows라면 먼저 Git부터** 설치해 주세요. Windows의 Claude Code는 Git이 있어야 동작해요.

```powershell
winget install --id Git.Git -e
```

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
# macOS (Homebrew가 없으면 아래 Q&A의 Homebrew 설치부터)
brew install --cask codex
```

```powershell
# Windows PowerShell (Node.js가 없으면 먼저 winget install --id OpenJS.NodeJS.LTS -e 후 새 창)
npm install -g @openai/codex
```

새 터미널에서 `codex` 실행 → **Sign in with ChatGPT** → 서울대 계정으로 로그인

**확인**: `안녕`에 답이 오면 성공이에요. Claude Code는 `/exit`, Codex는 `/quit`로 나올 수 있어요.

**Orca** (강의 화면과 같은 환경을 쓰고 싶을 때)

[github.com/stablyai/orca](https://github.com/stablyai/orca) Releases에서 내 운영체제용 설치 파일을 받아 주세요. Orca는 위에서 로그인한 Claude Code·Codex 계정을 그대로 사용해요.

### 3. 나머지는 에이전트에게 맡기기

Claude Code 또는 Codex 창에 아래 내용을 통째로 붙여 넣어 주세요. 에이전트가 4~8번을 한 단계씩 설명하고 확인받으면서 대신 진행해 줘요. 직접 해야 하는 일(GitHub 로그인, 이름·이메일 입력, 설치 허락)은 에이전트가 물어볼 때 답해 주시면 돼요.

```text
워크숍 수업 전 준비를 도와줘. 나는 터미널이 처음인 초보자야.
순서대로, 한 단계씩 나에게 설명하고 확인받으면서 해줘. 에러가 나면 원인을 쉬운 말로 설명하고 고쳐줘.

1) 도구 점검·설치: git, gh(GitHub CLI), Node.js(v22 이상), uv가 있는지 확인하고, 없는 것만 허락받고 설치해.
   macOS: git이 없으면 xcode-select --install. 나머지는 brew로. brew가 없으면 Homebrew 설치를 안내하고,
   설치 끝의 Next steps 명령까지 실행하게 해. 관리자 권한이 없어 brew가 안 되면 brew 없이 설치하는 방법으로 해.
   Windows: winget으로 설치해. 명령은 &&로 잇지 말고 한 줄씩 실행해.
   새로 설치한 도구를 못 찾으면, 내가 새 터미널에서 너를 다시 열고 이 프롬프트를 다시 붙여 넣을게.
2) GitHub 로그인: gh auth status 로 확인해. 로그인이 안 되어 있거나 Token scopes에 repo가 없으면 네가 대신 하지 말고,
   내가 새 터미널 창에서 직접 실행할
   gh auth login --hostname github.com --git-protocol https --web
   명령과 화면에서 할 일을 알려줘. 토큰은 만들지 않을 거야. 내가 "로그인했어"라고 하면 다시 확인하고 gh auth setup-git 을 실행해.
3) git 이름·이메일: git config --global user.name / user.email 이 비어 있으면 나에게 물어보고 설정해.
4) 실습 저장소 받기: gh repo clone yoonlee78/ai-agent-workshop-2026 ~/ai-agent-workshop-2026
   접근이 안 되면 로그인한 아이디를 보여 주고, 초대 메일을 수락했는지 확인하라고 알려줘.
5) push 테스트: 홈 폴더에 gh-test 폴더를 만들고 README.md 하나를 커밋한 뒤
   gh repo create gh-test --private --source . --push 로 올려. 같은 이름이 있으면 gh-test2 처럼 바꿔.
   성공하면 저장소 주소를 보여 주고, GitHub에서 지우는 방법(Settings → Delete this repository)을 알려 준 뒤 내 컴퓨터의 gh-test 폴더는 지워.
6) 마지막 점검: git --version, node --version, gh --version, uvx --version, claude --version, codex --version,
   gh auth status, git config user.name, git config user.email 을 실행하고 항목별 통과/실패 표로 보여줘.
   claude와 codex는 하나만 있어도 통과야. 내 GitHub에 lab-handbook 저장소가 아직 없는지도 확인해 줘(수업 중에 만들어).
```

**확인**: 에이전트가 마지막에 보여 준 표가 모두 통과면 준비 끝이에요.

아래 4~8번은 에이전트가 하는 일을 직접 하고 싶거나, 중간에 막혔을 때 참고하는 수동 안내예요.

### 4. (수동) 도구 설치

3번 프롬프트 없이 직접 설치하려면 8번 점검표의 "실패하면" 칸 명령을 하나씩 실행해 주세요. 설치가 끝나면 새 터미널을 열어 주세요.

### 5. (수동) 터미널과 GitHub 연결

GitHub 계정이 이미 있어도 터미널에서 따로 연결해야 수업 중에 저장소를 만들고 올릴 수 있어요.

새 터미널에서 직접 실행해 주세요.

```bash
gh auth login --hostname github.com --git-protocol https --web
```

- 화면에 나온 8자리 코드를 복사 → Enter → 열린 브라우저에 붙여 넣기 → **Authorize**
- "Authenticate Git with your GitHub credentials?"를 물으면 **Y**
- 이어서 `gh auth setup-git`도 실행해 주세요.

처음 git을 쓰는 컴퓨터라면 커밋에 남길 이름과 이메일도 정해 주세요. GitHub 가입 이메일을 쓰면 돼요.

```bash
git config --global user.name "내 이름"
git config --global user.email "GitHub 가입 이메일"
```

### 6. (수동) 실습 저장소 받기

초대 메일을 받으셨다면 먼저 수락해 주세요.

```bash
gh repo clone yoonlee78/ai-agent-workshop-2026 ~/ai-agent-workshop-2026
```

`Could not resolve to a Repository`가 나오면 아직 초대가 수락되지 않은 상태예요. 수락한 뒤에도 안 되면 강사에게 GitHub 아이디를 알려 주세요.

### 7. (수동) 저장소 만들고 올리기 테스트

수업 중에 하는 "저장소 만들기 → 커밋 → GitHub에 올리기"를 미리 한 번 해 봐요. 한 줄씩 붙여 넣어 주세요 (macOS·Windows 공통).

```bash
cd ~
mkdir gh-test
cd gh-test
git init
echo test > README.md
git add README.md
git commit -m "test"
gh repo create gh-test --private --source . --push
```

**확인**: 마지막에 `https://github.com/<아이디>/gh-test` 주소가 나오고, 브라우저에서 열었을 때 README.md가 보이면 성공이에요.

테스트가 끝나면 지워 주세요.

- GitHub: 브라우저에서 `gh-test` 저장소 → **Settings** → 맨 아래 **Delete this repository**
- 내 컴퓨터: `cd ~` 후 macOS `rm -rf gh-test`, Windows `Remove-Item -Recurse -Force gh-test`

### 8. (수동) 환경 점검

새 터미널에 붙여 넣어 주세요.

```bash
git --version; node --version; gh --version; uvx --version; claude --version; codex --version; gh auth status; git config user.name; git config user.email
```

| 항목 | 통과 기준 | 실패하면 |
| --- | --- | --- |
| Git | `git version 2.x` | macOS `xcode-select --install`, Windows `winget install --id Git.Git -e` |
| Node.js | `v22` 이상 | macOS `brew install node`, Windows `winget install --id OpenJS.NodeJS.LTS -e` |
| GitHub CLI | `gh version 2.x` | macOS `brew install gh`, Windows `winget install --id GitHub.cli -e` |
| uv | `uvx 0.x` | macOS `curl -LsSf https://astral.sh/uv/install.sh \| sh`, Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Claude Code / Codex | `2.x (Claude Code)` 또는 `codex-cli 0.x` (쓰는 것 하나 이상) | 2번 설치 명령 |
| GitHub 로그인 | `Logged in to github.com account <아이디>`, `Token scopes`에 `'repo'` 포함 | 5번 다시 |
| git 이름·이메일 | 마지막 두 줄에 이름과 이메일이 나옴 | 5번의 `git config` 두 줄 |

쓰지 않는 도구(예: Codex)는 `not found`가 나와도 괜찮아요.

**확인**

- [ ] 점검 항목이 모두 통과했나요? (Claude Code·Codex는 쓰는 것만)
- [ ] `~/ai-agent-workshop-2026` 폴더가 있나요?
- [ ] 7번 테스트 저장소가 GitHub에 올라갔나요? (확인 후 지워 주세요)
- [ ] 내 GitHub에 `lab-handbook` 저장소가 **아직 없나요?** (수업 중에 만들어요)

## 자주 묻는 질문 (Q&A)

에러가 나면 먼저 여기를 찾아보세요. 없으면 에러 문구를 통째로 Claude Code나 Codex에 붙여 넣고 "초보자인데 어떻게 해?"라고 물어보세요. 그래도 해결되지 않으면 강사·조교에게 편하게 연락 주세요.

### 공통

**Q. 설치했는데 `command not found` / `인식되지 않습니다`가 나와요.**
A. 터미널을 완전히 닫고(macOS는 `Cmd` + `Q`) 새로 열어 주세요. 그래도 안 되면 컴퓨터를 재시작해 주세요.

**Q. 비밀번호를 치는데 화면에 아무것도 안 보여요.**
A. 정상이에요. 컴퓨터 로그인 비밀번호를 입력하고 Enter를 눌러 주세요.

**Q. 설치가 중간에 멈춰 있어요.**
A. 학교 와이파이에서 자주 생겨요. `Ctrl` + `C`로 멈추고 휴대폰 핫스팟으로 바꿔서 다시 해 보세요.

### Claude Code · Codex

**Q. Claude Code 로그인이 안 되거나 구독이 필요하다고 나와요.**
A. Claude 무료 플랜으로는 Claude Code를 쓸 수 없어요. Pro 이상을 구독하거나 Codex(서울대 계정)를 써 주세요. 구독 상태는 claude.ai 왼쪽 아래 이름 → 설정에서 확인할 수 있어요.

**Q. 로그인할 때 "API 키를 쓸까요?"라고 물어요.**
A. 거절해 주세요. API 키로 쓰면 구독과 별도로 요금이 나가요.

**Q. `claude`를 실행했는데 브라우저가 안 열려요.**
A. 터미널에 나온 주소를 복사해 브라우저에 직접 붙여 넣어 주세요.

**Q. macOS에서 설치는 끝났는데 계속 `claude: command not found`가 나와요.**
A. 아래 두 줄을 실행하고 새 터미널을 열어 주세요.

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Q. 실습 중에 "usage limit" / 사용량 한도 메시지가 나와요.**
A. 무료 플랜이거나 한도를 다 쓴 경우예요. 안내된 시간이 지나면 다시 쓸 수 있어요. 수업 중이라면 다른 도구(Claude Code ↔ Codex)로 바꿔서 이어 가세요.

### GitHub 연결

**Q. GitHub 계정이 없어요.**
A. [github.com/signup](https://github.com/signup)에서 만들고 이메일 인증까지 마쳐 주세요. 만든 뒤 아이디를 강사에게 알려 주세요.

**Q. `gh auth login`을 했는데 브라우저가 안 열려요.**
A. 브라우저에서 [github.com/login/device](https://github.com/login/device)를 직접 열고 터미널에 나온 8자리 코드를 입력해 주세요.

**Q. 브라우저에서 Authorize를 눌렀는데 터미널이 그대로예요.**
A. 터미널 창을 한 번 클릭하고 Enter를 눌러 주세요. 그래도 그대로면 `Ctrl` + `C`로 멈추고 `gh auth login ...`부터 다시 해 주세요.

**Q. `gh auth status`에 `You are not logged into any GitHub hosts`가 나와요.**
A. 5번의 `gh auth login` 명령을 다시 실행해 주세요.

**Q. 다른 GitHub 계정으로 로그인되어 있어요.**
A. `gh auth logout`으로 로그아웃한 뒤 5번을 다시 해 주세요.

**Q. `Token scopes`에 `'repo'`가 없어요.**
A. `gh auth refresh -s repo`를 실행하고 브라우저에서 다시 승인해 주세요.

**Q. push할 때 Username과 Password를 물어요.**
A. GitHub는 비밀번호로 push할 수 없어요. `Ctrl` + `C`로 멈추고 `gh auth setup-git`을 실행한 뒤 다시 해 주세요.

**Q. push할 때 `Permission denied` / `403` 에러가 나요.**
A. 예전에 다른 계정 정보가 컴퓨터에 저장되어 있는 경우가 많아요. `gh auth setup-git`을 실행한 뒤 다시 해 주세요. 그래도 안 되면 저장된 정보를 지워 주세요.
- macOS: **키체인 접근** 앱 → `github.com` 검색 → 항목 삭제
- Windows: **자격 증명 관리자** → Windows 자격 증명 → `git:https://github.com` 삭제

**Q. `Permission denied (publickey)`가 나와요.**
A. SSH 방식으로 연결되어 있는 경우예요. 아래를 실행한 뒤 5번을 다시 해 주세요.

```bash
gh config set git_protocol https
```

**Q. `Please tell me who you are`가 나와요.**
A. git에 이름과 이메일이 없어서 그래요. 5번의 `git config` 두 줄을 실행해 주세요.

**Q. push할 때 `GH007: Your push would publish a private email address`가 나와요.**
A. GitHub에서 이메일 비공개 설정을 켜 둔 경우예요. GitHub **Settings → Emails**에 나온 `숫자+아이디@users.noreply.github.com` 주소를 복사해서 아래처럼 바꾼 뒤, 커밋을 다시 만들어 주세요.

```bash
git config --global user.email "숫자+아이디@users.noreply.github.com"
git commit --amend --reset-author --no-edit
```

**Q. 저장소를 만들 때 `Name already exists on this account`가 나와요.**
A. 같은 이름의 저장소가 이미 있어요. 7번 테스트라면 `gh-test2`처럼 다른 이름을 쓰면 돼요.

**Q. 저장소를 받을 때 `Could not resolve to a Repository`가 나와요.**
A. 실습 저장소 초대를 아직 수락하지 않은 경우예요. 메일이나 [github.com/notifications](https://github.com/notifications)에서 초대를 수락해 주세요. 수락했는데도 안 되면 `gh auth status`로 로그인한 아이디가 강사에게 알려 준 아이디와 같은지 확인해 주세요.

### macOS (Homebrew 등)

**Q. `brew: command not found`가 나와요.**
A. Homebrew가 없는 경우예요. 아래 명령으로 설치해 주세요. 중간에 컴퓨터 비밀번호를 묻고, Enter를 눌러 계속하라고 하면 Enter를 눌러 주세요.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치 끝에 나오는 **Next steps** 아래 명령(보통 `echo ... >> ~/.zprofile`과 `eval ...` 두 줄)을 꼭 그대로 복사해 실행하고, 새 터미널을 열어 주세요.

**Q. Homebrew를 설치했는데도 `brew: command not found`가 나와요.**
A. Next steps 줄을 실행하지 않은 경우예요. 아래를 실행하고 새 터미널을 열어 주세요 (M1·M2·M3 등 Apple 칩 Mac 기준).

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Q. Homebrew 설치 중 관리자 권한이 없다고 나와요.**
A. 연구실 공용 컴퓨터처럼 관리자 계정이 아닌 경우예요. Homebrew 없이 진행하면 돼요. 3번 프롬프트를 Claude Code나 Codex에 붙여 넣으면 brew 없이 설치하는 방법으로 진행해 줘요. Node.js는 [nodejs.org](https://nodejs.org)에서 LTS 설치 파일을 받아도 돼요.

**Q. `xcrun: error: invalid active developer path`가 나와요.**
A. macOS를 업데이트한 뒤 자주 나와요. `xcode-select --install`을 실행하고, 뜨는 창에서 **설치**를 눌러 주세요 (5~15분).

**Q. `xcode-select --install`에서 "이미 설치되어 있다"고 나와요.**
A. 이미 준비된 상태예요. 다음 단계로 넘어가세요.

### Windows

**Q. `'irm' is not recognized` / `'curl' is not recognized`가 나와요.**
A. PowerShell이 아니라 명령 프롬프트(CMD)에서 실행한 경우예요. 시작 → **Windows PowerShell**을 열고, 앞에 `PS`가 보이는지 확인한 뒤 다시 해 주세요.

**Q. `이 시스템에서 스크립트를 실행할 수 없으므로`가 나와요.**
A. 아래를 실행하고 `Y`를 누른 뒤 다시 해 주세요.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Q. `winget`을 찾을 수 없다고 나와요.**
A. Microsoft Store에서 **앱 설치 관리자**(App Installer)를 설치하거나 업데이트한 뒤 PowerShell을 새로 열어 주세요.

**Q. Claude Code가 Git(Git Bash)이 필요하다고 해요.**
A. `winget install --id Git.Git -e`로 Git을 설치하고 PowerShell을 새로 연 뒤 `claude`를 다시 실행해 주세요.

**Q. `npm`을 찾을 수 없다고 나와요 (Codex 설치 중).**
A. Node.js가 없는 경우예요. `winget install --id OpenJS.NodeJS.LTS -e`로 설치하고 PowerShell을 새로 열어 주세요.

**Q. `&&`가 올바른 구분 기호가 아니라고 나와요.**
A. Windows PowerShell은 `&&`를 지원하지 않아요. 명령을 한 줄씩 나눠서 붙여 넣어 주세요.

**Q. Windows 사용자 이름이 한글이에요 (예: `C:\Users\홍길동`).**
A. 대부분 문제없지만, 일부 도구가 한글 경로에서 에러를 낼 수 있어요. 설명하기 어려운 에러가 나면 사용자 이름이 한글이라는 점과 함께 강사·조교에게 알려 주세요.
