# -*- coding: utf-8 -*-
"""숫자 스프라이트(검정 배경 흰 숫자)를 검수하고 마스크용 WebP로 전개한다.

  python tools/apply_digits.py                    # images/number/neon-v3 에서
  python tools/apply_digits.py --src _placeholder # 임시 숫자판으로 테스트

납품은 '검정 배경 위 흰 숫자'의 불투명 PNG다(발주서 참조).
게임은 이걸 마스크로 쓰므로 여기서 명도를 그대로 투명도로 옮긴다.
  RGB = 흰색 고정, 알파 = 원본 명도
검수에서 하나라도 걸리면 아무것도 쓰지 않고 멈춘다 — 높이가 어긋난 숫자가
한 장만 섞여도 플레이 중에 숫자가 위아래로 춤추기 때문이다.
"""
import os, sys
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # number-app
GAME = os.path.abspath(os.path.join(ROOT, '..'))                       # workspace/game
OUTS = [os.path.join(GAME, 'games', 'img', 'number', 'play'),
        os.path.join(ROOT, 'www', 'img', 'number', 'play')]

CW, CH, INK_H, CY, CX = 224, 320, 256, 160, 112
INK_W_WANT = 192  # 권장 잉크 폭 (여기까지는 여백이 넉넉하다)
INK_W_MAX = 208   # 이보다 넓으면 가장자리 페더가 캔버스에 잘린다
TOL = 2           # 높이·중심 허용 오차(px)
THR = 24          # 잉크로 칠 명도 하한


def measure(path):
    im = Image.open(path).convert('RGB')
    L = im.convert('L')
    bb = L.point(lambda v: 255 if v > THR else 0).getbbox()
    if not bb:
        return im, L, None
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    corners = max(L.crop(c).getextrema()[1] for c in
                  [(0, 0, 20, 20), (CW - 20, 0, CW, 20), (0, CH - 20, 20, CH), (CW - 20, CH - 20, CW, CH)]) \
        if im.size == (CW, CH) else 255
    hist = L.histogram()
    ink = sum(hist[THR + 1:]) or 1
    mid = sum(hist[120:201]) / ink
    r, g, b = im.split()
    chroma = max(ImageChops.difference(r, g).getextrema()[1], ImageChops.difference(g, b).getextrema()[1])
    return im, L, dict(size=im.size, bb=bb, h=h, w=w, cy=(bb[1] + bb[3]) / 2, cx=(bb[0] + bb[2]) / 2,
                       corner=corners, mx=L.getextrema()[1], mid=mid, chroma=chroma)


def main():
    src_name = 'neon-v3'
    if '--src' in sys.argv:
        src_name = sys.argv[sys.argv.index('--src') + 1]
    SRC = os.path.join(GAME, 'images', 'number', src_name)

    rows, bad, warn = [], [], []
    for n in range(10):
        p = os.path.join(SRC, 'digit_%d.png' % n)
        if not os.path.exists(p):
            bad.append('digit_%d.png missing' % n); continue
        im, L, m = measure(p)
        if not m:
            bad.append('digit_%d: no ink' % n); continue
        rows.append((n, p, im, L, m))
        hard = lambda c, t: None if c else bad.append('digit_%d: %s' % (n, t))
        soft = lambda c, t: None if c else warn.append('digit_%d: %s' % (n, t))
        # 하드 — 이걸 어기면 플레이 화면이 실제로 망가진다
        hard(m['size'] == (CW, CH), 'canvas %s (want %s)' % (m['size'], (CW, CH)))
        hard(abs(m['h'] - INK_H) <= TOL, 'glyph height %d (want %d+-%d)' % (m['h'], INK_H, TOL))
        hard(abs(m['cy'] - CY) <= TOL, 'center y %.1f (want %d+-%d)' % (m['cy'], CY, TOL))
        hard(abs(m['cx'] - CX) <= TOL, 'center x %.1f (want %d+-%d)' % (m['cx'], CX, TOL))
        hard(m['w'] <= INK_W_MAX, 'ink width %d (max %d, edge would clip)' % (m['w'], INK_W_MAX))
        hard(m['corner'] <= 5, 'background not black (corner max %d)' % m['corner'])
        hard(m['mx'] >= 250, 'white face not white (max luma %d)' % m['mx'])
        hard(m['chroma'] <= 6, 'has color tint (chroma spread %d)' % m['chroma'])
        # 소프트 — 보기에 아쉽지만 동작은 한다
        soft(m['w'] <= INK_W_WANT, 'ink width %d (prefer %d or less)' % (m['w'], INK_W_WANT))
        soft(m['mid'] >= 0.03, 'midtones %.1f%% (want 3%%+, looks like a flat silhouette)' % (m['mid'] * 100))

    print('  file        canvas     height   center-y  center-x   ink-w   midtone')
    for n, p, im, L, m in rows:
        print('  digit_%d   %9s  %6d  %8.1f  %8.1f  %6d  %6.1f%%' %
              (n, '%dx%d' % m['size'], m['h'], m['cy'], m['cx'], m['w'], m['mid'] * 100))

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
    for n, p, im, L, m in rows:
        before += os.path.getsize(p)
        out = Image.merge('RGBA', (Image.new('L', im.size, 255),) * 3 + (L,))
        for d in OUTS:
            os.makedirs(d, exist_ok=True)
            out.save(os.path.join(d, 'digit_%d.webp' % n), 'WEBP', lossless=True, method=6)
        after += os.path.getsize(os.path.join(OUTS[0], 'digit_%d.webp' % n))

    print('\nOK 10/10  %dKB -> %dKB  (lossless WebP: a mask lives on its edges)'
          % (before // 1024, after // 1024))
    for d in OUTS:
        print('  ', os.path.relpath(d, GAME))


if __name__ == '__main__':
    main()
