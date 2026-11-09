# -*- coding: utf-8 -*-
"""3순위(숫자 스프라이트) 발주서용 규격 참고도를 그린다.

  python tools/make_digit_brief.py

'같은 베이스라인·같은 글자 높이'가 말로만은 안 지켜지는 항목이라
캔버스/기준선/잉크 영역/알파 단계를 그림으로 못 박는다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # number-app
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUT = os.path.join(GAME, 'images', 'number', '_brief', 'digit_metrics.png')

# 발주 규격 (실제 캔버스 단위)
CW, CH = 224, 320          # 캔버스
CAP, BASE = 32, 288        # 글자 윗선 / 베이스라인
SIDE = 16                  # 좌우 최소 여백

BG, INK, LINE, DIM, ACC, GOLD = (10, 14, 26), (235, 250, 255), (124, 246, 255), (120, 140, 170), (255, 211, 77), (92, 255, 176)
K = 1.0                    # 패널 A 확대율(실제 크기)


def font(path, size):
    for p in (path, 'C:/Windows/Fonts/' + path):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


FK = lambda s: font('malgun.ttf', s)     # 한글 라벨
FD = lambda s: font('arialbd.ttf', s)    # 숫자


def dashed(d, x0, y0, x1, y1, col, dash=9, gap=7, w=2):
    if y0 == y1:
        x = x0
        while x < x1:
            d.line([x, y0, min(x + dash, x1), y0], fill=col, width=w); x += dash + gap
    else:
        y = y0
        while y < y1:
            d.line([x0, y, x0, min(y + dash, y1)], fill=col, width=w); y += dash + gap


def digit(d, ch, ox, oy, k, col=INK):
    """캔버스 좌상단(ox,oy)에 글자 윗선~베이스라인을 꽉 채워 숫자를 그린다."""
    want = (BASE - CAP) * k
    f = FD(int(want * 1.36))
    for _ in range(14):
        a, b = f.getbbox(ch)[1], f.getbbox(ch)[3]
        h = b - a
        if abs(h - want) <= 1:
            break
        f = FD(max(8, int(f.size * want / max(h, 1))))
    bb = f.getbbox(ch)
    d.text((ox + CW * k / 2 - (bb[0] + bb[2]) / 2, oy + CAP * k - bb[1]), ch, font=f, fill=col)


W, H = 1180, 760
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)

d.text((34, 26), '멈춰라 숫자 — 숫자 스프라이트 규격 (digit_0 ~ digit_9)', font=FK(27), fill=INK)
d.text((34, 64), '10장 모두 아래 한 틀을 공유해야 합니다. 캔버스·베이스라인·글자 높이가 어긋나면 숫자가 춤춥니다.',
       font=FK(15), fill=DIM)

# ── 패널 A : 캔버스 한 장의 치수 ──────────────────────────────────
AX, AY = 70, 130
aw, ah = int(CW * K), int(CH * K)
d.text((AX, AY - 26), 'A. 캔버스 한 장', font=FK(17), fill=GOLD)
d.rectangle([AX, AY, AX + aw, AY + ah], fill=(0, 0, 0), outline=LINE, width=2)
# 잉크 허용 폭
d.rectangle([AX + SIDE * K, AY + CAP * K, AX + aw - SIDE * K, AY + BASE * K], outline=(44, 66, 96), width=1)
digit(d, '8', AX, AY, K)
# 기준선
for y, lab, col in ((CAP, 'y=32  글자 윗선', ACC), (BASE, 'y=288  베이스라인', GOLD)):
    yy = AY + y * K
    dashed(d, AX - 34, yy, AX + aw + 12, yy, col)
    d.text((AX + aw + 20, yy - 10), lab, font=FK(14), fill=col)
# 치수
d.line([AX, AY + ah + 18, AX + aw, AY + ah + 18], fill=DIM, width=2)
d.text((AX + aw / 2 - 34, AY + ah + 26), '224 px', font=FK(15), fill=DIM)
d.line([AX - 26, AY, AX - 26, AY + ah], fill=DIM, width=2)
d.text((AX - 56, AY + ah / 2 - 30), '320\npx', font=FK(15), fill=DIM)
d.text((AX, AY + ah + 50),
       '글자 높이 = 288 - 32 = 256 px  (10장 모두 동일)\n좌우 여백 최소 16 px  ·  잉크 폭 192 px 이하  ·  가로 중앙 정렬',
       font=FK(14), fill=DIM)

# ── 패널 B : 10장이 공유하는 기준선 ───────────────────────────────
BX, BY = 560, 130
k2 = 0.62
bw, bh = int(CW * k2), int(CH * k2)
d.text((BX, BY - 26), 'B. 10장이 공유하는 기준선 (이게 핵심)', font=FK(17), fill=GOLD)
for i, ch in enumerate('1408'):
    ox = BX + i * (bw + 10)
    d.rectangle([ox, BY, ox + bw, BY + bh], fill=(0, 0, 0), outline=(44, 66, 96), width=1)
    digit(d, ch, ox, BY, k2)
    dashed(d, ox, BY + CAP * k2, ox + bw, BY + CAP * k2, ACC, 6, 5, 1)
    dashed(d, ox, BY + BASE * k2, ox + bw, BY + BASE * k2, GOLD, 6, 5, 1)
d.text((BX, BY + bh + 16),
       '· 10장 모두 글자 높이 정확히 256 px, 세로 중심 y=160 (오차 ±2 px)\n'
       '· 둥근 숫자(0 3 6 8 9)도 시각 보정 없이 같은 높이로 — 들쭉날쭉이 더 나쁩니다\n'
       '· 「1」은 잉크가 좁아도 됩니다. 캔버스는 그대로, 가로 가운데 정렬',
       font=FK(14), fill=DIM)

d.text((BX, BY + bh + 110),
       '왜 흑백 한 장인가\n'
       '게임은 숫자 색을 매 프레임 바꿉니다.\n'
       '시안 -> 과열 주황 -> 목표 노랑 / 성공 민트 / 실패 빨강 / 롤링 보라.\n'
       '그래서 스프라이트를 마스크로 씁니다. 흑백으로만 그려 주시면\n'
       '제가 명도를 그대로 투명도로 바꾸고, 색과 글로우는 코드가 입힙니다.\n'
       '투명 PNG 말고 검정 배경 불투명 PNG로 주세요 - 그게 더 정확합니다.',
       font=FK(15), fill=INK, spacing=7)

# ── 패널 C : 명도 단계 ────────────────────────────────────────────
CX, CY = 70, 600
d.text((CX, CY - 26), 'C. 검정 배경 위 흰 숫자 (명도가 그대로 투명도가 됩니다)', font=FK(17), fill=GOLD)
steps = [(255, '흰색 255', '글자 면 · 상단 하이라이트'), (185, '회색 185', '안쪽 베벨 밝은 쪽'),
         (150, '회색 150', '안쪽 베벨 어두운 쪽'), (0, '검정 0', '배경 - 투명해질 부분')]
sw, sh = 150, 74
for i, (v, lab, desc) in enumerate(steps):
    x = CX + i * (sw + 22)
    d.rectangle([x, CY, x + sw, CY + sh], fill=(v, v, v), outline=(60, 80, 110), width=1)
    d.text((x, CY + sh + 8), lab, font=FK(15), fill=INK)
    d.text((x, CY + sh + 30), desc, font=FK(13), fill=DIM)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print('%s  %s' % (os.path.relpath(OUT, GAME), im.size))
