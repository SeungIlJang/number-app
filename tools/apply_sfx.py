# -*- coding: utf-8 -*-
"""neon-v1 효과음을 웹 배포용으로 최적화해 전개한다.

  python tools/apply_sfx.py

원본: D:/AI/workspace/game/sounds/number/neon-v1/sfx/  (48kHz 16bit 스테레오 WAV)
분석 결과 12kHz 이상 에너지가 사실상 0이고 좌우 차이도 미미해서,
모노 + 24kHz로 내려도 들리는 차이가 없다. 앞뒤 무음을 다듬고 끝에 짧은 페이드를 넣어
클릭음을 막는다. (ffmpeg이 없어 ogg/mp3는 만들 수 없다 — WAV 그대로 경량화)

전개처
  games/audio/number/sfx/            배포(깃헙 페이지)
  number-app/www/audio/number/sfx/   오프라인 폴백
원본은 건드리지 않는다.
"""
import os, wave, glob
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # number-app
GAME = os.path.abspath(os.path.join(ROOT, '..'))                       # workspace/game
SRC  = os.path.join(GAME, 'sounds', 'number', 'neon-v1', 'sfx')
OUTS = [os.path.join(GAME, 'games', 'audio', 'number', 'sfx'),
        os.path.join(ROOT, 'www', 'audio', 'number', 'sfx')]

OUT_SR   = 24000
SILENCE  = 0.002      # 최대 진폭 대비 이 아래는 무음 취급 (-54dB)
HEAD_PAD = 0.004      # 앞은 4ms 여유를 남겨 어택이 잘리지 않게
TAIL_PAD = 0.010      # 뒤는 10ms 여유
FADE     = 0.012      # 끝 12ms 페이드아웃 → 자른 자리 클릭음 방지


def read_wav(path):
    w = wave.open(path, 'rb')
    n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype='<i2').reshape(-1, ch).astype(np.float32) / 32768.0
    w.close()
    return d.mean(axis=1), sr


def write_wav(path, mono, sr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pcm = np.clip(mono, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype('<i2')
    w = wave.open(path, 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(pcm.tobytes()); w.close()


def process(mono, sr):
    # 1) 48k → 24k : 인접 두 샘플 평균(간단한 저역통과) 후 2배 데시메이션
    if sr % OUT_SR == 0 and sr != OUT_SR:
        f = sr // OUT_SR
        cut = (len(mono) // f) * f
        mono = mono[:cut].reshape(-1, f).mean(axis=1)
        sr = OUT_SR
    # 2) 앞뒤 무음 정리
    env = np.abs(mono)
    peak = float(env.max()) or 1.0
    nz = np.nonzero(env > peak * SILENCE)[0]
    if len(nz):
        a = max(0, nz[0] - int(HEAD_PAD * sr))
        b = min(len(mono), nz[-1] + int(TAIL_PAD * sr))
        mono = mono[a:b]
    # 3) 끝 페이드아웃
    f = min(int(FADE * sr), len(mono))
    if f > 1:
        mono = mono.copy()
        mono[-f:] *= np.linspace(1.0, 0.0, f)
    return mono, sr


def main():
    files = sorted(glob.glob(os.path.join(SRC, '*.wav')))
    if not files:
        raise SystemExit('원본 효과음을 찾지 못했습니다: ' + SRC)
    before = after = 0
    print('  파일                     원본      →   최적화')
    for p in files:
        name = os.path.basename(p)
        mono, sr = read_wav(p)
        out, osr = process(mono, sr)
        before += os.path.getsize(p)
        for d in OUTS:
            write_wav(os.path.join(d, name), out, osr)
        sz = os.path.getsize(os.path.join(OUTS[0], name))
        after += sz
        print('  %-22s %6.2fs %5dKB  →  %5.2fs %4dKB' %
              (name, len(mono) / sr, os.path.getsize(p) // 1024, len(out) / osr, sz // 1024))
    print('\n합계 %dKB → %dKB  (%.0f%% 감소)' %
          (before // 1024, after // 1024, 100 * (1 - after / before)))
    for d in OUTS:
        print('  ', os.path.relpath(d, GAME))


if __name__ == '__main__':
    main()
