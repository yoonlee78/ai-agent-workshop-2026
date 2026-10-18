"""9-3: 기기 드라이버. Model Hardware Standard(MHS)의 생각을 따라, 어떤 기기든 읽기(read)와 쓰기(write) 두 가지로 다룬다.
기기 설명(devices/<이름>.json)에 적힌 안전 한계는 드라이버가 지킨다. 에이전트가 무엇을 요청하든 범위 밖 값은 거절한다.
실습용 가상 기기라 실제 하드웨어 대신 상태 파일(devices/<id>.state.json)을 쓴다. 인큐베이터 온도는 맞출 온도 쪽으로 1초에 0.5°C씩 움직인다.
기기 설명에 "ros"가 있으면(로봇 팔), 움직일 때마다 ROS 2의 sensor_msgs/JointState 모양 메시지를 <id>.joint_states.jsonl 에 남긴다.

    uv run device_driver.py list
    uv run device_driver.py read incubator-1 temperature
    uv run device_driver.py write incubator-1 setpoint 30
    uv run device_driver.py reference incubator-1          에이전트용 설명서(<id>.md)를 만든다
    uv run device_driver.py echo robot-arm-1               ros2 topic echo 처럼 최근 관절 상태를 본다
    uv run device_driver.py sim robot-arm-1 zone occupied  (시험용) 센서 값을 바꾼다. 사람이 작업 구역에 들어온 것처럼
    uv run device_driver.py simulate plate-to-incubator    절차를 상태 복사본에서 미리 돌려 본다. 진짜 상태는 바뀌지 않는다
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

DEVICES = Path(__file__).parent / "devices"
PROTOCOLS = Path(__file__).parent / "protocols"
RATE = 0.5  # °C/초 (가상 기기)


class SafetyError(Exception):
    """안전 한계에 걸려 드라이버가 거절했다."""


def describe(device_id: str) -> dict:
    for p in DEVICES.glob("*.json"):
        if p.name.endswith(".state.json"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if d["id"] == device_id:
            return d
    raise KeyError(f"{device_id} 라는 기기가 없다. list 로 찾는다")


def list_devices() -> list[dict]:
    return [describe(json.loads(p.read_text(encoding="utf-8"))["id"]) for p in sorted(DEVICES.glob("*.json")) if not p.name.endswith(".state.json")]


def _state(device_id: str) -> dict:
    d = describe(device_id)
    path = DEVICES / f"{device_id}.state.json"
    s = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {**d.get("initial", {}), "t": time.time()}
    if "temperature" in s and "setpoint" in s:  # 인큐베이터: 지난번 이후 온도가 움직인 만큼
        dt, gap = time.time() - s["t"], s["setpoint"] - s["temperature"]
        s["temperature"] = round(s["temperature"] + max(-RATE * dt, min(RATE * dt, gap)), 1)
    s["t"] = time.time()
    path.write_text(json.dumps(s), encoding="utf-8")
    return s


def read(device_id: str, prop: str):
    d = describe(device_id)
    if prop not in d["properties"]:
        raise KeyError(f"{prop} 은(는) {device_id} 에 없다. 있는 것: {', '.join(d['properties'])}")
    return _state(device_id)[prop]


def write(device_id: str, prop: str, value):
    d = describe(device_id)
    spec = d["properties"].get(prop)
    if not spec or "write" not in spec["access"]:
        raise SafetyError(f"{prop} 은(는) 쓸 수 없는 값이다")
    s = _state(device_id)
    for need_prop, need in {**d.get("interlock", {}).get("*", {}), **d.get("interlock", {}).get(prop, {})}.items():
        if s.get(need_prop) != need:  # 잠금 조건: 문이 닫혀 있어야, 작업 구역이 비어 있어야
            raise SafetyError(f"{need_prop} 가 {s.get(need_prop)} 라서 {prop} 를 바꾸지 않는다 ({need_prop}={need} 이어야 한다)")
    if "choices" in spec:
        if value not in spec["choices"]:
            raise SafetyError(f"{value} 는 고를 수 있는 값({', '.join(spec['choices'])})이 아니다")
    else:
        value = float(value)
        if not spec["min"] <= value <= spec["max"]:
            raise SafetyError(f"{value:g}{spec['unit']} 는 허용 범위 {spec['min']}~{spec['max']}{spec['unit']} 밖이다")
        if abs(value - s[prop]) > spec["max_step"]:
            raise SafetyError(f"한 번에 {spec['max_step']}{spec['unit']} 넘게 바꿀 수 없다 (지금 {s[prop]:g} → 요청 {value:g}). 나눠서 바꾼다")
    s[prop] = value
    (DEVICES / f"{device_id}.state.json").write_text(json.dumps(s), encoding="utf-8")
    if "ros" in d:  # ROS 2 의 /joint_states 토픽처럼 관절 상태를 한 줄 남긴다
        joints = [k for k, v in d["properties"].items() if "write" in v["access"]]
        msg = {"topic": d["ros"]["joint_states"], "type": d["ros"]["message"], "header": {"stamp": round(time.time(), 3)},
               "name": joints, "position": [s[j] for j in joints]}
        with (DEVICES / f"{device_id}.joint_states.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    return value


def move(device_id: str, joints: dict) -> dict:
    """관절 여러 개를 한 목표로 (ROS 의 FollowJointTrajectory 목표 하나와 비슷하다). 하나라도 걸리면 거기서 멈춘다."""
    return {j: write(device_id, j, v) for j, v in joints.items()}


def check_start(steps: list) -> str | None:
    """절차를 시작하기 전에 쓰는 모든 기기의 잠금 조건을 본다. 걸리면 이유를, 아니면 None."""
    for dev in sorted({st["device"] for st in steps if "device" in st}):
        for need_prop, need in describe(dev).get("interlock", {}).get("*", {}).items():
            if read(dev, need_prop) != need:
                return f"{dev}.{need_prop} 가 {need} 가 아니다"
    return None


def run_step(st: dict) -> str:
    """절차의 한 단계(write 또는 move)를 실행하고 한 줄 기록을 돌려준다. 안전 한계에 걸리면 SafetyError."""
    if st["do"] == "write":
        write(st["device"], st["prop"], st["value"])
        return f"{st['device']}.{st['prop']} → {st['value']}"
    if st["do"] == "move":  # 로봇 팔: 관절 여러 개를 한 목표로
        move(st["device"], st["joints"])
        return f"{st['device']} → " + ", ".join(f"{j}={v}" for j, v in st["joints"].items())
    raise SafetyError(f"모르는 단계: {st.get('do')}")


def simulate(name: str) -> str:
    """시뮬레이터: 절차를 상태 파일의 복사본에서 끝까지 돌려 본다. 진짜 상태는 바뀌지 않고, 기다림은 시간을 건너뛴다.
    로봇에서 실제 팔을 움직이기 전에 시뮬레이터(Gazebo 등)로 먼저 돌려 보는 것과 같은 생각이다."""
    global DEVICES
    steps = json.loads((PROTOCOLS / f"{name}.json").read_text(encoding="utf-8"))["steps"]
    real, tmp = DEVICES, Path(tempfile.mkdtemp())
    shutil.copytree(real, tmp / "devices")
    DEVICES = tmp / "devices"
    log = [f"[시뮬레이션] {name}: {len(steps)}단계, 지금 기기 상태의 복사본에서 시작"]
    try:
        why = check_start(steps)
        if why:
            return "\n".join(log + [f"시작하지 않음: {why}"])
        for i, st in enumerate(steps, start=1):
            if st["do"] == "wait":
                for p in DEVICES.glob("*.state.json"):  # 시간을 건너뛴다: 그만큼 지난 것처럼
                    s = json.loads(p.read_text(encoding="utf-8"))
                    s["t"] -= st["seconds"]
                    p.write_text(json.dumps(s), encoding="utf-8")
                log.append(f"{i}. {st['seconds']}초 기다림 (건너뜀)")
                continue
            try:
                log.append(f"{i}. {run_step(st)}")
            except SafetyError as e:
                return "\n".join(log + [f"{i}. 멈춤: {e}", "결과: 통과 못 함. 절차를 고친 뒤 다시 시뮬레이션한다"])
        end = {d["id"]: {k: v for k, v in _state(d["id"]).items() if k != "t"} for d in list_devices()}
        return "\n".join(log + ["결과: 통과", "끝 상태: " + json.dumps(end, ensure_ascii=False)])
    finally:
        DEVICES = real
        shutil.rmtree(tmp, ignore_errors=True)


def reference(device_id: str) -> str:
    """기기 설명에서 에이전트가 읽을 설명서를 만든다 (MHS: 설명에 적은 안전 문맥으로 참고 파일을 자동 생성)."""
    d = describe(device_id)
    lines = [f"# {d['name']} (`{d['id']}`)", "", f"담당: {d['owner']}", "", "| 값 | 단위 | 읽기/쓰기 | 설명 | 한계 |", "| --- | --- | --- | --- | --- |"]
    for k, v in d["properties"].items():
        limit = f"{v['min']}~{v['max']}, 한 번에 {v['max_step']}까지" if "min" in v else (" / ".join(v["choices"]) if "choices" in v else "")
        lines.append(f"| `{k}` | {v['unit']} | {v['access']} | {v['description']} | {limit} |")
    for target, need in d.get("interlock", {}).items():
        lines.append(f"\n잠금: {'모든 값' if target == '*' else target}은(는) " + ", ".join(f"{k}={v}" for k, v in need.items()) + "일 때만 바꿀 수 있다.")
    if "ros" in d:
        lines.append(f"\nROS 2: 관절 상태 토픽 `{d['ros']['joint_states']}` ({d['ros']['message']}), 궤적 액션 `{d['ros']['trajectory_action']}`")
    lines += ["", "## 안전", ""] + [f"- {x}" for x in d["safety"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    cmd, *a = sys.argv[1:] or ["list"]
    try:
        if cmd == "list":
            for d in list_devices():
                print(f"{d['id']}\t{d['name']}\t값: {', '.join(d['properties'])}")
        elif cmd == "read":
            print(read(a[0], a[1]))
        elif cmd == "write":
            print(f"{a[1]} = {write(a[0], a[1], a[2] if not a[2].lstrip('-').replace('.', '').isdigit() else float(a[2]))}")
        elif cmd == "echo":
            log = DEVICES / f"{a[0]}.joint_states.jsonl"
            for line in (log.read_text(encoding="utf-8").splitlines()[-5:] if log.exists() else ["{}"]):
                if line == "{}":
                    print("아직 움직인 기록이 없다")
                    break
                m = json.loads(line)
                print(f"{m['topic']}  " + "  ".join(f"{n}={p:g}" for n, p in zip(m["name"], m["position"])))
        elif cmd == "sim":
            s = _state(a[0])
            s[a[1]] = a[2]
            (DEVICES / f"{a[0]}.state.json").write_text(json.dumps(s), encoding="utf-8")
            print(f"(시험) {a[0]}.{a[1]} = {a[2]}")
        elif cmd == "simulate":
            print(simulate(a[0]))
        elif cmd == "reference":
            out = DEVICES / f"{a[0]}.md"
            out.write_text(reference(a[0]), encoding="utf-8")
            print(out)
        else:
            sys.exit(__doc__)
    except (SafetyError, KeyError) as e:
        sys.exit(f"거절: {e}")
