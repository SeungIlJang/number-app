# -*- coding: utf-8 -*-
"""렌더러 테스트용 임시 숫자판을 만든다. (아트가 오면 버릴 것)

  python tools/make_digit_placeholder.py

Codex가 납품할 형식과 똑같이 만든다 — 224x320, 검정 배경, 흰 숫자, 불투명 PNG.
덕분에 apply_digits.py(실제 변환·검수 파이프라인)를 지금 그대로 돌려볼 수 있다.
그림 품질이 목적이 아니라 '렌더러가 제대로 도는지' 확인이 목적이다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

GAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(GAME, 'images', 'number', '_placeholder')

CW, CH, INK_H, CY, CX = 224, 320, 256, 160, 112
TOP, BOT = 255, 168        # 베벨 흉내 — 위가 밝고 아래가 어둡게


def font(size):
    for p in ('C:/Windows/Fonts/ariblk.ttf', 'C:/Windows/Fonts/arialbd.ttf', 'arial.ttf'):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def main():
    os.makedirs(OUT, exist_ok=True)
    # 세로 그라디언트 (잉크 영역에만 곱해진다)
    grad = Image.new('L', (1, CH))
    for y in range(CH):
        t = min(1.0, max(0.0, (y - (CY - INK_H / 2)) / INK_H))
        grad.putpixel((0, y), int(round(TOP + (BOT - TOP) * t)))
    grad = grad.resize((CW, CH))

    for n in range(10):
        ch = str(n)
        # 1) 넉넉한 캔버스에 크게 그린 뒤
        big = Image.new('L', (CW * 3, CH * 3), 0)
        f = font(int(INK_H * 1.36 * 2))
        ImageDraw.Draw(big).text((big.width / 2, big.height / 2), ch, font=f, fill=255, anchor='mm')
        bb = big.getbbox()
        # 2) 잉크 높이가 정확히 256이 되게 정규화하고 중심을 (112,160)에 둔다
        k = INK_H / (bb[3] - bb[1])
        # Arial Black 은 게임 폰트보다 넓다 — 규격(잉크 폭 192) 안으로 눌러 넣는다.
        # 임시 숫자판이라 가로를 눌러도 상관없고, 오히려 system-ui 900 비율에 가까워진다.
        w = min(188, max(1, int(round((bb[2] - bb[0]) * k))))
        crop = big.crop(bb).resize((w, INK_H), Image.LANCZOS)
        mask = Image.new('L', (CW, CH), 0)
        mask.paste(crop, (CX - crop.width // 2, CY - INK_H // 2))
        # 3) 베벨 흉내 그라디언트를 입히고 검정 배경 위에 얹는다
        shaded = Image.composite(grad, Image.new('L', (CW, CH), 0), mask.point(lambda v: 255 if v > 127 else 0))
        soft = Image.composite(shaded, Image.new('L', (CW, CH), 0), mask)
        Image.merge('RGB', (soft, soft, soft)).save(os.path.join(OUT, 'digit_%d.png' % n))

    print('임시 숫자판 10장 ->', os.path.relpath(OUT, GAME))


if __name__ == '__main__':
    main()
