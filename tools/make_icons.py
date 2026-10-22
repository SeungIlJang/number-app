# -*- coding: utf-8 -*-
"""멈춰라 숫자 — 앱 아이콘 / 스플래시 생성기 (PIL only)

  python tools/make_icons.py

안드로이드 mipmap·drawable, capacitor assets 소스(1024), 스토어용 1024 아이콘,
PWA용 SVG를 한 번에 다시 만든다. 색/글자를 바꾸고 다시 돌리면 전부 갱신된다.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES  = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
ASSETS = os.path.join(ROOT, 'assets')
STORE = os.path.abspath(os.path.join(ROOT, '..', 'images', 'number'))

NAVY  = (10, 14, 26)
GLOW  = (20, 28, 54)
CYAN  = (124, 246, 255)
GOLD  = (255, 211, 77)
WHITE = (255, 255, 255)

DIGIT = '7'                 # 아이콘 중앙 숫자
GHOST = ('6', '8')          # 위/아래로 흘러가는 잔상 숫자
FONT_PATH = r'C:\Windows\Fonts\ariblk.ttf'      # Arial Black
if not os.path.exists(FONT_PATH):
    FONT_PATH = r'C:\Windows\Fonts\arialbd.ttf'


def font_for(px):
    return ImageFont.truetype(FONT_PATH, int(px))


def text_layer(S, txt, px, color, alpha, center):
    """투명 레이어에 가운데 정렬 텍스트 한 줄."""
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = font_for(px)
    bb = d.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text((center[0] - w / 2 - bb[0], center[1] - h / 2 - bb[1]), txt,
           font=f, fill=color + (alpha,))
    return lay


def add(base, layer):
    return Image.alpha_composite(base, layer)


def bloom(layer, radius, times=2, gain=1.0):
    """네온 블룸: 흐린 복사본을 여러 번 겹친다."""
    out = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    b = layer.filter(ImageFilter.GaussianBlur(radius))
    if gain != 1.0:
        a = b.split()[3].point(lambda v: min(255, int(v * gain)))
        b.putalpha(a)
    for _ in range(times):
        out = Image.alpha_composite(out, b)
    return out


def radial_background(S):
    base = Image.new('RGBA', (S, S), NAVY + (255,))
    mask = Image.new('L', (S, S), 0)
    d = ImageDraw.Draw(mask)
    cx, cy, R, steps = S / 2, S * 0.44, S * 0.66, 72
    for i in range(steps, 0, -1):
        r = R * i / steps
        a = int(255 * (1 - i / steps) ** 1.7)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    mask = mask.filter(ImageFilter.GaussianBlur(S * 0.03))
    glow = Image.new('RGBA', (S, S), GLOW + (255,))
    return Image.composite(glow, base, mask)


def mark(S, scale=1.0):
    """아이콘 본체(배경 없음): 잔상 숫자 + 조준링 + 중앙 숫자. RGBA 반환."""
    cx, cy = S / 2, S / 2
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))

    # 1) 잔상 숫자 — 릴이 돌다 멈춘 느낌
    gpx = S * 0.34 * scale
    for txt, dy, al in ((GHOST[0], -S * 0.345 * scale, 46), (GHOST[1], S * 0.345 * scale, 46)):
        g = text_layer(S, txt, gpx, CYAN, al, (cx, cy + dy))
        out = add(out, g.filter(ImageFilter.GaussianBlur(S * 0.024)))

    # 2) 조준 링 + 눈금
    ring = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    R = S * 0.345 * scale
    lw = max(2, int(S * 0.022 * scale))
    rd.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD + (255,), width=lw)
    tick = S * 0.072 * scale
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        x0, y0 = cx + math.cos(a) * (R - tick * 0.45), cy + math.sin(a) * (R - tick * 0.45)
        x1, y1 = cx + math.cos(a) * (R + tick * 0.75), cy + math.sin(a) * (R + tick * 0.75)
        rd.line([x0, y0, x1, y1], fill=GOLD + (255,), width=lw)
    out = add(out, bloom(ring, S * 0.022, 2))
    out = add(out, ring)

    # 3) 중앙 숫자 — 멈춘 숫자
    npx = S * 0.52 * scale
    num = text_layer(S, DIGIT, npx, CYAN, 255, (cx, cy - S * 0.012 * scale))
    out = add(out, bloom(num, S * 0.055 * scale, 3, 1.25))
    out = add(out, bloom(num, S * 0.018 * scale, 2))
    out = add(out, num)
    # 숫자 안쪽 하이라이트
    out = add(out, text_layer(S, DIGIT, npx * 0.94, WHITE, 42, (cx, cy - S * 0.021 * scale)))
    return out


def icon_full(S, content=1.0):
    return add(radial_background(S).convert('RGBA'), mark(S, content))


def icon_round(S):
    im = icon_full(S)
    m = Image.new('L', (S * 4, S * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, S * 4 - 1, S * 4 - 1], fill=255)
    im.putalpha(m.resize((S, S), Image.LANCZOS))
    return im


def splash(W, H):
    S = max(W, H)
    bg = radial_background(S).convert('RGBA').resize((S, S), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), NAVY + (255,))
    canvas.paste(bg, ((W - S) // 2, (H - S) // 2))
    m = min(W, H)
    size = int(m * 0.52)
    canvas = Image.alpha_composite(
        canvas, _paste_center(Image.new('RGBA', (W, H), (0, 0, 0, 0)), mark(size), W, H))
    return canvas.convert('RGB')


def _paste_center(canvas, im, W, H):
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2), im)
    return canvas


KR_FONT = r'C:\Windows\Fonts\malgunbd.ttf'


def feature_graphic(W=1024, H=500):
    """구글 플레이 피처 그래픽 — 왼쪽 타이틀, 오른쪽 조준 마크 + 숫자 흐름."""
    S = int(W * 1.1)
    bg = radial_background(S).convert('RGBA')
    canvas = Image.new('RGBA', (W, H), NAVY + (255,))
    canvas.paste(bg, (int(W * 0.46), (H - S) // 2))

    # 오른쪽: 목표를 향해 흘러가는 숫자 수열
    stream = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stream)
    seq = ['3', '6', '9', '12', '15']
    x = W * 0.50
    for i, t in enumerate(seq):
        px = int(H * (0.105 + 0.022 * i))
        f = font_for(px)
        bb = sd.textbbox((0, 0), t, font=f)
        y = int(H * (0.90 - 0.026 * i))
        sd.text((x, y - (bb[3] - bb[1]) / 2 - bb[1]), t, font=f, fill=CYAN + (34 + i * 20,))
        x += (bb[2] - bb[0]) + H * 0.058      # 글자 폭을 재서 띄움 (두 자리 숫자 겹침 방지)
    canvas = add(canvas, stream.filter(ImageFilter.GaussianBlur(H * 0.006)))

    # 오른쪽 끝: 조준링에 멈춘 숫자
    m = int(H * 0.70)
    mk = mark(m)
    canvas.paste(mk, (int(W * 0.785 - m / 2), int(H * 0.40 - m / 2)), mk)

    # 왼쪽: 타이틀 + 한 줄 카피
    d = ImageDraw.Draw(canvas)
    tf = ImageFont.truetype(KR_FONT, int(H * 0.168))
    sf = ImageFont.truetype(KR_FONT, int(H * 0.064))
    tx, ty = int(W * 0.065), int(H * 0.33)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((tx, ty), '멈춰라 숫자', font=tf, fill=CYAN + (170,), anchor='ls')
    canvas = add(canvas, glow.filter(ImageFilter.GaussianBlur(H * 0.022)))
    d = ImageDraw.Draw(canvas)
    d.text((tx, ty), '멈춰라 숫자', font=tf, fill=(255, 255, 255, 255), anchor='ls')
    d.text((tx, int(H * 0.47)), '규칙을 읽고  목표에서  STOP!', font=sf, fill=(150, 170, 200, 255), anchor='ls')
    d.text((tx, int(H * 0.62)), '🔗 체인 목표 · 🏅 랭크 승급 · 🌐 전세계 랭킹'.replace('🔗 ', '').replace('🏅 ', '').replace('🌐 ', ''),
           font=sf, fill=GOLD + (230,), anchor='ls')
    return canvas.convert('RGB')


def save(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    print('  ', os.path.relpath(path, ROOT), im.size)


MIPMAP = {'ldpi': (36, 81), 'mdpi': (48, 108), 'hdpi': (72, 162),
          'xhdpi': (96, 216), 'xxhdpi': (144, 324), 'xxxhdpi': (192, 432)}
SPLASH_PORT = {'mdpi': (320, 480), 'hdpi': (480, 800), 'xhdpi': (720, 1280),
               'xxhdpi': (960, 1600), 'xxxhdpi': (1280, 1920)}
SPLASH_LAND = {'mdpi': (480, 320), 'hdpi': (800, 480), 'xhdpi': (1280, 720),
               'xxhdpi': (1600, 960), 'xxxhdpi': (1920, 1280)}

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="bg" cx="50%" cy="44%" r="66%">
      <stop offset="0%" stop-color="#141c36"/><stop offset="100%" stop-color="#0a0e1a"/>
    </radialGradient>
    <filter id="gl" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="14" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="gs" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>
  <rect width="512" height="512" rx="96" fill="url(#bg)"/>
  <g font-family="Arial Black, Arial, sans-serif" font-weight="900" text-anchor="middle">
    <text x="256" y="104" font-size="118" fill="#7cf6ff" opacity=".26" filter="url(#gs)">6</text>
    <text x="256" y="452" font-size="118" fill="#7cf6ff" opacity=".26" filter="url(#gs)">8</text>
    <g filter="url(#gl)">
      <circle cx="256" cy="256" r="177" fill="none" stroke="#ffd34d" stroke-width="11"/>
      <path d="M256 140 V 215 M256 297 V 372 M140 256 H 215 M297 256 H 372"
            stroke="#ffd34d" stroke-width="11" stroke-linecap="round"/>
      <text x="256" y="312" font-size="154" fill="#7cf6ff">7</text>
    </g>
  </g>
</svg>
'''


def main():
    print('안드로이드 런처 아이콘')
    for dpi, (small, big) in MIPMAP.items():
        d = os.path.join(RES, 'mipmap-' + dpi)
        save(icon_full(small), os.path.join(d, 'ic_launcher.png'))
        save(icon_round(small), os.path.join(d, 'ic_launcher_round.png'))
        # 적응형 아이콘: 전경은 가운데 66% 안전영역 안에 들어오게 축소
        save(mark(big, 0.62), os.path.join(d, 'ic_launcher_foreground.png'))
        save(radial_background(big).convert('RGBA'), os.path.join(d, 'ic_launcher_background.png'))

    print('스플래시')
    save(splash(480, 320), os.path.join(RES, 'drawable', 'splash.png'))
    for dpi, (w, h) in SPLASH_PORT.items():
        save(splash(w, h), os.path.join(RES, 'drawable-port-' + dpi, 'splash.png'))
    for dpi, (w, h) in SPLASH_LAND.items():
        save(splash(w, h), os.path.join(RES, 'drawable-land-' + dpi, 'splash.png'))

    print('capacitor assets 소스 + 스토어')
    save(icon_full(1024), os.path.join(ASSETS, 'icon-only.png'))
    save(mark(1024, 0.62), os.path.join(ASSETS, 'icon-foreground.png'))
    save(radial_background(1024).convert('RGBA'), os.path.join(ASSETS, 'icon-background.png'))
    save(icon_full(1024), os.path.join(STORE, 'icon_1024.png'))
    save(splash(1080, 1920), os.path.join(STORE, 'splash_portrait_1080x1920.png'))
    save(feature_graphic(), os.path.join(STORE, 'feature_graphic_1024x500.png'))

    with open(os.path.join(ROOT, 'icon-512.svg'), 'w', encoding='utf-8') as f:
        f.write(SVG)
    print('   icon-512.svg (PWA)')


if __name__ == '__main__':
    main()
