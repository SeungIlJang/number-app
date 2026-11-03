# -*- coding: utf-8 -*-
"""일일 챌린지 모드 — 진입 화면 · 하루 3회 · 결과 공유 (1회성 패치)"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  body.menu #modBar{visibility:hidden}""",
"""  body.menu #modBar{visibility:hidden}
  /* 일일 챌린지 */
  #daily{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    background:rgba(8,10,22,.95);gap:8px;padding:24px;padding-top:calc(26px + env(safe-area-inset-top,0px));z-index:12;overflow-y:auto}
  #dailyX{position:absolute;top:calc(12px + env(safe-area-inset-top,0px));right:16px;width:42px;height:42px;display:flex;
    align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#cfe;background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.18);border-radius:50%;cursor:pointer;z-index:13}
  #dailyCard{width:min(92vw,340px);background:rgba(124,246,255,.08);border:1px solid rgba(124,246,255,.3);
    border-radius:16px;padding:14px 16px;margin:4px 0}
  #dailyCard .dk{font-size:13px;color:#7cf6ff;font-weight:800}
  #dailyCard .dv{font-size:30px;font-weight:900;margin:3px 0}
  .dtry{display:inline-block;width:11px;height:11px;border-radius:50%;margin:0 3px;background:rgba(255,255,255,.18)}
  .dtry.used{background:#7cf6ff}
  #dailyLog{width:min(92vw,340px);margin-top:4px}
  .dlog{display:flex;justify-content:space-between;padding:7px 12px;margin:4px 0;border-radius:10px;
    background:rgba(255,255,255,.05);font-size:14px;font-weight:700}
  #dailyBadge{position:absolute;top:-7px;right:-7px;background:#ff5a6e;color:#fff;font-size:10px;font-weight:900;
    border-radius:9px;padding:1px 5px}"""))

# ── HTML ──────────────────────────────────────────────────────────
S.append(("""    <button class="btn" id="helpBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f;padding:10px 16px;font-size:15px">📖 방법</button>""",
"""    <button class="btn" id="helpBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f;padding:10px 16px;font-size:15px">📖 방법</button>
  </div>
  <div style="display:flex;margin-top:9px">
    <button class="btn" id="dailyBtn" style="position:relative;background:#1b3a4a;box-shadow:0 6px 0 #0d2029;padding:12px 26px;font-size:16px;border:1px solid rgba(124,246,255,.45)">📅 일일 챌린지<span id="dailyBadge" class="hidden">NEW</span></button>"""))

S.append(("""<div id="draft" class="hidden">""",
"""<div id="daily" class="hidden">
  <div id="dailyX" role="button" aria-label="닫기">✕</div>
  <h1 style="font-size:30px">📅 일일 챌린지</h1>
  <div class="sub" style="font-size:13.5px">오늘은 <b style="color:#7cf6ff">모두가 똑같은 순서</b>의 라운드를 받아요<br/>부스터 없이, 실력만으로</div>
  <div id="dailyCard">
    <div class="dk" id="dailyDate">–</div>
    <div class="dv" id="dailyBest">–</div>
    <div class="dk" id="dailyTries" style="color:#8892b0;font-weight:700">남은 도전 –</div>
  </div>
  <button class="btn" id="dailyStart">도전!</button>
  <button class="btn" id="dailyShare" style="margin-top:6px;background:#20263c;box-shadow:0 6px 0 #10131f;padding:11px 22px;font-size:15px">🏆 결과 공유</button>
  <div class="sub" style="font-size:12px;opacity:.6;margin-top:10px">최근 기록</div>
  <div id="dailyLog"></div>
  <button class="btn" id="dailyClose" style="margin-top:4px;background:#20263c;box-shadow:0 6px 0 #10131f">닫기</button>
</div>

<div id="draft" class="hidden">"""))

