# -*- coding: utf-8 -*-
"""런 중 모디파이어 선택(3택 1) 추가 — 판마다 다른 빌드를 만드는 장치 (1회성 패치)

5연속마다 카드 3장 중 하나를 고른다. 죽은 전환 텀 대신 '내 판을 만드는' 선택이 들어간다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #muteBtn.off{opacity:.45}""",
"""  #muteBtn.off{opacity:.45}
  /* 런 중 모디파이어 선택 */
  #draft{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(8,10,22,.93);gap:9px;padding:22px;z-index:11}
  #draft h1{font-size:26px;margin:0}
  #draftList{width:100%;max-width:340px;display:flex;flex-direction:column;gap:10px;margin-top:6px}
  .modcard{display:flex;align-items:center;gap:12px;padding:13px 15px;border-radius:15px;text-align:left;
    background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);cursor:pointer}
  .modcard:active{background:rgba(124,246,255,.16);border-color:#7cf6ff}
  .modcard .mi{font-size:30px;flex:0 0 auto;width:38px;text-align:center}
  .modcard .mn{font-size:17.5px;font-weight:900}
  .modcard .md{font-size:12.5px;color:#9fb0cc;font-weight:700;margin-top:2px}
  .modcard .mlv{font-size:11px;color:#5a6684;font-weight:800}
  #modBar{position:fixed;top:calc(62px + env(safe-area-inset-top,0px));left:0;right:0;text-align:center;
    font-size:14px;z-index:3;pointer-events:none;min-height:18px;letter-spacing:2px}
  body.menu #modBar{visibility:hidden}"""))

# ── HTML ──────────────────────────────────────────────────────────
S.append(("""<div id="muteBtn" role="button" aria-label="소리 켜기 끄기">\U0001F50A</div>""",
"""<div id="muteBtn" role="button" aria-label="소리 켜기 끄기">\U0001F50A</div>
<div id="modBar"></div>"""))

S.append(("""<div id="ranks" class="hidden">""",
"""<div id="draft" class="hidden">
  <div class="sub" id="draftWhy" style="font-size:13px;color:#7cf6ff">5연속 달성!</div>
  <h1>강화 선택</h1>
  <div class="sub" style="font-size:13px;opacity:.75">하나를 고르면 이번 판 내내 적용돼요</div>
  <div id="draftList"></div>
</div>

<div id="ranks" class="hidden">"""))

# ── 모디파이어 정의 + 상태 ────────────────────────────────────────
S.append(("""let state='start', cur=0, target=0, score=0, hits=0, rule=null, ti=0, seq=[], timer=null;""",
"""// ── 런 중 강화(모디파이어) ────────────────────────────────────────
// 판마다 다른 빌드가 나오도록 5연속마다 3택 1. 위험/보상이 갈리는 카드를 섞는다.
const MODS=[
  {id:'speed',  i:'⚡', n:'가속',     d:'속도 +14% · 점수 ×1.3',        max:5, a:()=>{ modSpeed*=0.86; modScore*=1.3; }},
  {id:'slow',   i:'🐢', n:'감속',     d:'속도 -15% · 점수 ×0.88',       max:3, a:()=>{ modSpeed*=1.15; modScore*=0.88; }},
  {id:'chain',  i:'🔗', n:'체인 특화', d:'체인 등장↑ · 완성 보너스 ×1.5', max:3, a:()=>{ modChain+=0.12; modChainBonus*=1.5; }},
  {id:'perfect',i:'✨', n:'정밀',     d:'PERFECT 판정 +70ms · 배수 상한 +1', max:3, a:()=>{ modPerfect+=70; modMultCap+=1; }},
  {id:'life',   i:'💛', n:'생명',     d:'생명 +1 (상한도 +1)',          max:3, a:()=>{ heartMax++; hearts=Math.min(heartMax,hearts+1); renderHearts(); }},
  {id:'golden', i:'🌟', n:'황금',     d:'골든 라운드 2배 자주 · 골든 ×1.5', max:2, a:()=>{ modGolden++; modGoldenScore*=1.5; }},
  {id:'read',   i:'🧮', n:'해독',     d:'수열을 6개까지 표시 · 점수 ×0.92', max:1, a:()=>{ modSeq=6; modScore*=0.92; }},
  {id:'lucky',  i:'🎲', n:'행운',     d:'롤링 2배 자주 · 롤링 점수 ×1.6', max:2, a:()=>{ modRoll+=0.10; modRollScore*=1.6; }},
];
const MOD_BY={}; MODS.forEach(m=>MOD_BY[m.id]=m);
let modSpeed=1, modScore=1, modChain=0, modChainBonus=1, modPerfect=0, modMultCap=5,
    modGolden=0, modGoldenScore=1, modSeq=4, modRoll=0, modRollScore=1, heartMax=3,
    modOwned={}, nextDraftAt=5;
function resetMods(){
  modSpeed=1; modScore=1; modChain=0; modChainBonus=1; modPerfect=0; modMultCap=5;
  modGolden=0; modGoldenScore=1; modSeq=4; modRoll=0; modRollScore=1; heartMax=3;
  modOwned={}; nextDraftAt=5; renderModBar();
}
function renderModBar(){
  const el=$('modBar'); if(!el) return;
  const keys=Object.keys(modOwned);
  el.innerHTML = keys.length ? keys.map(k=>'<span style="margin:0 2px">'+MOD_BY[k].i+(modOwned[k]>1?('<span style="font-size:10px">'+modOwned[k]+'</span>'):'')+'</span>').join('') : '';
}
let state='start', cur=0, target=0, score=0, hits=0, rule=null, ti=0, seq=[], timer=null;"""))

