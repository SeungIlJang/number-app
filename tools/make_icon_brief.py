# -*- coding: utf-8 -*-
"""4순위(HUD 아이콘) 발주서용 규격 참고도를 그린다.

  python tools/make_icon_brief.py

아이콘 세트에서 실제로 망하는 건 두 가지다.
 1) 96px 캔버스가 화면에서 15px 로 줄어든다(16%). 가는 선은 그때 사라진다.
 2) 모양이 제각각이면 같은 크기로 안 보인다(둥근 건 작아 보이고 각진 건 커 보인다).
말로 적으면 안 지켜지니 그림으로 못 박는다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUT = os.path.join(GAME, 'images', 'number', '_brief', 'icon_metrics.png')

CV, SAFE = 96, 80          # 캔버스 / 안전영역
BG, INK, LINE, DIM, GOLD, MINT, RED = (10, 14, 26), (235, 250, 255), (124, 246, 255), (120, 140, 170), (255, 211, 77), (92, 255, 176), (255, 90, 110)


def font(path, size):
    for p in (path, 'C:/Windows/Fonts/' + path):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


FK = lambda s: font('malgun.ttf', s)


def dashed(d, x0, y0, x1, y1, col, dash=8, gap=6, w=2):
    if y0 == y1:
        x = x0
        while x < x1:
            d.line([x, y0, min(x + dash, x1), y0], fill=col, width=w); x += dash + gap
    else:
        y = y0
        while y < y1:
            d.line([x0, y, x0, min(y + dash, y1)], fill=col, width=w); y += dash + gap


def dashed_rect(d, box, col, **kw):
    x0, y0, x1, y1 = box
    dashed(d, x0, y0, x1, y0, col, **kw); dashed(d, x0, y1, x1, y1, col, **kw)
    dashed(d, x0, y0, x0, y1, col, **kw); dashed(d, x1, y0, x1, y1, col, **kw)


def sample(size, thick):
    """테스트 아이콘 — 트로피 비슷한 실루엣. thick=선 굵기(96px 기준)."""
    k = size / CV
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = max(1, int(round(thick * k)))
    s = lambda v: v * k
    # 컵
    d.ellipse([s(26), s(16), s(70), s(56)], outline=GOLD, width=w)
    # 손잡이 둘
    d.arc([s(12), s(22), s(32), s(46)], 90, 270, fill=GOLD, width=w)
    d.arc([s(64), s(22), s(84), s(46)], 270, 90, fill=GOLD, width=w)
    # 기둥 + 받침
    d.line([s(48), s(54), s(48), s(68)], fill=GOLD, width=w)
    d.line([s(32), s(72), s(64), s(72)], fill=GOLD, width=max(1, int(round(thick * 1.2 * k))))
    return im


W, H = 1180, 800
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)

d.text((34, 26), '멈춰라 숫자 — HUD 아이콘 규격 (96 x 96, 투명 PNG)', font=FK(27), fill=INK)
d.text((34, 64), '게임에서 이 아이콘들은 10.5 ~ 16 px 로 표시됩니다. 96px 캔버스가 화면에서 16% 로 줄어든다는 뜻입니다.',
       font=FK(15), fill=DIM)

# ── 패널 A : 캔버스와 안전영역 ────────────────────────────────────
AX, AY, K = 70, 140, 3.0
aw = int(CV * K)
d.text((AX, AY - 30), 'A. 캔버스와 안전영역', font=FK(17), fill=GOLD)
d.rectangle([AX, AY, AX + aw, AY + aw], fill=(0, 0, 0), outline=LINE, width=2)
pad = (CV - SAFE) / 2 * K
dashed_rect(d, (AX + pad, AY + pad, AX + aw - pad, AY + aw - pad), MINT, dash=7, gap=5, w=2)
im.paste(sample(int(SAFE * K), 8), (int(AX + pad), int(AY + pad)), sample(int(SAFE * K), 8))
d.text((AX + aw + 18, AY + pad - 12), '안전영역 80 x 80', font=FK(15), fill=MINT)
d.text((AX + aw + 18, AY + pad + 12), '그림은 여기 안에', font=FK(13), fill=DIM)
d.text((AX, AY + aw + 14), '캔버스 96 x 96  ·  사방 여백 8 px', font=FK(15), fill=DIM)
d.text((AX, AY + aw + 40),
       '· 둥근 것(코인)은 지름 76 까지 키워도 됩니다\n'
       '  그래야 각진 것과 같은 크기로 보입니다\n'
       '· 가로로 긴 것(책·카트)은 폭 80 을,\n'
       '  세로로 긴 것(트로피)은 높이 80 을 채우세요\n'
       '· 8장이 한 줄에 나란히 섭니다 - "같은 무게"로\n'
       '  보이는 게 수치보다 중요합니다',
       font=FK(14), fill=DIM, spacing=5)

# ── 패널 B : 선 굵기 하한 ─────────────────────────────────────────
BX, BY = 560, 140
d.text((BX, BY - 30), 'B. 선 굵기 하한 - 이게 이번 발주의 핵심', font=FK(17), fill=GOLD)
rows = [(8, '선 굵기 8 px', MINT, '화면에서 1.25 px - 살아남습니다'),
        (3, '선 굵기 3 px', RED, '화면에서 0.47 px - 사라집니다')]
for i, (th, lab, col, note) in enumerate(rows):
    y = BY + i * 150
    im.paste(sample(96, th), (BX, y), sample(96, th))
    d.rectangle([BX, y, BX + 96, y + 96], outline=(44, 66, 96), width=1)
    d.text((BX + 112, y + 6), lab, font=FK(16), fill=col)
    d.text((BX + 112, y + 32), note, font=FK(13), fill=DIM)
    # 실제 표시 크기
    for j, px in enumerate((24, 16)):
        x = BX + 112 + j * 150
        s = sample(px, th)
        im.paste(s, (x, y + 64), s)
        d.rectangle([x - 1, y + 63, x + px, y + 64 + px], outline=(44, 66, 96), width=1)
        d.text((x + px + 8, y + 64), str(px) + 'px', font=FK(12), fill=DIM)
d.text((BX, BY + 330),
       '화면 표시 크기는 10.5 ~ 16 px 입니다(고밀도 화면에서 실제 32~48 px).\n'
       '96px 캔버스에서 8 px 보다 가는 선·틈은 그 크기에서 뭉개져 사라집니다.\n'
       '세부를 줄이고 실루엣을 굵고 단순하게 가세요 - 작아도 뭔지 알아보는 게 전부입니다.',
       font=FK(15), fill=INK, spacing=7)

# ── 패널 C : 납품 전 꼭 볼 것 ─────────────────────────────────────
CY = 632
d.text((70, CY - 26), 'C. 납품 전에 16 px 로 줄여서 직접 보세요', font=FK(17), fill=GOLD)
d.text((70, CY + 6),
       '8장을 96px 로 나란히 붙인 미리보기와, 똑같은 8장을 16px 로 줄여 붙인 미리보기를 각각 주세요.\n'
       '16px 줄에서 무엇인지 못 알아보는 아이콘이 있으면 그 장은 다시 그려야 합니다.\n'
       '전부 full-color 입니다 - 3순위 숫자처럼 흑백으로 만들지 마세요. 색은 코드가 입히지 않습니다.',
       font=FK(16), fill=INK, spacing=8)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print('%s  %s' % (os.path.relpath(OUT, GAME), im.size))
