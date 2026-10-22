# -*- coding: utf-8 -*-
"""games/number.html 에 neon-v1 효과음을 연결한다 (1회성 패치 스크립트)."""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# 1) 엔진 + tone() 음소거 게이트
S.append(("""let AC; function tone(f,d,type,g){ try{""",
          """let AC; function tone(f,d,type,g){ if(!sfxOn) return; try{"""))

S.append(("""function chord(base){ [0,4,7].forEach((s,i)=>setTimeout(()=>tone(base*Math.pow(2,s/12),0.14,'triangle',0.06),i*35)); }""",
          """function chord(base){ [0,4,7].forEach((s,i)=>setTimeout(()=>tone(base*Math.pow(2,s/12),0.14,'triangle',0.06),i*35)); }
// -- 효과음 (neon-v1 샘플) -----------------------------------------
// 납품 믹스가 이미 균형이 잡혀 있어(틱이 가장 작고 STOP이 판정음보다 낮음) 개별 보정 없이 마스터만 올린다.
// sfx()가 false면(로딩중·오프라인·구버전 APK) 호출부가 기존 절차 생성음으로 대체한다.
const SFX_DIR='audio/number/sfx/', SFX_MASTER=2.0;
const SFX_EAGER=['number_tick','rolling_tick','stop_tap','hit_good','hit_perfect','miss','ui_tap'];
const SFX_REST=['game_start','countdown','slow_enter','combo_5','chain_step','chain_complete',
  'rolling_success','rolling_miss','golden_enter','life_continue','coin_reward','rank_up','game_over'];
let sfxBuf={}, sfxPrimed=false;
let sfxOn=(function(){ try{ return localStorage.getItem('num_sfx')!=='0'; }catch(e){ return true; } })();
function actx(){ try{ if(!AC) AC=new(window.AudioContext||window.webkitAudioContext)(); if(AC.state==='suspended') AC.resume(); return AC; }catch(e){ return null; } }
function sfxLoad(n){
  if(n in sfxBuf) return; sfxBuf[n]=null;                       // null = 로딩중
  fetch(SFX_DIR+n+'.wav').then(r=>{ if(!r.ok) throw 0; return r.arrayBuffer(); })
    .then(b=>{ const c=actx(); if(!c) throw 0; return c.decodeAudioData(b); })
    .then(buf=>{ sfxBuf[n]=buf; }).catch(()=>{ sfxBuf[n]=false; });   // false = 실패 → 절차음 유지
}
function sfxPrime(){ if(sfxPrimed) return; sfxPrimed=true; actx();
  SFX_EAGER.forEach(sfxLoad); setTimeout(()=>SFX_REST.forEach(sfxLoad), 1500); }
function sfx(n,g){
  if(!sfxOn) return true;                                       // 음소거: 절차음도 울리지 않게 '처리됨'
  const b=sfxBuf[n];
  if(!b){ if(!(n in sfxBuf)) sfxLoad(n); return false; }
  const c=actx(); if(!c) return false;
  try{ const src=c.createBufferSource(), v=c.createGain(); src.buffer=b;
    v.gain.value=(g==null?1:g)*SFX_MASTER; src.connect(v); v.connect(c.destination); src.start(); return true;
  }catch(e){ return false; }
}
function renderMute(){ const b=$('muteBtn'); if(b){ b.textContent=sfxOn?'\\u{1F50A}':'\\u{1F507}'; b.classList.toggle('off',!sfxOn); } }"""))

# 2) 음소거 버튼
S.append(("""  .art{vertical-align:middle;object-fit:contain;display:inline-block;flex:0 0 auto}""",
          """  .art{vertical-align:middle;object-fit:contain;display:inline-block;flex:0 0 auto}
  #muteBtn{position:fixed;top:calc(46px + env(safe-area-inset-top,0px));right:12px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:17px;border-radius:50%;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);z-index:14;cursor:pointer}
  #muteBtn:active{background:rgba(255,255,255,.22)}
  #muteBtn.off{opacity:.45}"""))