# ── 선택 화면 ─────────────────────────────────────────────────────
S.append(("""function rollMiss(timeout){""",
"""// 5연속마다 강화 선택 — 전환 텀을 '내 판을 만드는' 순간으로 바꾼다
function openDraft(){
  state='draft'; clearTimeout(timer); clearTimeout(rollTO); clearTimeout(cTO); clearTimeout(cCd);
  const pool=MODS.filter(m=>(modOwned[m.id]||0)<m.max);
  const pick3=[]; const bag=pool.slice();
  while(pick3.length<3 && bag.length) pick3.push(bag.splice(Math.floor(Math.random()*bag.length),1)[0]);
  $('draftWhy').textContent=hits+'연속 달성!';
  const box=$('draftList');
  box.innerHTML=pick3.map(m=>{ const lv=modOwned[m.id]||0;
    return '<div class="modcard" data-m="'+m.id+'"><span class="mi">'+m.i+'</span><span style="flex:1">'
      +'<span class="mn">'+m.n+'</span>'+(lv?' <span class="mlv">Lv'+lv+'→'+(lv+1)+'</span>':'')
      +'<div class="md">'+m.d+'</div></span></div>'; }).join('');
  box.querySelectorAll('.modcard').forEach(c=>c.onclick=()=>takeMod(c.dataset.m));
  if(!sfx('golden_enter')) chord(660);
  $('draft').classList.remove('hidden');
}
function takeMod(id){
  if(state!=='draft') return;
  const m=MOD_BY[id]; if(!m) return;
  modOwned[id]=(modOwned[id]||0)+1; m.a(); renderModBar();
  $('draft').classList.add('hidden'); state='play';
  floatText(m.i+' '+m.n,'#7cf6ff'); if(!sfx('coin_reward')) tone(880,0.1,'triangle',0.07); vib([15,30,15]);
  newRound(true); if(rule.type!=='choice') nextTick(Math.max(220, speed()));
}
function rollMiss(timeout){"""))

# ── 모디파이어를 실제 수치에 반영 ─────────────────────────────────
S.append(("""function speed(){ let s=Math.max(210, 660 - hits*18); if(slowLeft>0) s=Math.round(s*1.35); return s; }""",
          """function speed(){ let s=Math.max(210, 660 - hits*18)*modSpeed; if(slowLeft>0) s*=1.35; return Math.max(150, Math.round(s)); }"""))

S.append(("""function judge(){ if(!targetShownAt) return 'GOOD'; return (now()-targetShownAt) < 190 ? 'PERFECT' : 'GOOD'; }""",
          """function judge(){ if(!targetShownAt) return 'GOOD'; return (now()-targetShownAt) < (190+modPerfect) ? 'PERFECT' : 'GOOD'; }"""))

S.append(("""  if(grade==='PERFECT'){ mult=Math.min(5, mult+1); mprog('perfect',1); } else mult=1;""",
          """  if(grade==='PERFECT'){ mult=Math.min(modMultCap, mult+1); mprog('perfect',1); } else mult=1;"""))

S.append(("""  const base=((wasRoll?25:10) + (hits-1)*2) * (wasGolden?2:1);    // 🌟 골든 라운드 점수 ×2
  const gain=Math.round(base*mult*link*(runBoost.score2?2:1));""",
          """  const base=((wasRoll?25*modRollScore:10) + (hits-1)*2) * (wasGolden?2*modGoldenScore:1);   // 🌟 골든 라운드 점수 ×2
  const gain=Math.round(base*mult*link*modScore*(runBoost.score2?2:1));"""))