# ── 상태 + 로직 ───────────────────────────────────────────────────
S.append(("""// 5연속마다 강화 선택 — 전환 텀을 '내 판을 만드는' 순간으로 바꾼다""",
"""// ── 일일 챌린지 ───────────────────────────────────────────────────
// 같은 날이면 시드가 같아 라운드 순서·강화 카드까지 동일하다. 하루 3회, 그중 최고 기록이 그날의 성적.
const DAILY_TRIES=3;
let dailyMode=false, dailyRunMods=[];
function loadDaily2(){
  let d=null; try{ d=JSON.parse(localStorage.getItem('num_daily2')||'null'); }catch(e){}
  if(!d || d.d!==dayKey()) d={d:dayKey(), tries:0, best:0, hits:0, log:[]};
  return d;
}
function saveDaily2(d){ try{ localStorage.setItem('num_daily2', JSON.stringify(d)); }catch(e){} }
function renderDailyBadge(){
  const b=$('dailyBadge'); if(!b) return;
  const d=loadDaily2(); const left=DAILY_TRIES-d.tries;
  b.textContent=left>0?left:'✓'; b.classList.toggle('hidden', false);
  b.style.background = left>0 ? '#ff5a6e' : '#2ec77a';
}
function openDaily(){
  const d=loadDaily2(); const left=Math.max(0,DAILY_TRIES-d.tries);
  $('dailyDate').textContent=d.d+' 오늘의 수열';
  $('dailyBest').innerHTML = d.best ? ('<b style="color:#ffd34d">'+d.best.toLocaleString()+'</b>점 <span style="font-size:14px;color:#8892b0">· '+d.hits+'연속</span>') : '<span style="color:#5a6684">아직 기록 없음</span>';
  let dots=''; for(let i=0;i<DAILY_TRIES;i++) dots+='<span class="dtry'+(i<d.tries?' used':'')+'"></span>';
  $('dailyTries').innerHTML='남은 도전 <b style="color:'+(left?'#7cf6ff':'#ff5a6e')+'">'+left+'</b>/'+DAILY_TRIES+' '+dots;
  const sb=$('dailyStart'); sb.disabled=!left; sb.style.opacity=left?1:.45; sb.textContent=left?'도전!':'내일 다시 만나요';
  $('dailyShare').style.display = d.best?'block':'none';
  $('dailyLog').innerHTML = (d.log||[]).slice().reverse().map((r,i)=>
    '<div class="dlog"><span>'+(i+1)+'번째 도전</span><b style="color:#7cf6ff">'+r.s.toLocaleString()+'점 · '+r.h+'연속</b></div>').join('')
    || '<div class="sub" style="font-size:12px;opacity:.5;text-align:center">아직 없어요</div>';
  $('daily').classList.remove('hidden');
}
function closeDaily(){ $('daily').classList.add('hidden'); }
function startDaily(){
  const d=loadDaily2(); if(d.tries>=DAILY_TRIES) return;
  d.tries++; saveDaily2(d);
  dailyMode=true; dailyRunMods=[];
  rngF=mulberry32(daySeed(d.d));           // 오늘의 시드 고정
  closeDaily(); start();
}
function finishDaily(){
  if(!dailyMode) return; dailyMode=false; rngF=Math.random;
  const d=loadDaily2();
  d.log=(d.log||[]).concat([{s:score,h:hits}]).slice(-DAILY_TRIES);
  if(score>d.best){ d.best=score; d.hits=hits; }
  saveDaily2(d); renderDailyBadge();
}
function shareDaily(){
  const d=loadDaily2();
  const icons=dailyRunMods.map(id=>(MOD_BY[id]?MOD_BY[id].i:'')).join('');
  const txt='멈춰라 숫자 📅'+d.d+'\\n⭐ '+d.best.toLocaleString()+'점 · '+d.hits+'연속 '+(icons?('\\n'+icons):'')
    +'\\n같은 수열로 도전해봐!\\nhttps://seungiljang.github.io/games/number.html';
  try{ if(navigator.share){ navigator.share({title:'멈춰라 숫자 일일 챌린지', text:txt}); return; } }catch(e){}
  try{ navigator.clipboard.writeText(txt); floatText('📋 복사됨!','#7cf6ff'); }catch(e){}
}
// 5연속마다 강화 선택 — 전환 텀을 '내 판을 만드는' 순간으로 바꾼다"""))

# ── 강화 선택 기록(공유용) ────────────────────────────────────────
S.append(("""  modOwned[id]=(modOwned[id]||0)+1; m.a(); renderModBar();""",
          """  modOwned[id]=(modOwned[id]||0)+1; m.a(); renderModBar(); dailyRunMods.push(id);"""))

# ── 챌린지에선 부스터 금지(공정성) ────────────────────────────────
S.append(("""  runBoost={};
  for(const B of BOOSTS){ if(eqb[B.id] && (bst[B.id]||0)>0){ bst[B.id]--; runBoost[B.id]=true; if(!bst[B.id]) eqb[B.id]=false; } }""",
          """  runBoost={};
  if(!dailyMode) for(const B of BOOSTS){ if(eqb[B.id] && (bst[B.id]||0)>0){ bst[B.id]--; runBoost[B.id]=true; if(!bst[B.id]) eqb[B.id]=false; } }"""))

# ── 죽을 때 챌린지 결과 반영 ──────────────────────────────────────
S.append(("""  deathCount++;
  renderChase();""",
          """  deathCount++;
  const wasDaily=dailyMode; finishDaily();
  if(wasDaily) $('overTitle').textContent = rec?'🏆 신기록!':'📅 오늘의 도전 종료';
  renderChase();"""))

# ── 챌린지 기록은 전세계 랭킹에 올리지 않는다(조건이 다르므로) ────
S.append(("""  if(fbReady && score>0 && rec){ fbSubmit(myName,score);""",
          """  if(fbReady && score>0 && rec && !wasDaily){ fbSubmit(myName,score);"""))

# ── 버튼 연결 + 초기 배지 ─────────────────────────────────────────
S.append(("""$('rankCard').onclick=()=>{ sfx('ui_tap'); openRanks(); };""",
"""$('rankCard').onclick=()=>{ sfx('ui_tap'); openRanks(); };
$('dailyBtn').onclick=()=>openDaily();
$('dailyClose').onclick=()=>closeDaily();
$('dailyX').onclick=()=>closeDaily();
$('dailyStart').onclick=()=>startDaily();
$('dailyShare').onclick=()=>shareDaily();"""))

S.append(("""renderRankCard(); renderDaily(); renderBoostRow(); document.body.classList.add('menu');""",
          """renderRankCard(); renderDaily(); renderBoostRow(); renderDailyBadge(); document.body.classList.add('menu');"""))

# ── 홈으로 돌아갈 때 챌린지 상태 정리 ─────────────────────────────
S.append(("""  $('draft').classList.add('hidden'); modOwned={}; renderModBar();""",
          """  $('draft').classList.add('hidden'); modOwned={}; renderModBar();
  dailyMode=false; rngF=Math.random; renderDailyBadge();"""))

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
print('챌린지 패치 %d건 완료' % len(S))