S.append(("""<div id="chase"></div>""",
          """<div id="chase"></div>
<div id="muteBtn" role="button" aria-label="소리 켜기 끄기">\U0001F50A</div>"""))

# 3) 라운드 / 틱
S.append(("""if(rule.golden){ banner('\U0001F31F 골든 라운드! 점수 ×2','#ffd34d'); vib([15,30,15]); tone(880,0.1,'triangle',0.06); }""",
          """if(rule.golden){ banner('\U0001F31F 골든 라운드! 점수 ×2','#ffd34d'); vib([15,30,15]); if(!sfx('golden_enter')) tone(880,0.1,'triangle',0.06); }"""))

S.append(("""    tone(520+ (cur%9)*30, 0.02, 'square', 0.025);""",
          """    if(!sfx('rolling_tick')) tone(520+ (cur%9)*30, 0.02, 'square', 0.025);"""))

S.append(("""  if(slow) tone(880,0.05,'sine',0.05); else tone(300+Math.min(hits,22)*11, 0.03, 'sine', 0.03);""",
          """  if(slow && !slowPrev){ if(!sfx('slow_enter')) tone(880,0.05,'sine',0.05); }        // 슬로모 진입 순간에만
  else if(!sfx('number_tick')) tone(slow?880:300+Math.min(hits,22)*11, slow?0.05:0.03, 'sine', slow?0.05:0.03);
  slowPrev=slow;"""))

# 4) 판정
S.append(("""chord(523); setTimeout(()=>chord(784),120); vib([20,40,20,40,60]); shake=6; }""",
          """if(!sfx('rolling_success')){ chord(523); setTimeout(()=>chord(784),120); } vib([20,40,20,40,60]); shake=6; }"""))

S.append(("""chord(660); setTimeout(()=>tone(990,0.08,'triangle',0.06),90); vib([12,26,12]); shake=8; }""",
          """if(!sfx('hit_perfect')){ chord(660); setTimeout(()=>tone(990,0.08,'triangle',0.06),90); } vib([12,26,12]); shake=8; }"""))

S.append(("""chord(440); vib([15,30,15]); shake=8; }""",
          """if(!sfx('combo_5')) chord(440); vib([15,30,15]); shake=8; }"""))

S.append(("""tone(720+hits*8,0.07,'square',0.07); vib(18); }""",
          """if(!sfx('hit_good')) tone(720+hits*8,0.07,'square',0.07); vib(18); }"""))

S.append(("""    tone(940,0.07,'triangle',0.07); render(false); nextTick(Math.max(200, speed()));""",
          """    if(!sfx('chain_step')) tone(940,0.07,'triangle',0.07); render(false); nextTick(Math.max(200, speed()));"""))

S.append(("""chord(880); vib([20,40,20,40,80]); shake=10;""",
          """if(!sfx('chain_complete')) chord(880); vib([20,40,20,40,80]); shake=10;"""))

S.append(("""tone(220,0.12,'sawtooth',0.07); vib(25);""",
          """if(!sfx('rolling_miss')) tone(220,0.12,'sawtooth',0.07); vib(25);"""))

# 5) 선택형
S.append(("""chord(440); vib([15,30,15]); shake=7; }""",
          """if(!sfx('combo_5')) chord(440); vib([15,30,15]); shake=7; }"""))

S.append(("""tone(760,0.07,'square',0.07); vib(18); }""",
          """if(!sfx('hit_good')) tone(760,0.07,'square',0.07); vib(18); }"""))

# 6) 사망 / 생명 / 게임오버 / 승급
S.append(("""  hitFlash('#ff5a6e'); shake=16; vib(120); tone(200,0.16,'sawtooth',0.09);""",
          """  hitFlash('#ff5a6e'); shake=16; vib(120); if(!sfx('miss')) tone(200,0.16,'sawtooth',0.09);"""))

