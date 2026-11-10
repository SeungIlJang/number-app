# -*- coding: utf-8 -*-
"""홈 화면·파비콘용 아이콘을 표시 크기에 맞게 다시 뽑는다.

  python tools/apply_icon.py

icon_512.png 는 480KB인데 실제로는 72px(고밀도에서 216px)로 쓰인다.
OTA로 띄운 앱은 이제 이 파일을 라이브 사이트에서 받으므로, 실행할 때마다
480KB를 내려받게 된다. 256px로 줄이고 팔레트로 양자화하면 14KB가 된다.
"""
import os
from PIL import Image, ImageChops, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUTS = [os.path.join(GAME, 'games', 'img', 'number', 'ui'),
        os.path.join(ROOT, 'www', 'img', 'number', 'ui')]
SRC = os.path.join(OUTS[0], 'icon_512.png')
N = 256


def main():
    src = Image.open(SRC).convert('RGBA')
    small = src.resize((N, N), Image.LANCZOS)
    out = small.quantize(colors=256, method=Image.FASTOCTREE)

    # 양자화로 색이 뭉개지지 않았는지 — 줄이기만 한 것과 비교
    diff = ImageChops.difference(out.convert('RGB'), small.convert('RGB'))
    st = ImageStat.Stat(diff)
    rms = (sum(v ** 2 for v in st.mean) / 3) ** .5

    for d in OUTS:
        out.save(os.path.join(d, 'icon_256.png'), optimize=True)

    before, after = os.path.getsize(SRC), os.path.getsize(os.path.join(OUTS[0], 'icon_256.png'))
    print('icon_512.png %dKB (512) -> icon_256.png %dKB (256)  %.0f%% 감소'
          % (before // 1024, after // 1024, 100 * (1 - after / before)))
    print('양자화 오차: 평균 %.2f / 최대 %d  (8 이하면 눈에 안 보임)' % (rms, max(st.extrema[i][1] for i in range(3))))
    for d in OUTS:
        print('  ', os.path.relpath(os.path.join(d, 'icon_256.png'), GAME))


if __name__ == '__main__':
    main()
