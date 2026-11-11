# -*- coding: utf-8 -*-
"""5순위(라운드 배너 아이콘) 발주서용 규격 참고도를 그린다.

  python tools/make_banner_brief.py

이번 발주에서 망할 수 있는 건 두 가지다.
 1) 이미 들어간 HUD 아이콘 8종과 따로 노는 것 — 한 게임 안에서 두 가족이 싸운다.
 2) 곱하기(x)와 실패(X)가 둘 다 X 모양이라 헷갈리는 것.
그래서 기존 8종을 실제로 붙여 보여주고, 두 X 의 구분을 그림으로 못 박는다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
UI = os.path.join(GAME, 'games', 'img', 'number', 'ui')
OUT = os.path.join(GAME, 'images', 'number', '_brief', 'banner_metrics.png')

BG, INK, DIM, GOLD, MINT, RED = (10, 14, 26), (235, 250, 255), (120, 140, 170), (255, 211, 77), (92, 255, 176), (255, 90, 110)
CYAN, PURPLE = (124, 246, 255), (201, 163, 255)
HAVE = ['life', 'combo', 'coin', 'trophy', 'daily', 'shop', 'help', 'target']


def font(path, size):
    for p in (path, 'C:/Windows/Fonts/' + path):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


FK = lambda s: font('malgun.ttf', s)


def paste_icon(im, name, xy, px):
    p = os.path.join(UI, 'ui_%s.webp' % name)
    if not os.path.exists(p):
        return False
    ic = Image.open(p).convert('RGBA').resize((px, px), Image.LANCZOS)
    im.paste(ic, xy, ic)
    return True


W, H = 1180, 900
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)

d.text((34, 24), '멈춰라 숫자 — 라운드 배너 아이콘 규격 (96 x 96, 투명 PNG)', font=FK(26), fill=INK)
d.text((34, 60), '4순위 HUD 아이콘과 같은 규격·같은 형식입니다. 다른 건 쓰이는 자리와 크기뿐입니다.',
       font=FK(15), fill=DIM)

# ── 패널 A : 이미 들어간 8종 (스타일 기준) ────────────────────────
AX, AY = 60, 118
d.text((AX, AY - 28), 'A. 이미 게임에 들어간 8종 — 이 가족에 들어가야 합니다', font=FK(17), fill=GOLD)
ok = 0
for i, n in enumerate(HAVE):
    x = AX + i * 76
    d.rectangle([x, AY, x + 64, AY + 64], fill=(0, 0, 0), outline=(44, 66, 96), width=1)
    if paste_icon(im, n, (x + 4, AY + 4), 56):
        ok += 1
    d.text((x + 2, AY + 70), n, font=FK(11), fill=DIM)
d.text((AX, AY + 94),
       '같은 광원(위에서 아래) · 같은 선 굵기 · 같은 디테일 수준 · 정면 평면 · 어두운 외곽선 없음.\n'
       '새로 그릴 6종이 이 줄 옆에 섰을 때 "같은 사람이 그렸다"로 보여야 합니다.',
       font=FK(15), fill=INK, spacing=6)

# ── 패널 B : 곱하기 X 와 실패 X 구분 ──────────────────────────────
BY = 300
d.text((60, BY - 4), 'B. 곱하기(x)와 실패(X)는 반드시 달라 보여야 합니다', font=FK(17), fill=GOLD)
d.text((60, BY + 26), '둘 다 X 모양이라 이번 발주에서 제일 헷갈리기 쉬운 부분입니다.', font=FK(14), fill=DIM)

bx, by = 70, BY + 60
# 곱하기 — 가는 사선 십자, 보라, 테두리 없음
d.rectangle([bx, by, bx + 150, by + 150], fill=(0, 0, 0), outline=(44, 66, 96), width=1)
for a, b, c, e in [(38, 38, 112, 112), (112, 38, 38, 112)]:
    d.line([bx + a, by + b, bx + c, by + e], fill=PURPLE, width=14)
d.text((bx, by + 160), '곱하기 — 보라 #c9a3ff', font=FK(15), fill=PURPLE)
d.text((bx, by + 184), '가는 사선 십자, 테두리 없음\n수학 기호로 읽히게', font=FK(13), fill=DIM, spacing=4)

# 실패 — 굵은 X 가 둥근 사각 안에, 빨강
cx2 = bx + 230
d.rectangle([cx2, by, cx2 + 150, by + 150], fill=(0, 0, 0), outline=(44, 66, 96), width=1)
d.rounded_rectangle([cx2 + 24, by + 24, cx2 + 126, by + 126], radius=26, fill=RED)
for a, b, c, e in [(52, 52, 98, 98), (98, 52, 52, 98)]:
    d.line([cx2 + a, by + b, cx2 + c, by + e], fill=(14, 10, 16), width=15)
d.text((cx2, by + 160), '실패 — 빨강 #ff5a6e', font=FK(15), fill=RED)
d.text((cx2, by + 184), '굵은 X 가 채워진 둥근 사각 안에\n한눈에 "틀렸다"로 읽히게', font=FK(13), fill=DIM, spacing=4)

d.text((cx2 + 200, by + 10),
       '구분 원칙\n'
       '· 곱하기는 선만, 실패는 면(배경 도형)이 있습니다\n'
       '· 곱하기는 가늘고, 실패는 굵습니다\n'
       '· 색이 보라 / 빨강으로 다릅니다\n'
       '· 16px 로 줄여서 나란히 놓고 헷갈리면 다시 그려주세요',
       font=FK(15), fill=INK, spacing=8)

# ── 패널 C : 실제 표시 크기 ───────────────────────────────────────
CY = 680
d.text((60, CY - 4), 'C. 실제 표시 크기 — 4순위보다 큽니다', font=FK(17), fill=GOLD)
rows = [('라운드 배너', 28, '"롤링! 감으로 STOP" 처럼 0.9초간 크게 뜹니다'),
        ('게임오버 제목', 34, '"실패!" 앞 — 실패 아이콘만 여기에 쓰입니다')]
for i, (lab, px, note) in enumerate(rows):
    y = CY + 34 + i * 54
    d.rectangle([62, y, 62 + px, y + px], outline=(60, 80, 110), width=1)
    d.text((70 + px, y + px / 2 - 11), '%-9s %d px' % (lab, px), font=FK(16), fill=INK)
    d.text((300, y + px / 2 - 10), note, font=FK(14), fill=DIM)
d.text((60, CY + 150),
       '4순위 HUD 아이콘은 10.5~16px 라 선 굵기 하한이 빡빡했지만, 이번엔 28~34px 라 여유가 있습니다.\n'
       '그래도 세부는 과하지 않게 — 같은 가족으로 보이는 게 먼저입니다.',
       font=FK(15), fill=INK, spacing=7)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print('%s  %s  (기존 아이콘 %d/8 삽입)' % (os.path.relpath(OUT, GAME), im.size, ok))
