# -*- coding: utf-8 -*-
"""2순위 연출 아트(판정 스탬프·버스트·체인 링크)를 웹 배포용으로 전개한다.

  python tools/apply_vfx.py

0.5초 번쩍이고 사라지는 연출이라 해상도를 표시 크기에 맞춰 낮춰도 티가 안 난다.
알파가 있는 글로우라 WebP가 PNG의 절반(500KB -> 252KB).
Android minSdk 24라 알파 WebP는 전 기기 지원된다.
못 불러와도 연출만 빠질 뿐 게임 진행에는 지장이 없다.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # number-app
GAME = os.path.abspath(os.path.join(ROOT, '..'))                       # workspace/game
SRC  = os.path.join(GAME, 'images', 'number', 'neon-v3')
OUTS = [os.path.join(GAME, 'games', 'img', 'number', 'play'),
        os.path.join(ROOT, 'www', 'img', 'number', 'play')]

# (파일, 목표 가로폭) — 표시 크기: 스탬프 약 230px / 버스트 약 240px / 링크 24px
PLAN = [
    ('stamp_perfect', 512),
    ('stamp_good',    512),
    ('stamp_miss',    512),
    ('burst_hit',     384),
    ('burst_perfect', 384),
    ('burst_chain',   384),
    ('chain_link',     96),
]
QUALITY = 90


def main():
    before = after = 0
    print('  파일                원본  ->  WebP')
    for name, width in PLAN:
        p = os.path.join(SRC, name + '.png')
        before += os.path.getsize(p)
        src = Image.open(p).convert('RGBA')
        im = src if src.width == width else src.resize(
            (width, int(round(src.height * width / src.width))), Image.LANCZOS)
        for d in OUTS:
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, name + '.webp'), 'WEBP', quality=QUALITY, method=6)
        sz = os.path.getsize(os.path.join(OUTS[0], name + '.webp'))
        after += sz
        print('  %-16s %4dKB -> %4dKB  %s' % (name, os.path.getsize(p) // 1024, sz // 1024, im.size))
    print('\n합계 %dKB -> %dKB (%.0f%% 감소)' % (before // 1024, after // 1024, 100 * (1 - after / before)))
    for d in OUTS:
        print('  ', os.path.relpath(d, GAME))


if __name__ == '__main__':
    main()
