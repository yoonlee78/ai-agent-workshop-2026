# /// script
# requires-python = ">=3.12"
# dependencies = ["faster-whisper>=1.2.1", "av>=14,<17"]
# ///
"""9-2: 영상에서 음성만 뽑아 16kHz 모노 WAV로 저장한다. ffmpeg를 따로 설치하지 않는다(PyAV가 영상을 읽는다).

    uv run 09-advanced/video/extract_audio.py 09-advanced/video/<이름>.mp4   → 같은 이름의 .wav
"""
import sys
import wave
from pathlib import Path

import numpy as np
from faster_whisper.audio import decode_audio

src = Path(sys.argv[1])
audio = decode_audio(str(src), sampling_rate=16000)  # 소리만 꺼내 16kHz 한 채널로 (값은 -1~1)
out = src.with_suffix(".wav")
with wave.open(str(out), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)  # 16비트
    w.setframerate(16000)
    w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
print(f"{out}  ({len(audio) / 16000:.0f}초)")
