# -*- coding: utf-8 -*-
"""글로벌 일일 랭킹 (1회성 패치)

컬렉션 경로에 날짜를 넣는다: number_daily/{YYYY-MM-DD}/scores/{uid}
- 날짜가 경로에 있으므로 복합 색인이 필요 없다(score 단일 정렬만 쓴다)
- 문서 ID가 uid라 setDoc으로 덮어쓰면 '1인 1기록'이 저절로 보장된다
- 규칙이 아직 안 열렸으면 읽기/쓰기가 조용히 실패하고 로컬 기록으로만 동작한다
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #dailyLog{width:min(92vw,340px);margin-top:4px}""",
"""  #dailyLog{width:min(92vw,340px);margin-top:4px}
  #dailyLbList{width:min(92vw,340px);margin:4px 0 2px;max-height:34vh;overflow-y:auto;-webkit-overflow-scrolling:touch}
  #dailyTabs{display:flex;gap:7px;margin:8px 0 2px}"""))

# ── HTML: 오늘의 랭킹 영역 ────────────────────────────────────────
S.append(("""  <div class="sub" style="font-size:12px;opacity:.6;margin-top:10px">최근 기록</div>
  <div id="dailyLog"></div>""",
"""  <div id="dailyTabs">
    <button class="stab on" id="dtabRank">🌍 오늘의 랭킹</button>
    <button class="stab" id="dtabLog">📝 내 기록</button>
  </div>
  <div id="dailyLbList"></div>
  <div id="dailyLog" class="hidden"></div>"""))

# ── 제출·조회 ─────────────────────────────────────────────────────
S.append(("""function shareDaily(){""",
"""// 날짜를 경로에 둔다 → 복합 색인 불필요, 문서 ID가 uid라 1인 1기록
function dailyUid(){ try{ let u=localStorage.getItem('num_uid');
  if(!u){ u='u'+Date.now().toString(36)+Math.random().toString(36).slice(2,8); localStorage.setItem('num_uid',u); }
  return u; }catch(e){ return 'u0'; } }
let dailyLbState='idle';    // idle | ok | closed (규칙 미개방)
async function dailySubmit(day, sc, hh){
  if(!fbReady) return false;
  try{
    await fbApi.setDoc(fbApi.doc(fbDb,'number_daily',day,'scores',dailyUid()),
      { name:String(myName).slice(0,16), score:Math.floor(sc), hits:hh|0, ts:fbApi.serverTimestamp() });
    dailyLbState='ok'; return true;
  }catch(e){ dailyLbState='closed'; return false; }
}
async function dailyTop(day){
  if(!fbReady) return null;
  try{
    const q=fbApi.query(fbApi.collection(fbDb,'number_daily',day,'scores'), fbApi.orderBy('score','desc'), fbApi.limit(50));
    const snap=await fbApi.getDocs(q);
    dailyLbState='ok';
    return snap.docs.map(d=>({ id:d.id, name:String(d.data().name||'익명'), score:d.data().score|0, hits:d.data().hits|0 }));
  }catch(e){ dailyLbState='closed'; return null; }
}
async function renderDailyLb(){
  const box=$('dailyLbList'); if(!box) return;
  const d=loadDaily2();
  if(!fbReady){ box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.6;padding:14px">오프라인이에요 · 내 기록만 저장돼요</div>'; return; }
  box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.6;padding:14px">🌍 오늘의 순위 불러오는 중…</div>';
  const rows=await dailyTop(d.d);
  if(!rows){ box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.6;padding:12px">아직 글로벌 일일 랭킹이 열리지 않았어요.<br/>내 기록은 안전하게 저장되고 있어요 📝</div>'; return; }
  if(!rows.length){ box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.6;padding:14px">오늘 첫 기록의 주인공이 되어보세요! 🎯</div>'; return; }
  const me=dailyUid();
  box.innerHTML=rows.slice(0,30).map((r,i)=>{ const mine=r.id===me;
    const medal=['🥇','🥈','🥉'][i]||('<span style="opacity:.5;display:inline-block;width:1.4em">'+(i+1)+'</span>');
    return '<div class="lbrow" style="padding:7px 12px;margin:4px 0;font-size:15px;background:'+(mine?'rgba(124,246,255,.18)':'rgba(255,255,255,.045)')
      +';border:1px solid '+(mine?'rgba(124,246,255,.55)':'transparent')+'"><span>'+medal+' '+esc(r.name)
      +'</span><b style="color:#7cf6ff">'+r.score.toLocaleString()+'<span style="font-size:11px;color:#8892b0;font-weight:700"> · '+r.hits+'연속</span></b></div>'; }).join('');
}
function shareDaily(){"""))

# ── 챌린지 종료 시 그날 최고 기록을 올린다 ────────────────────────
S.append(("""  d.log=(d.log||[]).concat([{s:score,h:hits}]).slice(-DAILY_TRIES);
  if(score>d.best){ d.best=score; d.hits=hits; }
  saveDaily2(d); renderDailyBadge();""",
"""  d.log=(d.log||[]).concat([{s:score,h:hits}]).slice(-DAILY_TRIES);
  const improved = score>d.best;
  if(improved){ d.best=score; d.hits=hits; }
  saveDaily2(d); renderDailyBadge();
  if(improved && d.best>0) dailySubmit(d.d, d.best, d.hits);   // 그날 최고 기록만 올린다"""))

# ── 탭 전환 + 화면 열 때 랭킹 로드 ────────────────────────────────
S.append(("""  $('daily').classList.remove('hidden');
}
function closeDaily(){""",
"""  $('daily').classList.remove('hidden');
  dailyTab('rank');
}
function dailyTab(which){
  const r=which==='rank';
  $('dtabRank').classList.toggle('on',r); $('dtabLog').classList.toggle('on',!r);
  $('dailyLbList').classList.toggle('hidden',!r); $('dailyLog').classList.toggle('hidden',r);
  if(r) renderDailyLb();
}
function closeDaily(){"""))

S.append(("""$('dailyShare').onclick=()=>shareDaily();""",
"""$('dailyShare').onclick=()=>shareDaily();
$('dtabRank').onclick=()=>{ sfx('ui_tap'); dailyTab('rank'); };
$('dtabLog').onclick=()=>{ sfx('ui_tap'); dailyTab('log'); };"""))

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
print('일일 랭킹 패치 %d건 완료' % len(S))
