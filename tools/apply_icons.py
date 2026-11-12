# -*- coding: utf-8 -*-
"""HUD 아이콘 8종을 검수하고 웹 배포용으로 전개한다.

  python tools/apply_icons.py

이 아이콘들은 화면에서 10.5~16px 로 보인다. 96px 캔버스의 16% 다.
그래서 캔버스 규격보다 '줄였을 때 살아남는가'가 더 중요하다 —
16px 로 줄여 가장자리 대비를 재고, 너무 밋밋해지면 경고한다.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
SRC = os.path.join(GAME, 'images', 'number', 'neon-v3')
OUTS = [os.path.join(GAME, 'games', 'img', 'number', 'ui'),
        os.path.join(ROOT, 'www', 'img', 'number', 'ui')]

NAMES = ['life', 'combo', 'coin', 'trophy', 'daily', 'shop', 'help', 'target',
         # 5순위 — 라운드 배너
         'roll', 'golden', 'stepup', 'mul', 'choice', 'fail']
CV, SAFE_LO, SAFE_HI = 96, 8, 88
LONG_LO, LONG_HI = 72, 80      # 광학 크기: 경계상자 긴 변
QUALITY = 92


def measure(p):
    im = Image.open(p).convert('RGBA')
    a = im.getchannel('A')
    bb = a.point(lambda v: 255 if v > 8 else 0).getbbox()
    if not bb:
        return im, None
    corners = max(a.crop(c).getextrema()[1] for c in
                  [(0, 0, 8, 8), (CV - 8, 0, CV, 8), (0, CV - 8, 8, CV), (CV - 8, CV - 8, CV, CV)]) \
        if im.size == (CV, CV) else 255
    # 16px 로 줄였을 때 얼마나 남는가 — 불투명 픽셀 비율과 색 대비
    small = im.resize((16, 16), Image.LANCZOS)
    sa = small.getchannel('A')
    solid = sum(1 for v in sa.getdata() if v > 160) / 256.0
    rgb = small.convert('RGB').getdata()
    lum = [0.299 * r + 0.587 * g + 0.114 * b for (r, g, b), al in zip(rgb, sa.getdata()) if al > 160]
    spread = (max(lum) - min(lum)) if len(lum) > 1 else 0
    return im, dict(size=im.size, bb=bb, w=bb[2] - bb[0], h=bb[3] - bb[1],
                    corner=corners, amax=a.getextrema()[1], solid16=solid, spread16=spread)


def main():
    rows, bad, warn = [], [], []
    for n in NAMES:
        p = os.path.join(SRC, 'ui_%s.png' % n)
        if not os.path.exists(p):
            bad.append('ui_%s.png missing' % n); continue
        im, m = measure(p)
        if not m:
            bad.append('ui_%s: fully transparent' % n); continue
        rows.append((n, p, im, m))
        hard = lambda c, t: None if c else bad.append('ui_%s: %s' % (n, t))
        soft = lambda c, t: None if c else warn.append('ui_%s: %s' % (n, t))
        hard(m['size'] == (CV, CV), 'canvas %s (want %s)' % (m['size'], (CV, CV)))
        hard(m['corner'] == 0, 'background not transparent (corner alpha %d)' % m['corner'])
        hard(m['bb'][0] >= SAFE_LO and m['bb'][1] >= SAFE_LO
             and m['bb'][2] <= SAFE_HI and m['bb'][3] <= SAFE_HI,
             'outside safe area: bbox %s (want within %d..%d)' % (m['bb'], SAFE_LO, SAFE_HI))
        hard(m['amax'] >= 250, 'never fully opaque (alpha max %d)' % m['amax'])
        long_side = max(m['w'], m['h'])
        soft(LONG_LO <= long_side <= LONG_HI,
             'long side %d (prefer %d..%d, else it looks a different size)' % (long_side, LONG_LO, LONG_HI))
        soft(m['solid16'] >= 0.12, 'at 16px only %.0f%% solid - too thin to read' % (m['solid16'] * 100))
        soft(m['spread16'] >= 30, 'at 16px luminance spread %.0f - shape may flatten into a blob' % m['spread16'])

    print('  file         canvas    bbox                long  16px:solid  16px:contrast')
    for n, p, im, m in rows:
        print('  ui_%-8s %7s  %-18s %4d  %8.0f%%  %11.0f' %
              (n, '%dx%d' % m['size'], str(m['bb']), max(m['w'], m['h']),
               m['solid16'] * 100, m['spread16']))

    if warn:
        print('\nwarnings (%d):' % len(warn))
        for w in warn:
            print('  ~', w)
    if bad:
        print('\nFAILED (%d) - nothing written:' % len(bad))
        for b in bad:
            print('  x', b)
        sys.exit(1)

    before = after = 0
    for n, p, im, m in rows:
        before += os.path.getsize(p)
        for d in OUTS:
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, 'ui_%s.webp' % n), 'WEBP', quality=QUALITY, method=6)
        after += os.path.getsize(os.path.join(OUTS[0], 'ui_%s.webp' % n))

    print('\nOK %d/%d  %dKB -> %dKB' % (len(rows), len(NAMES), before // 1024, after // 1024))
    for d in OUTS:
        print('  ', os.path.relpath(d, GAME))


if __name__ == '__main__':
    main()
