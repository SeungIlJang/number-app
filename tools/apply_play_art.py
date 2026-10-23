# -*- coding: utf-8 -*-
"""neon-v3 플레이 화면 아트를 웹 배포용으로 전개한다.

  python tools/apply_play_art.py

원본: images/number/neon-v3/   (배경 1080x1920 / 링 512 / 무대 768x448)
전개: games/img/number/play/           배포(깃헙 페이지)
      number-app/www/img/number/play/  오프라인 폴백

부드러운 네온 그라데이션이라 255색 팔레트로 떨어뜨려도 오차가 0.5% 미만이다.
배경은 어두운 글로우 위주라 해상도를 조금 낮춰도 눈에 띄지 않는다.
원본은 건드리지 않는다.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # number-app
GAME = os.path.abspath(os.path.join(ROOT, '..'))                       # workspace/game
SRC  = os.path.join(GAME, 'images', 'number', 'neon-v3')
OUTS = [os.path.join(GAME, 'games', 'img', 'number', 'play'),
        os.path.join(ROOT, 'www', 'img', 'number', 'play')]

# (파일, 목표 가로폭 또는 None=원본 그대로 복사)
# 배경 원본은 이미 잘 압축된 팔레트 PNG다. 다시 인코딩하면 오히려 커지므로 손대지 않는다.
# 알파가 있는 링·무대만 표시 크기에 맞춰 줄이고 255색으로 떨군다(오차 0.5% 미만).
PLAN = [
    ('play_bg_normal',      None),
    ('play_bg_golden',      None),
    ('play_bg_roll',        None),
    ('target_ring',          384),
    ('target_ring_locked',   384),
    ('number_stage',         640),
]


def main():
    before = after = 0
    print('  파일                      원본  ->  최적화')
    for name, width in PLAN:
        p = os.path.join(SRC, name + '.png')
        before += os.path.getsize(p)
        if width is None:
            data = open(p, 'rb').read()
            for d in OUTS:
                os.makedirs(d, exist_ok=True)
                open(os.path.join(d, name + '.png'), 'wb').write(data)
            size = Image.open(p).size
        else:
            src = Image.open(p).convert('RGBA')
            im = src.resize((width, int(round(src.height * width / src.width))), Image.LANCZOS)
            im = im.quantize(colors=255, method=Image.FASTOCTREE).convert('RGBA')
            for d in OUTS:
                os.makedirs(d, exist_ok=True)
                im.save(os.path.join(d, name + '.png'), optimize=True)
            size = im.size
        sz = os.path.getsize(os.path.join(OUTS[0], name + '.png'))
        after += sz
        print('  %-22s %4dKB -> %4dKB  %s%s' %
              (name, os.path.getsize(p) // 1024, sz // 1024, size,
               '  (원본 그대로)' if width is None else ''))
    print('\n합계 %dKB -> %dKB (%.0f%% 감소)' %
          (before // 1024, after // 1024, 100 * (1 - after / before)))
    for d in OUTS:
        print('  ', os.path.relpath(d, GAME))


if __name__ == '__main__':
    main()
