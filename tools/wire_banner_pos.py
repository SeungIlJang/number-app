# -*- coding: utf-8 -*-
"""라운드 배너가 목표 숫자를 가리던 것을 고친다. (1회성 패치)

문제: #banner 가 top:24% 고정이라 조준링 한가운데에 선다.
  360x640 기준 배너 161~182 / 조준링 132~264 — 조준링 안의 목표 숫자를 덮는다.
  배너는 라운드 시작에 0.9초 뜨는데, 그때가 바로 목표를 읽어야 하는 순간이다.
  (불투명 구간은 약 160~740ms, 숫자는 450ms 부터 움직이기 시작한다.)

플레이 중 빈 공간을 전부 재봤다. 체인 라운드(가장 빽빽한 경우) 360x560 기준:
  hud 12~32 · chase 38~54 · target 74~94 · targetWrap 90~222 · chainTag 214~238
  curWrap 244~430 · seq 430~458 · hint 466~486
  → 빈 띠는 54~74 (20px) 와 화면 맨 아래뿐이다.
  맨 아래는 판정 리본(403~521)이 쓰고 있고 라운드 안내로는 너무 구석이다.

그래서 기록줄과 목표 안내문 사이 20px 띠로 옮기고, 거기 들어가게 글자를
26 -> 22px 로 줄였다(높이 21 -> 18px). 화면 높이마다 플레이 영역 위치가
달라지므로 좌표는 그때그때 잰다 — 고정 %로는 어느 한 해상도에서 반드시 깨진다.

선택형 라운드처럼 조준링이 숨는 화면에서는 가릴 것이 없으므로 기존 자리를 쓴다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

S.append(("""  #banner{position:fixed;top:24%;left:0;right:0;text-align:center;font-size:26px;font-weight:900;z-index:6;pointer-events:none;opacity:0}""",
          """  #banner{position:fixed;top:24%;left:0;right:0;text-align:center;font-size:22px;font-weight:900;z-index:6;pointer-events:none;opacity:0;padding:0 12px}"""))

S.append(("""function banner(txt,col){ const b=$('banner'); b.innerHTML=txt;""",
"""// 기본 자리(top:24%)는 조준링 한가운데라 목표 숫자를 덮는다.
// 조준링이 보일 때만 기록줄과 목표 안내문 사이 빈 띠로 옮긴다.
// 화면 높이마다 플레이 영역이 오르내리므로 고정 %가 아니라 그때그때 잰다.
function bannerTop(b){
  const ch=$('chase'), tg=$('target');
  if(!ch||!tg) return '';
  const cr=ch.getBoundingClientRect(), tr=tg.getBoundingClientRect();
  if(!(tr.height>0)) return '';                 // 선택형 등 조준링이 숨은 화면
  const h=b.getBoundingClientRect().height;
  return Math.round(Math.max(cr.bottom+2, (cr.bottom+tr.top)/2 - h/2))+'px';
}
function banner(txt,col){ const b=$('banner'); b.innerHTML=txt;"""))

S.append(("""b.style.color=col||'#fff'; b.classList.remove('show'); void b.offsetWidth; b.classList.add('show'); }""",
          """b.style.color=col||'#fff'; b.style.top=''; b.style.top=bannerTop(b);
  b.classList.remove('show'); void b.offsetWidth; b.classList.add('show'); }"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:72]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('matched %d, expected 1: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('banner position: %d patches' % len(S))
