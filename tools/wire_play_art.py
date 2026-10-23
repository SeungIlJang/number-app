# -*- coding: utf-8 -*-
"""games/number.html 에 플레이 화면 아트(배경·조준링·숫자 무대)를 연결한다 (1회성 패치)."""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  .art{vertical-align:middle;object-fit:contain;display:inline-block;flex:0 0 auto}""",
"""  .art{vertical-align:middle;object-fit:contain;display:inline-block;flex:0 0 auto}
  /* 플레이 배경 — 두 겹을 교차 페이드해서 라운드마다 분위기를 바꾼다 */
  .pbg{position:fixed;inset:0;z-index:0;background-size:cover;background-position:center;
       opacity:0;transition:opacity .45s ease-out;pointer-events:none}
  body.menu .pbg{visibility:hidden}
  /* 목표 조준링 — 가운데가 비어 있어 목표 숫자가 그 안에 들어간다 */
  #targetWrap{width:132px;height:132px;display:flex;align-items:center;justify-content:center;
    background-size:contain;background-repeat:no-repeat;background-position:center;margin:-6px 0 -8px}
  /* 숫자 무대 — 현재 숫자가 이 패널 위에 얹힌다 */
  #curWrap{width:min(88vw,330px);height:186px;display:flex;align-items:center;justify-content:center;
    background-size:contain;background-repeat:no-repeat;background-position:center;margin:6px 0 0}
  #curWrap #cur{margin:0}
  #wrap.choice #targetWrap,#wrap.choice #curWrap{display:none}"""))

# ── HTML: 배경 두 겹 + 목표/숫자 래퍼 ─────────────────────────────
S.append(("""<div id="vig"></div>""",
"""<div id="pbgA" class="pbg"></div><div id="pbgB" class="pbg"></div>
<div id="vig"></div>"""))

S.append(("""  <div id="targetN">–</div>
  <div id="chainTag"></div>
  <div id="cur">–</div>""",
"""  <div id="targetWrap"><div id="targetN">–</div></div>
  <div id="chainTag"></div>
  <div id="curWrap"><div id="cur">–</div></div>"""))

# ── 엔진 ──────────────────────────────────────────────────────────
S.append(("""function renderMute(){""",
"""// ── 플레이 화면 아트 ──────────────────────────────────────────────
// 못 불러와도(구버전 APK·오프라인) 배경이 비어 보일 뿐 진행에는 지장이 없다.
const PLAY_DIR='img/number/play/';
let bgKind='', bgTop=false, ringLocked=null;
function setBG(kind){
  if(kind===bgKind) return; bgKind=kind;
  const show=$(bgTop?'pbgA':'pbgB'), hide=$(bgTop?'pbgB':'pbgA');
  if(!show||!hide) return;
  show.style.backgroundImage='url('+PLAY_DIR+'play_bg_'+kind+'.png)';
  show.style.opacity='1'; hide.style.opacity='0'; bgTop=!bgTop;
}
function setRing(locked){
  if(locked===ringLocked) return; ringLocked=locked;
  const el=$('targetWrap'); if(el) el.style.backgroundImage='url('+PLAY_DIR+(locked?'target_ring_locked':'target_ring')+'.png)';
}
function initPlayArt(){
  const cw=$('curWrap'); if(cw) cw.style.backgroundImage='url('+PLAY_DIR+'number_stage.png)';
  setRing(false); setBG('normal');
  setTimeout(()=>['golden','roll'].forEach(k=>{ const i=new Image(); i.src=PLAY_DIR+'play_bg_'+k+'.png'; }), 1200);
  const i=new Image(); i.src=PLAY_DIR+'target_ring_locked.png';
}
function renderMute(){"""))

# ── 라운드마다 배경 전환 ──────────────────────────────────────────
S.append(("""  chainAll=[]; chain=[]; chainIdx=0; renderChainTag();
  if(rule.type==='choice'){ setupChoice(); return; }""",
"""  chainAll=[]; chain=[]; chainIdx=0; renderChainTag();
  setBG(rule.type==='roll' ? 'roll' : (rule.golden ? 'golden' : 'normal'));
  if(rule.type==='choice'){ setupChoice(); return; }"""))

# ── 목표에 도달하면 조준링을 잠금 버전으로 ────────────────────────
S.append(("""    c.classList.toggle('ontarget', cur===target); if(cur===target) targetShownAt=now();
    $('vig').style.boxShadow='inset 0 0 90px 10px rgba(90,50,160,.55)';""",
"""    c.classList.toggle('ontarget', cur===target); if(cur===target) targetShownAt=now();
    setRing(cur===target);
    $('vig').style.boxShadow='inset 0 0 90px 10px rgba(90,50,160,.55)';"""))

S.append(("""  const onT = cur===target; c.classList.toggle('ontarget', onT); if(onT) targetShownAt=now();""",
"""  const onT = cur===target; c.classList.toggle('ontarget', onT); if(onT) targetShownAt=now();
  setRing(onT);"""))

# ── 시작 시 초기화 ────────────────────────────────────────────────
S.append(("""  mprog('play',1); slowPrev=false;""",
"""  mprog('play',1); slowPrev=false; initPlayArt();"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:70]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('매칭 %d건: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('교체 %d건 완료' % len(S))
