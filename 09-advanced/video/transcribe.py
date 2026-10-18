# /// script
# requires-python = ">=3.12"
# dependencies = ["faster-whisper>=1.2.1", "av>=14,<17"]
# ///
"""9-2: 음성 파일을 받아 적는다(전사). 오픈소스 Whisper 모델을 내 컴퓨터에서 돌린다(faster-whisper).

    uv run 09-advanced/video/transcribe.py 09-advanced/video/<이름>.wav   → 같은 이름의 .segments.json
"""
import json
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel

src = Path(sys.argv[1])
model = WhisperModel("small", device="cpu", compute_type="int8")  # 처음 한 번 모델(약 500MB)을 받는다
start = time.time()
segments, info = model.transcribe(str(src), vad_filter=True)  # 언어는 알아서 찾는다. vad: 말 없는 구간은 건너뛴다
rows = []
for s in segments:
    rows.append({"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text.strip()})
    print(f"[{s.start:6.1f}s] {s.text.strip()}")
out = src.with_suffix(".segments.json")
out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{out}  언어 {info.language}, 구간 {len(rows)}개, {time.time() - start:.0f}초 걸림")