S.append(("""    const cb=Math.round(base*chainAll.length*0.6*(runBoost.score2?2:1));""",
          """    const cb=Math.round(base*chainAll.length*0.6*modChainBonus*modScore*(runBoost.score2?2:1));"""))

S.append(("""  const base=15 + (hits-1)*2, gain=Math.round(base*mult*(runBoost.score2?2:1));   // 콤보 배수·부스터 일관 적용""",
          """  const base=15 + (hits-1)*2, gain=Math.round(base*mult*modScore*(runBoost.score2?2:1));   // 콤보 배수·부스터 일관 적용"""))

S.append(("""  const rollCh = hits>=4 ? (hits<14?0.20:0.11) : 0;            // ⚡ 롤링 — 후반엔 빈도↓(생명 남발 방지)""",
          """  const rollCh = hits>=4 ? (hits<14?0.20:0.11)+modRoll : 0;    // ⚡ 롤링 — 후반엔 빈도↓(생명 남발 방지)"""))

S.append(("""  if(hits>=6 && hits%10===0){ const g={type:'add', s:pick([3,4,5])}; g.golden=true; return g; }  // 🌟 10·20·30… 골든(점수 ×2)""",
          """  const gEvery=modGolden?5:10;                                  // 🌟 황금 강화를 먹으면 5연속마다
  if(hits>=6 && hits%gEvery===0){ const g={type:'add', s:pick([3,4,5])}; g.golden=true; return g; }"""))

S.append(("""cur=advance(cur,ti); ti++; seq.push(cur); if(seq.length>4) seq.shift();""",
          """cur=advance(cur,ti); ti++; seq.push(cur); if(seq.length>modSeq) seq.shift();"""))

S.append(("""function renderHearts(){ const e=$('hearts'); if(e) e.textContent = hearts>0 ? ('💛'.repeat(Math.min(hearts,HEART_MAX))) : ''; }""",
          """function renderHearts(){ const e=$('hearts'); if(e) e.textContent = hearts>0 ? ('💛'.repeat(Math.min(hearts,heartMax))) : ''; }"""))

S.append(("""  if(wasRoll){ const was=hearts; hearts=Math.min(HEART_MAX,hearts+1); renderHearts(); mprog('roll',1);""",
          """  if(wasRoll){ const was=hearts; hearts=Math.min(heartMax,hearts+1); renderHearts(); mprog('roll',1);"""))

# ── 라운드가 끝날 때 강화 선택을 끼워 넣는다 ──────────────────────
S.append(("""  inGap=true; clearTimeout(timer); clearTimeout(rollTO);   // 전환 텀(약 1초) — 그 사이 입력 무시
  setTimeout(()=>{ if(state!=='play') return; newRound(true); if(rule.type!=='choice') nextTick(Math.max(220, speed())); }, GAP_MS);""",
"""  inGap=true; clearTimeout(timer); clearTimeout(rollTO);   // 전환 텀 — 그 사이 입력 무시
  setTimeout(()=>{ if(state!=='play') return;
    if(hits>=nextDraftAt){ nextDraftAt=hits+5; openDraft(); return; }   // 5연속마다 강화 선택
    newRound(true); if(rule.type!=='choice') nextTick(Math.max(220, speed())); }, GAP_MS);"""))

# ── 시작 시 초기화 ────────────────────────────────────────────────
S.append(("""  mprog('play',1); slowPrev=false; initPlayArt();""",
          """  mprog('play',1); slowPrev=false; initPlayArt(); resetMods(); $('draft').classList.add('hidden');"""))

# ── 죽거나 홈으로 가면 정리 ───────────────────────────────────────
S.append(("""function die(msg, fromChoice){
  if(state!=='play') return;""",
          """function die(msg, fromChoice){
  if(state!=='play') return;
  $('draft').classList.add('hidden');"""))

S.append(("""function goHome(){ state='start'; clearTimeout(timer); clearTimeout(rollTO); clearTimeout(cTO); clearTimeout(cCd); document.body.classList.add('menu');""",
          """function goHome(){ state='start'; clearTimeout(timer); clearTimeout(rollTO); clearTimeout(cTO); clearTimeout(cCd); document.body.classList.add('menu');
  $('draft').classList.add('hidden'); modOwned={}; renderModBar();"""))

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
print('모디파이어 패치 %d건 완료' % len(S))
