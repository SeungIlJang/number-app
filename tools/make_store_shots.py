# -*- coding: utf-8 -*-
"""플레이스토어 스크린샷 4장을 규격에 맞춰 저장한다.

  python tools/make_store_shots.py <파일1> <파일2> <파일3> <파일4>

플레이 콘솔 휴대전화 스크린샷 요건: PNG/JPEG, 각 변 320~3840px, 가로세로 16:9 또는 9:16.
브라우저 패널에서 받은 캡처가 672x1194 / 674x1198 로 조금씩 다르므로
정확히 9:16 인 675x1200 으로 통일한다(0.4% 확대라 눈에 안 보인다).

JPEG 로 받은 것을 PNG(24비트, 알파 없음)로 저장한다 — 알파가 있으면 콘솔이 거부한다.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'store-assets')
W, H = 675, 1200                      # 정확히 9:16
NAMES = ['shot1-home', 'shot2-play', 'shot3-perfect', 'shot4-rank']
CAPTION = ['홈 · 랭크와 일일 챌린지', '플레이 · 목표 숫자에서 멈추기',
           '판정 연출 · PERFECT 와 콤보 배수', '전세계 랭킹']


def main():
    src = sys.argv[1:5]
    if len(src) != 4:
        print('4장의 캡처 파일 경로를 넘겨주세요'); sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    print('  file               source        -> output      ratio   size')
    for name, cap, p in zip(NAMES, CAPTION, src):
        im = Image.open(p).convert('RGB')          # 알파 제거
        before = im.size
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        dst = os.path.join(OUT, name + '.png')
        im.save(dst, 'PNG', optimize=True)
        kb = os.path.getsize(dst) // 1024
        print('  %-18s %-13s -> %dx%d  %.4f  %4dKB   %s'
              % (name, '%dx%d' % before, W, H, W / H, kb, cap))
    print('\n9:16 = %.4f · 각 변 320~3840 안 · PNG 24bit' % (9 / 16))
    print('저장 위치:', os.path.relpath(OUT, os.path.dirname(ROOT)))


if __name__ == '__main__':
    main()
