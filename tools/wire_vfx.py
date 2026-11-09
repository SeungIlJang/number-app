# -*- coding: utf-8 -*-
"""2순위 연출 연결: 판정 스탬프 · 성공 버스트 · 체인 링크 (1회성 패치)"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  .float{position:fixed;left:50%;top:46%;transform:translateX(-50%);font-size:34px;font-weight:900;z-index:7;pointer-events:none;animation:fl .7s ease-out forwards}""",
"""  .float{position:fixed;left:50%;top:46%;transform:translateX(-50%);font-size:34px;font-weight:900;z-index:7;pointer-events:none;animation:fl .7s ease-out forwards}
  /* 판정 리본 — 글자가 리본 안에 들어가도록 가로세로를 2:1로 고정 */
  .float.stamped{width:236px;height:118px;display:flex;align-items:center;justify-content:center;
    background-size:contain;background-position:center;background-repeat:no-repeat;font-size:27px;letter-spacing:.5px}
  /* 성공 버스트 — 숫자 뒤에서 한 번 터지고 사라진다 */
  .vfxb{position:fixed;left:50%;top:0;width:240px;height:240px;pointer-events:none;z-index:1;
    background-size:contain;background-position:center;background-repeat:no-repeat;
    animation:vfxb .52s ease-out forwards}
  @keyframes vfxb{
    0%{opacity:0;transform:translate(-50%,-50%) scale(.42)}
    16%{opacity:1;transform:translate(-50%,-50%) scale(1)}
    100%{opacity:0;transform:translate(-50%,-50%) scale(1.42)}}"""))

# ── 엔진 ──────────────────────────────────────────────────────────
S.append(("""function floatText(txt,col){ const d=document.createElement('div'); d.className='float'; d.textContent=txt; d.style.color=col; document.body.appendChild(d); setTimeout(()=>d.remove(),720); }""",
"""// stamp를 주면 글자가 판정 리본 안에 담겨 함께 떠오른다
function floatText(txt,col,stamp){
  const d=document.createElement('div'); d.className='float'; d.textContent=txt; d.style.color=col;
  if(stamp){ d.classList.add('stamped'); d.style.backgroundImage='url('+PLAY_DIR+stamp+'.webp)'; }
  document.body.appendChild(d); setTimeout(()=>d.remove(),720);
}
// 성공 순간 숫자 뒤에서 터지는 버스트
function burstFx(kind){
  const w=$('curWrap'); if(!w) return;
  const r=w.getBoundingClientRect();
  const d=document.createElement('div'); d.className='vfxb';
  d.style.backgroundImage='url('+PLAY_DIR+'burst_'+kind+'.webp)';
  d.style.top=Math.round(r.top+r.height/2)+'px';
  document.body.appendChild(d); setTimeout(()=>d.remove(),560);
}"""))

# ── 선로딩 (플레이 아트와 함께) ───────────────────────────────────
S.append(("""  setTimeout(()=>['golden','roll'].forEach(k=>{ const i=new Image(); i.src=PLAY_DIR+'play_bg_'+k+'.png'; }), 1200);""",
"""  setTimeout(()=>{
    ['golden','roll'].forEach(k=>{ const i=new Image(); i.src=PLAY_DIR+'play_bg_'+k+'.png'; });
    ['burst_hit','burst_perfect','burst_chain','stamp_perfect','stamp_good','stamp_miss','chain_link']
      .forEach(n=>{ const i=new Image(); i.src=PLAY_DIR+n+'.webp'; });
  }, 1200);"""))

# ── 판정별 스탬프 + 버스트 ────────────────────────────────────────
S.append(("""floatText(hearts>was?'⚡ 롤링 성공! 💛 생명 +1':'⚡ 롤링 성공! (생명 최대)','#ffd34d');""",
          """floatText(hearts>was?'💛 생명 +1':'롤링 성공!','#ffd34d','stamp_perfect'); burstFx('perfect');"""))

S.append(("""floatText('PERFECT!'+(mult>1?('  ×'+mult):''),'#ffe14d');""",
          """floatText('PERFECT!'+(mult>1?(' ×'+mult):''),'#ffe14d','stamp_perfect'); burstFx('perfect');"""))

S.append(("""floatText('🔥 '+hits+' 연속!','#ffd34d'); if(!sfx('combo_5',jg)) chord(440); vib([15,30,15]); shake=8; }""",
          """floatText(hits+' 연속!','#ffd34d','stamp_perfect'); burstFx('perfect'); if(!sfx('combo_5',jg)) chord(440); vib([15,30,15]); shake=8; }"""))

S.append(("""floatText(pick(['GOOD!','NICE!','좋아!','정확!']),'#5cffb0'); if(!sfx('hit_good',jg)) tone(720+hits*8,0.07,'square',0.07); vib(18); }""",
          """floatText(pick(['GOOD!','NICE!','좋아!','정확!']),'#5cffb0','stamp_good'); burstFx('hit'); if(!sfx('hit_good',jg)) tone(720+hits*8,0.07,'square',0.07); vib(18); }"""))

S.append(("""floatText('🔗 체인 완성! +'+cb,'#ffd34d');""",
          """floatText('체인 완성 +'+cb,'#ffd34d','stamp_perfect'); burstFx('chain');"""))

# 체인 중간 고리 성공에도 작은 버스트
S.append(("""    if(!sfx('chain_step')) tone(940,0.07,'triangle',0.07); render(false); nextTick(Math.max(200, speed()));""",
          """    if(!sfx('chain_step')) tone(940,0.07,'triangle',0.07); burstFx('chain'); render(false); nextTick(Math.max(200, speed()));"""))

# 선택형 정답
S.append(("""floatText('🔥 '+hits+' 연속!','#ffd34d'); if(!sfx('combo_5')) chord(440); vib([15,30,15]); shake=7; }""",
          """floatText(hits+' 연속!','#ffd34d','stamp_perfect'); if(!sfx('combo_5')) chord(440); vib([15,30,15]); shake=7; }"""))

S.append(("""floatText(pick(['정답!','NICE!','좋아!']),'#5cffb0'); if(!sfx('hit_good')) tone(760,0.07,'square',0.07); vib(18); }""",
          """floatText(pick(['정답!','NICE!','좋아!']),'#5cffb0','stamp_good'); if(!sfx('hit_good')) tone(760,0.07,'square',0.07); vib(18); }"""))

# 실패 — 미스 리본
S.append(("""  floatText(timeout?'⏰ 롤링 놓침 (손해 없음)':'아깝다! (롤링)','#c9a3ff');""",
          """  floatText(timeout?'시간 초과':'아깝다!','#c9a3ff','stamp_miss');"""))

# ── 체인 링크 아이콘 ──────────────────────────────────────────────
S.append(("""  el.innerHTML='🔗 '+chainAll.map((v,i)=>'<span class="'+(i<chainIdx?'done':(i===chainIdx?'now':'todo'))+'">'+v+'</span>').join('<span class="todo"> → </span>');""",
"""  el.innerHTML='<img src="'+PLAY_DIR+'chain_link.webp" alt="" width="19" height="19" class="art" style="margin-right:5px" onerror="this.replaceWith(document.createTextNode(\\'🔗\\'))">'
    +chainAll.map((v,i)=>'<span class="'+(i<chainIdx?'done':(i===chainIdx?'now':'todo'))+'">'+v+'</span>').join('<span class="todo"> → </span>');"""))

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
print('연출 연결 %d건 완료' % len(S))
