# -*- coding: utf-8 -*-
"""조준링 안 목표 숫자(#targetN)도 스프라이트로 그린다. (1회성 패치)

현재 숫자만 블록체가 되니 조준링 안 목표 숫자가 혼자 기본 폰트로 남아
같은 화면에서 두 서체가 싸웠다. 46px(4자리는 30px)에서도 모서리 깎임과
베벨이 또렷한 걸 확인하고 같이 넘긴다.

setCur 을 setNum(el, ...) 으로 일반화해 두 곳이 한 구현을 쓰게 한다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS: 두 요소가 같은 규칙을 쓰게 ───────────────────────────────
S.append(("""  #cur.spr{display:flex;align-items:center;justify-content:center;font-size:0;line-height:0}
  #cur.spr>i{display:block;width:var(--dw);height:var(--dh);margin:0 var(--dm);""",
"""  #cur.spr,#targetN.spr{display:flex;align-items:center;justify-content:center;font-size:0;line-height:0}
  #cur.spr>i,#targetN.spr>i{display:block;width:var(--dw);height:var(--dh);margin:0 var(--dm);"""))

S.append(("""  #cur.spr.ontarget{filter:drop-shadow(0 0 30px rgba(255,225,77,.85)) drop-shadow(0 0 60px rgba(255,180,40,.45))}""",
"""  #cur.spr.ontarget{filter:drop-shadow(0 0 30px rgba(255,225,77,.85)) drop-shadow(0 0 60px rgba(255,180,40,.45))}
  #targetN.spr{filter:drop-shadow(0 0 14px rgba(124,246,255,.6))}"""))

# ── 렌더러 일반화 ─────────────────────────────────────────────────
S.append(("""function setCur(v, sizes){
  const el=$('cur'), s=String(v), fs=sizes[Math.min(s.length,sizes.length)-1];""",
"""function setNum(el, v, sizes){
  const s=String(v), fs=sizes[Math.min(s.length,sizes.length)-1];"""))

# ── 호출부 ────────────────────────────────────────────────────────
S.append(("""  $('targetN').textContent=target; fitNum($('targetN'), target, [46,46,38,30]);
  const c=$('cur'); setCur(cur, [126,126,104,80]);""",
"""  setNum($('targetN'), target, [46,46,38,30]);
  const c=$('cur'); setNum(c, cur, [126,126,104,80]);"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:72]))
    else:
        s = s.replace(a, b)

# fitNum 은 이제 쓰이지 않는다 — 남겨두면 다음 사람이 헷갈린다
if 'fitNum(' in s and s.count('fitNum(') == 1:
    s = s.replace("""// 자릿수가 늘어도 숫자 무대·조준링 밖으로 삐져나가지 않게 글자 크기를 맞춘다
function fitNum(el, v, sizes){ const n=String(v).replace('-','').length; el.style.fontSize=(sizes[Math.min(n,sizes.length)-1])+'px'; }
""", '')

if fail:
    for c, a in fail:
        print('no match (%d): %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('targetN sprite wiring: %d patches' % len(S))
