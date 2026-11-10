# -*- coding: utf-8 -*-
"""현재 숫자(#cur)를 글자 -> 스프라이트로 그릴 수 있게 렌더러를 깐다. (1회성 패치)

게임은 숫자 색을 매 프레임 바꾼다(콤보 과열 그라디언트 + 상태색 5종).
그래서 스프라이트를 '마스크'로 쓴다 — 그림은 모양만 주고 색은 currentColor가
입힌다. 덕분에 기존 색 로직을 한 줄도 건드리지 않는다.

아트(digit_0~9.webp)는 아직 없다. DIGIT_SPR=false 로 깔아두고,
아트가 들어오면 true 한 줄만 바꾸면 켜진다. 켠 뒤 파일을 못 불러와도
글자 렌더링으로 자동 복구된다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #cur{font-size:126px;font-weight:900;line-height:1;margin:16px 0}""",
"""  #cur{font-size:126px;font-weight:900;line-height:1;margin:16px 0}
  /* 숫자 스프라이트 — 그림은 마스크(모양)만 주고 색은 currentColor가 입힌다.
     그래서 과열 그라디언트와 상태색 5종이 글자일 때와 똑같이 동작한다. */
  #cur.spr{display:flex;align-items:center;justify-content:center;font-size:0;line-height:0}
  #cur.spr>i{display:block;width:var(--dw);height:var(--dh);margin:0 var(--dm);
    background-color:currentColor;
    -webkit-mask-size:contain;mask-size:contain;
    -webkit-mask-position:center;mask-position:center;
    -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
  /* 마스크에는 text-shadow가 안 먹는다 — 같은 빛을 drop-shadow로 옮겼다 */
  #cur.spr.miss{filter:drop-shadow(0 0 26px rgba(255,90,110,.7))}
  #cur.spr.hit{filter:drop-shadow(0 0 26px rgba(92,255,176,.7))}
  #cur.spr.roll{filter:drop-shadow(0 0 4px #c9a3ff) drop-shadow(0 0 16px rgba(201,163,255,.55))}
  #cur.spr.ontarget{filter:drop-shadow(0 0 30px rgba(255,225,77,.85)) drop-shadow(0 0 60px rgba(255,180,40,.45))}"""))

# ── 렌더러 ────────────────────────────────────────────────────────
S.append(("""function initPlayArt(){""",
"""// ── 숫자 스프라이트 ──────────────────────────────────────────────
// 아트(digit_0~9.webp)가 들어오면 아래 한 줄을 true 로. 켜도 파일을 못 불러오면
// 글자 렌더링으로 자동 복구되므로 구버전 APK·오프라인에서도 안전하다.
const DIGIT_SPR=false;
let digitOK=false, digitTried=false;
function initDigits(){
  if(!DIGIT_SPR || digitTried) return; digitTried=true;
  let left=10, bad=false;
  for(let i=0;i<10;i++){
    const im=new Image();
    im.onload=()=>{ if(!--left && !bad){ digitOK=true; if(state==='play') try{render(false);}catch(e){} } };
    im.onerror=()=>{ bad=true; };
    im.src=PLAY_DIR+'digit_'+i+'.webp';
  }
}
// 캔버스 224x320 안에서 글자 높이가 256이므로
//   스프라이트 높이 = 글자 크기 x 0.738(글자 높이 비율) x 1.25(캔버스/글자 높이)
// 폭은 캔버스 비율(224/320), 자간은 폰트의 advance(0.579em)에 맞춰 음수 마진으로 좁힌다.
function setCur(v, sizes){
  const el=$('cur'), s=String(v), fs=sizes[Math.min(s.length,sizes.length)-1];
  if(!digitOK || !/^[0-9]+$/.test(s)){
    el.classList.remove('spr'); el.style.fontSize=fs+'px';
    if(el.firstElementChild || el.textContent!==s) el.textContent=s;
    return;
  }
  const dh=Math.round(fs*0.9225), dw=Math.round(dh*0.7), dm=Math.round(dh*0.036);
  if(!el.classList.contains('spr')){ el.textContent=''; el.classList.add('spr'); }
  el.style.setProperty('--dh',dh+'px'); el.style.setProperty('--dw',dw+'px'); el.style.setProperty('--dm',(-dm)+'px');
  while(el.children.length>s.length) el.removeChild(el.lastChild);
  while(el.children.length<s.length) el.appendChild(document.createElement('i'));
  for(let k=0;k<s.length;k++){
    const c=el.children[k];
    if(c._d!==s[k]){ c._d=s[k]; const u='url('+PLAY_DIR+'digit_'+s[k]+'.webp)';
      c.style.webkitMaskImage=u; c.style.maskImage=u; }
  }
}
function initPlayArt(){
  initDigits();"""))

# ── render()에서 교체 ─────────────────────────────────────────────
S.append(("""  const c=$('cur'); c.textContent=cur; fitNum(c, cur, [126,126,104,80]);""",
          """  const c=$('cur'); setCur(cur, [126,126,104,80]);"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:72]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('매칭 %d건: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('숫자 스프라이트 렌더러 %d건 연결' % len(S))
