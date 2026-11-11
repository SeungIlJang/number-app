# -*- coding: utf-8 -*-
"""콤보 배수 표시를 화면 가운데 팝업에서 HUD 안으로 옮긴다. (1회성 패치)

문제: #mult 가 top:15% 에 고정된 큰 팝업이라 목표 안내문과 조준링을 덮었다.
  360x640 기준 배수 96~155 / 안내문 116~136 / 조준링 132~264 — 둘 다 겹친다.
  HUD 아래 빈 띠(55~116)로 옮겨봤지만 360x560 처럼 짧은 화면에서는 플레이 영역이
  위로 올라와 다시 겹친다. 고정 좌표로는 모든 화면을 만족시킬 수 없다.

고침: 배수를 HUD 가운데 칸(콤보 자리)에 상시 표시한다.
  HUD 는 상단에 고정된 띠라 어떤 화면 크기에서도 플레이 영역과 겹치지 않는다.
  덤으로, 올라가는 순간 1초만 보이던 배수를 판 내내 확인할 수 있게 된다 —
  점수에 직접 곱해지는 값인데 그동안 볼 방법이 없었다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #combo{color:#ffd34d;font-weight:900}
  #mult{position:fixed;top:15%;left:50%;transform:translateX(-50%) scale(.7);font-size:44px;font-weight:900;color:#ffd34d;text-shadow:0 0 22px rgba(255,211,77,.8);z-index:6;pointer-events:none;opacity:0;transition:opacity .18s,transform .18s}
  #mult.show{opacity:1;transform:translateX(-50%) scale(1)}
  #mult.bump{animation:mbump .28s ease-out}""",
"""  /* 콤보와 배수를 HUD 가운데 한 자리에 모은다.
     배수는 예전에 화면 가운데 큰 팝업(top:15%)이었는데 목표 안내문과 조준링을
     덮었다. HUD 는 상단 고정 띠라 어떤 화면 높이에서도 플레이 영역과 안 겹친다. */
  #combo{color:#ffd34d;font-weight:900;white-space:nowrap}
  #combo .mx{color:#ffe14d;text-shadow:0 0 10px rgba(255,211,77,.85);margin-left:4px}
  #combo.bump{animation:cbump .28s ease-out}"""))

S.append(("""  @keyframes mbump{0%{transform:translateX(-50%) scale(1.5)}60%{transform:translateX(-50%) scale(.9)}100%{transform:translateX(-50%) scale(1)}}""",
          """  @keyframes cbump{0%{transform:scale(1.45)}60%{transform:scale(.94)}100%{transform:scale(1)}}"""))

S.append(("""body.menu #hud,body.menu #wrap,body.menu #chase,body.menu #mult,body.menu #banner{visibility:hidden}""",
          """body.menu #hud,body.menu #wrap,body.menu #chase,body.menu #banner{visibility:hidden}"""))

# ── 마크업 ────────────────────────────────────────────────────────
S.append(("""<div id="mult"></div>\n""", ""))

# ── 렌더러 ────────────────────────────────────────────────────────
S.append(("""function showMult(){ const m=$('mult'); if(mult>1){ m.textContent='×'+mult; m.classList.add('show'); m.classList.remove('bump'); void m.offsetWidth; m.classList.add('bump'); } else { m.classList.remove('show'); } }""",
"""// HUD 가운데 칸 — 콤보와 배수를 함께 그린다.
// hits<2 라 콤보가 비어 있어도 배수는 보여야 한다(PERFECT 한 번이면 바로 ×2 다).
function renderCombo(){
  const el=$('combo'); if(!el) return;
  const c = hits>=2 ? (uic('combo','\\u{1F525}',15)+' '+hits+' 연속') : '';
  const m = mult>1 ? '<b class="mx">×'+mult+'</b>' : '';
  el.innerHTML = c + m;
}
let multShown=1;
function showMult(){
  renderCombo();
  if(mult===multShown) return;            // 매 타격마다 부르므로 값이 바뀔 때만 튕긴다
  multShown=mult;
  if(mult>1){ const el=$('combo'); el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); }
}"""))

# ── 기존 콤보 렌더 3곳을 한 구현으로 ──────────────────────────────
S.append(("""$('combo').innerHTML=hits>=2?(uic('combo','\U0001F525',15)+' '+hits+' 연속'):''""",
          """renderCombo()""", 3))

fail = []
for rule in S:
    a, b = rule[0], rule[1]
    want = rule[2] if len(rule) > 2 else 1
    c = s.count(a)
    if c != want:
        fail.append((c, want, a[:70]))
    else:
        s = s.replace(a, b)
if fail:
    for c, w, a in fail:
        print('matched %d, expected %d: %s' % (c, w, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('multiplier moved into HUD: %d rules' % len(S))