S.append(("""tone(660,0.12,'sine',0.09); setTimeout(()=>tone(880,0.12,'sine',0.08),110);""",
          """if(!sfx('life_continue')){ tone(660,0.12,'sine',0.09); setTimeout(()=>tone(880,0.12,'sine',0.08),110); }"""))

S.append(("""setTimeout(()=>tone(110,0.3,'sawtooth',0.08),90);""",
          """setTimeout(()=>{ if(!sfx('game_over')) tone(110,0.3,'sawtooth',0.08); },90);"""))

S.append((""" 승급!',up.R.c); chord(660); setTimeout(()=>chord(990),160); vib([25,50,25,50,80]); }""",
          """ 승급!',up.R.c); vib([25,50,25,50,80]); }"""))

S.append(("""$('over').classList.remove('hidden'); renderOverLB(); },750);""",
          """$('over').classList.remove('hidden'); renderOverLB();
    if(up && !sfx('rank_up')){ chord(660); setTimeout(()=>chord(990),160); }   // 승급음은 결과창이 열린 뒤 — 종료음과 분리
  },750);"""))

# 7) 입력 / 시작 / 상점 / 미션
S.append(("""  if(inChoice) return;   // 선택형은 버튼으로만""",
          """  if(inChoice) return;   // 선택형은 버튼으로만
  sfx('stop_tap');       // STOP 입력 타격음 (판정음보다 낮게 — 샘플 없으면 무음)"""))

S.append(("""  mprog('play',1);""",
          """  mprog('play',1); slowPrev=false;
  if(!sfx('game_start')) chord(523);"""))

S.append((""" 획득!','#5cffb0'); vib([15,30,15]); tone(880,0.1,'triangle',0.07); });""",
          """ 획득!','#5cffb0'); vib([15,30,15]); if(!sfx('coin_reward')) tone(880,0.1,'triangle',0.07); });"""))

S.append(("""renderBoostRow(); tone(eqb[id]?760:420,0.06,'square',0.06); });""",
          """renderBoostRow(); if(!sfx('ui_tap')) tone(eqb[id]?760:420,0.06,'square',0.06); });"""))

S.append(("""renderShop(); tone(640,0.05,'square',0.06); });""",
          """renderShop(); if(!sfx('ui_tap')) tone(640,0.05,'square',0.06); });"""))

S.append((""" 획득!',t.accent); vib([15,30,15]); } });""",
          """ 획득!',t.accent); vib([15,30,15]); sfx('coin_reward'); } });"""))

S.append(("""floatText('✅ 미션 완료! \U0001F4B0+'+MBY[id].rw,'#5cffb0'); }""",
          """floatText('✅ 미션 완료! \U0001F4B0+'+MBY[id].rw,'#5cffb0'); sfx('coin_reward'); }"""))

# 8) 전역 리스너
S.append(("""addEventListener('pointerdown', e=>{ if(e.target.closest('.btn')) return; if(state!=='play') return; tap(); });""",
          """addEventListener('pointerdown', sfxPrime);                       // 첫 터치에 오디오 활성화 + 선로딩
addEventListener('click', e=>{ if(e.target.closest('.btn,#lbX,#shopX')) sfx('ui_tap'); }, true);
addEventListener('pointerdown', e=>{ if(e.target.closest('.btn,#muteBtn')) return; if(state!=='play') return; tap(); });
$('muteBtn').onclick=(e)=>{ e.stopPropagation(); sfxOn=!sfxOn; try{ localStorage.setItem('num_sfx', sfxOn?'1':'0'); }catch(e2){}
  renderMute(); if(sfxOn){ sfxPrime(); sfx('ui_tap'); } };
renderMute();"""))

# 9) 상태 변수
S.append(("""let curIsRoll=false, rollLo=0, rollHi=0, rollTO=null, slowEndShown=false;""",
          """let curIsRoll=false, rollLo=0, rollHi=0, rollTO=null, slowEndShown=false, slowPrev=false;"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:75]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('매칭 %d건: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('교체 %d건 완료' % len(S))
