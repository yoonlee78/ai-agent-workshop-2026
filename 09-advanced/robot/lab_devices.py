# /// script
# requires-python = ">=3.11"
# dependencies = ["fastmcp>=2.12"]
# ///
"""9-3: 연구실 기기를 MCP 도구로 내놓는다. 기기 찾기, 설명서 읽기, 읽기, 쓰기, 절차 찾기와 실행.
MHS가 기기를 다루는 세 가지 길(MCP, 명령줄, 코드 파일) 중 MCP 길이다. 안전 한계는 device_driver.py가 지킨다."""
import asyncio
import json
from pathlib import Path

from fastmcp import Context, FastMCP

import device_driver as drv

mcp = FastMCP("lab-devices")
PROTOCOLS = drv.PROTOCOLS


@mcp.tool
def list_devices() -> str:
    """연구실에 연결된 기기 목록(아이디, 이름, 다룰 수 있는 값)."""
    return "\n".join(f"{d['id']}: {d['name']} (값: {', '.join(d['properties'])})" for d in drv.list_devices())


@mcp.tool
def describe_device(device_id: str) -> str:
    """기기 설명서. 단위, 읽기/쓰기, 한계, 안전 수칙. 기기를 다루기 전에 반드시 먼저 읽는다."""
    return drv.reference(device_id)


@mcp.tool
def read_value(device_id: str, prop: str) -> str:
    """기기의 값 하나를 읽는다. 예: incubator-1 의 temperature."""
    return f"{device_id}.{prop} = {drv.read(device_id, prop)}"


@mcp.tool
def write_value(device_id: str, prop: str, value: float | str) -> str:
    """기기의 값 하나를 바꾼다. 드라이버가 안전 한계를 넘는 값은 거절한다."""
    try:
        return f"{device_id}.{prop} → {drv.write(device_id, prop, value)}"
    except drv.SafetyError as e:
        return f"거절(안전 한계): {e}"


@mcp.tool
def list_protocols() -> str:
    """사람이 검토해 둔 절차 파일 목록(이름, 설명, 단계). 절차는 이 MCP 서버 쪽에 있으니 파일을 찾지 말고 이 도구로 본다."""
    out = []
    for p in sorted(PROTOCOLS.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out.append(f"## {p.stem}: {d['description']}\n" + "\n".join(f"  {i}. {json.dumps(st, ensure_ascii=False)}" for i, st in enumerate(d["steps"], 1)))
    return "\n".join(out) or "절차 파일이 없다"


@mcp.tool
def simulate_protocol(name: str) -> str:
    """시뮬레이터. 절차 하나(protocols/<name>.json)를 기기 상태의 복사본에서 끝까지 돌려 본다. 진짜 기기는 움직이지 않는다.
    새 절차를 짰거나 고쳤으면 run_protocol 전에 반드시 이것부터 부른다. 통과하지 못하면 어느 단계에서 왜 멈췄는지 알려 준다."""
    return drv.simulate(name)


@mcp.tool
async def run_protocol(name: str, ctx: Context) -> str:
    """list_protocols 에 있는 절차 하나(protocols/<name>.json)의 단계를 진짜 기기에서 차례로 실행한다. 단계마다 에이전트가 판단하지 않고 기기가 그대로 수행한다.
    시작하기 전에 절차가 쓰는 모든 기기의 잠금 조건(문, 작업 구역 센서)을 보고, 하나라도 걸리면 어떤 단계도 하지 않는다.
    시작한 뒤 한 단계라도 안전 한계에 걸리면 그 자리에서 멈춘다."""
    steps = json.loads((PROTOCOLS / f"{name}.json").read_text(encoding="utf-8"))["steps"]
    why = drv.check_start(steps)  # 시작하기 전에 모든 기기의 잠금 조건부터 본다
    if why:
        return f"시작하지 않음: {why}. 아무 기기도 건드리지 않았다"
    log = []
    for i, st in enumerate(steps, start=1):
        if st["do"] == "wait":
            await asyncio.sleep(st["seconds"])
            log.append(f"{i}. {st['seconds']}초 기다림 (온도 {drv.read('incubator-1', 'temperature')})")
        else:
            try:
                log.append(f"{i}. {drv.run_step(st)}")
            except drv.SafetyError as e:
                return "\n".join(log + [f"{i}. 멈춤: {e}"])
        await ctx.report_progress(i, len(steps), log[-1])
    return "\n".join(log + ["완료"])


if __name__ == "__main__":
    mcp.run(show_banner=False)
