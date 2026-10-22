# -*- coding: utf-8 -*-
"""neon-v2 납품 아트를 각 사용처 규격으로 전개한다.

  python tools/apply_art.py

소스: D:/AI/workspace/game/images/number/neon-v2/  (1024·256·128 원본)
전개처
  1) number-app/assets/            capacitor assets 소스 3종
  2) android/.../res/mipmap-*      런처 아이콘 24장
  3) android/.../res/drawable*     스플래시 11장 (cover 크롭, 비율 왜곡 없음)
  4) games/img/number/ui/          게임이 불러 쓰는 웹용 축소본(랭크 128·부스터 96)
     number-app/www/img/number/ui/ 오프라인 폴백용 동일 사본
  5) images/number/neon-v2/        타이틀 얹은 피처 그래픽

원본은 건드리지 않는다. 아트를 교체하면 이 스크립트만 다시 돌리면 된다.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # number-app
GAME   = os.path.abspath(os.path.join(ROOT, '..'))                        # workspace/game
SRC    = os.path.join(GAME, 'images', 'number', 'neon-v2')
RES    = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
ASSETS = os.path.join(ROOT, 'assets')
WEB_A  = os.path.join(GAME, 'games', 'img', 'number', 'ui')
WEB_B  = os.path.join(ROOT, 'www', 'img', 'number', 'ui')

KR_FONT = r'C:\Windows\Fonts\malgunbd.ttf'
CYAN, GOLD = (124, 246, 255), (255, 211, 77)

MIPMAP = {'ldpi': (36, 81), 'mdpi': (48, 108), 'hdpi': (72, 162),
          'xhdpi': (96, 216), 'xxhdpi': (144, 324), 'xxxhdpi': (192, 432)}
SPLASH_PORT = {'mdpi': (320, 480), 'hdpi': (480, 800), 'xhdpi': (720, 1280),
               'xxhdpi': (960, 1600), 'xxxhdpi': (1280, 1920)}
SPLASH_LAND = {'mdpi': (480, 320), 'hdpi': (800, 480), 'xhdpi': (1280, 720),
               'xxhdpi': (1600, 960), 'xxxhdpi': (1920, 1280)}
RANKS = ['rank_1_bronze', 'rank_2_silver', 'rank_3_gold', 'rank_4_platinum',
         'rank_5_diamond', 'rank_6_master', 'rank_7_grandmaster']
BOOSTS = ['boost_life', 'boost_slow', 'boost_coin2', 'boost_score2']


def load(name):
    return Image.open(os.path.join(SRC, name + '.png'))


def save(im, path, **kw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, optimize=True, **kw)
    rel = os.path.relpath(path, GAME)
    print('   %-62s %-11s %4dKB' % (rel, im.size, os.path.getsize(path) // 1024))


def fit(im, size):
    return im.resize(size, Image.LANCZOS)


def cover(im, W, H):
    """비율 유지하며 가득 채우고 가운데를 잘라낸다(찌그러짐 방지)."""
    s = max(W / im.width, H / im.height)
    r = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    L, T = (r.width - W) // 2, (r.height - H) // 2
    return r.crop((L, T, L + W, T + H))


def circle(im):
    S = im.width
    m = Image.new('L', (S * 4, S * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, S * 4 - 1, S * 4 - 1], fill=255)
    out = im.convert('RGBA').copy()
    out.putalpha(m.resize((S, S), Image.LANCZOS))
    return out


def titled_feature():
    base = load('feature_graphic_1024x500').convert('RGBA')
    W, H = base.size
    tx = int(W * 0.055)
    maxw = int(W * 0.415) - tx          # 아트가 시작되기 전까지의 빈 폭
    probe = ImageDraw.Draw(base)

    def fitted(txt, px):               # 빈 폭을 넘지 않을 때까지 글자 크기를 줄인다
        while px > 10:
            f = ImageFont.truetype(KR_FONT, int(px))
            bb = probe.textbbox((0, 0), txt, font=f)
            if bb[2] - bb[0] <= maxw:
                return f
            px -= 1
        return ImageFont.truetype(KR_FONT, 10)

    tf = fitted('멈춰라 숫자', H * 0.158)
    sf = fitted('규칙을 읽고  목표에서  STOP!', H * 0.062)
    gf = fitted('체인 목표 · 랭크 승급 · 전세계 랭킹', H * 0.062)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((tx, int(H * 0.40)), '멈춰라 숫자', font=tf,
                              fill=CYAN + (165,), anchor='ls')
    out = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(H * 0.02)))
    d = ImageDraw.Draw(out)
    d.text((tx, int(H * 0.40)), '멈춰라 숫자', font=tf, fill=(255, 255, 255, 255), anchor='ls')
    d.text((tx, int(H * 0.54)), '규칙을 읽고  목표에서  STOP!', font=sf,
           fill=(152, 172, 202, 255), anchor='ls')
    d.text((tx, int(H * 0.69)), '체인 목표 · 랭크 승급 · 전세계 랭킹', font=gf,
           fill=GOLD + (235,), anchor='ls')
    return out.convert('RGB')


def main():
    icon, fg, bg = load('icon_1024').convert('RGB'), load('icon_foreground').convert('RGBA'), load('icon_background').convert('RGB')

    print('1) capacitor assets 소스')
    save(fit(icon, (1024, 1024)), os.path.join(ASSETS, 'icon-only.png'))
    save(fit(fg, (1024, 1024)), os.path.join(ASSETS, 'icon-foreground.png'))
    save(fit(bg, (1024, 1024)), os.path.join(ASSETS, 'icon-background.png'))

    print('2) 런처 아이콘')
    for dpi, (small, big) in MIPMAP.items():
        d = os.path.join(RES, 'mipmap-' + dpi)
        save(fit(icon, (small, small)).convert('RGBA'), os.path.join(d, 'ic_launcher.png'))
        save(circle(fit(icon, (small, small))), os.path.join(d, 'ic_launcher_round.png'))
        save(fit(fg, (big, big)), os.path.join(d, 'ic_launcher_foreground.png'))
        save(fit(bg, (big, big)).convert('RGBA'), os.path.join(d, 'ic_launcher_background.png'))

    print('3) 스플래시')
    sp, sl = load('splash_portrait_1080x1920').convert('RGB'), load('splash_land_1920x1080').convert('RGB')
    save(cover(sl, 480, 320), os.path.join(RES, 'drawable', 'splash.png'))
    for dpi, (w, h) in SPLASH_PORT.items():
        save(cover(sp, w, h), os.path.join(RES, 'drawable-port-' + dpi, 'splash.png'))
    for dpi, (w, h) in SPLASH_LAND.items():
        save(cover(sl, w, h), os.path.join(RES, 'drawable-land-' + dpi, 'splash.png'))

    print('4) 게임 UI용 축소본 (랭크 128 / 부스터 96)')
    for folder in (WEB_A, WEB_B):
        for n in RANKS:
            save(fit(load(n).convert('RGBA'), (128, 128)), os.path.join(folder, n + '.png'))
        for n in BOOSTS:
            save(fit(load(n).convert('RGBA'), (96, 96)), os.path.join(folder, n + '.png'))

    print('5) 타이틀 얹은 피처 그래픽')
    save(titled_feature(), os.path.join(SRC, 'feature_graphic_1024x500_titled.png'))


if __name__ == '__main__':
    main()
