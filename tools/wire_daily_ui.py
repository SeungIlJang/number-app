# -*- coding: utf-8 -*-
"""일일 챌린지 화면 리디자인 (1회성 패치)

문제: 반투명 배경이라 뒤의 시작화면이 그대로 비쳐 지저분하고,
요소마다 폭이 제각각에 버튼 위계도 없었다. X와 닫기 버튼이 중복.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS 전면 교체 ─────────────────────────────────────────────────
S.append(("""  /* 일일 챌린지 */
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
  #dailyLbList{width:min(92vw,340px);margin:4px 0 2px;max-height:34vh;overflow-y:auto;-webkit-overflow-scrolling:touch}
  #dailyTabs{display:flex;gap:7px;margin:8px 0 2px}""",
"""  /* 일일 챌린지 */
  #daily{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    background:linear-gradient(180deg,#0c1427 0%,#080b17 55%,#05070f 100%);
    padding:0 20px calc(22px + env(safe-area-inset-bottom,0px));
    padding-top:calc(16px + env(safe-area-inset-top,0px));z-index:12;overflow-y:auto;-webkit-overflow-scrolling:touch}
  #daily::before{content:'';position:absolute;inset:0;background:url(img/number/play/play_bg_normal.png) center/cover;
    opacity:.3;pointer-events:none}
  #daily>*{position:relative;z-index:1;flex:0 0 auto}
  #dailyX{position:absolute;top:calc(12px + env(safe-area-inset-top,0px));right:16px;width:40px;height:40px;display:flex;
    align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#cfe;background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.18);border-radius:50%;cursor:pointer;z-index:13}
  #dailyX:active{background:rgba(255,255,255,.2)}
  #dailyHead{display:flex;flex-direction:column;align-items:center;gap:7px;margin-bottom:14px}
  #dailyHead h1{font-size:26px;margin:0}
  #dailyDateChip{font-size:11.5px;font-weight:900;color:#06121a;background:#7cf6ff;border-radius:999px;padding:3px 12px;letter-spacing:.3px}
  #dailyCard{width:min(92vw,352px);background:linear-gradient(160deg,rgba(124,246,255,.15),rgba(124,246,255,.035));
    border:1px solid rgba(124,246,255,.34);border-radius:20px;padding:17px 18px 14px;text-align:center;
    box-shadow:0 12px 34px rgba(0,0,0,.4)}
  .dk{font-size:11.5px;color:#8fa8c4;font-weight:800;letter-spacing:.5px}
  #dailyBest{font-size:40px;font-weight:900;line-height:1.05;margin:7px 0 1px;text-shadow:0 0 24px rgba(255,211,77,.3)}
  #dailySub{font-size:13px;color:#9fb0cc;font-weight:700;min-height:18px}
  #dailyTriesRow{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:13px;
    padding-top:12px;border-top:1px solid rgba(255,255,255,.1)}
  .dtry{display:inline-block;width:13px;height:13px;border-radius:50%;background:transparent;border:2px solid rgba(255,255,255,.24)}
  .dtry.used{background:#7cf6ff;border-color:#7cf6ff;box-shadow:0 0 9px rgba(124,246,255,.65)}
  #dailyStart{width:min(92vw,352px);margin-top:15px;padding:16px;font-size:19px}
  #dailyTabs{display:flex;width:min(92vw,352px);background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
    border-radius:14px;padding:4px;margin-top:17px;gap:4px}
  #dailyTabs .stab{flex:1;border:none;background:transparent;border-radius:10px;padding:9px 0;font-size:13.5px}
  #dailyTabs .stab.on{background:#3a7bff;color:#fff;border-color:transparent}
  #dailyLbList,#dailyLog{width:min(92vw,352px);margin-top:9px;min-height:128px;max-height:32vh;
    overflow-y:auto;-webkit-overflow-scrolling:touch}
  #dailyShare{margin-top:15px;background:transparent;box-shadow:none;border:1px solid rgba(255,255,255,.22);
    color:#cfe;padding:10px 22px;font-size:14px}
  #dailyShare:active{background:rgba(255,255,255,.1);transform:none}"""))

# ── HTML 재구성 ───────────────────────────────────────────────────
S.append(("""  <div id="dailyX" role="button" aria-label="닫기">✕</div>
  <h1 style="font-size:30px">📅 일일 챌린지</h1>
  <div class="sub" style="font-size:13.5px">오늘은 <b style="color:#7cf6ff">모두가 똑같은 순서</b>의 라운드를 받아요<br/>부스터 없이, 실력만으로</div>
  <div id="dailyCard">
    <div class="dk" id="dailyDate">–</div>
    <div class="dv" id="dailyBest">–</div>
    <div class="dk" id="dailyTries" style="color:#8892b0;font-weight:700">남은 도전 –</div>
  </div>
  <button class="btn" id="dailyStart">도전!</button>
  <button class="btn" id="dailyShare" style="margin-top:6px;background:#20263c;box-shadow:0 6px 0 #10131f;padding:11px 22px;font-size:15px">🏆 결과 공유</button>
  <div id="dailyTabs">
    <button class="stab on" id="dtabRank">🌍 오늘의 랭킹</button>
    <button class="stab" id="dtabLog">📝 내 기록</button>
  </div>
  <div id="dailyLbList"></div>
  <div id="dailyLog" class="hidden"></div>
  <button class="btn" id="dailyClose" style="margin-top:4px;background:#20263c;box-shadow:0 6px 0 #10131f">닫기</button>""",
"""  <div id="dailyX" role="button" aria-label="닫기">✕</div>
  <div id="dailyHead">
    <h1>📅 일일 챌린지</h1>
    <span id="dailyDateChip">–</span>
    <div class="sub" style="font-size:12.5px;line-height:1.55;margin-top:2px">오늘은 <b style="color:#7cf6ff">모두 똑같은 순서</b>의 라운드 · 부스터 없이</div>
  </div>
  <div id="dailyCard">
    <div class="dk">오늘의 최고 기록</div>
    <div id="dailyBest">–</div>
    <div id="dailySub"></div>
    <div id="dailyTriesRow"></div>
  </div>
  <button class="btn" id="dailyStart">도전!</button>
  <div id="dailyTabs">
    <button class="stab on" id="dtabRank">🌍 오늘의 랭킹</button>
    <button class="stab" id="dtabLog">📝 내 기록</button>
  </div>
  <div id="dailyLbList"></div>
  <div id="dailyLog" class="hidden"></div>
  <button class="btn" id="dailyShare">🏆 결과 공유</button>"""))

# ── openDaily 갱신 ────────────────────────────────────────────────
S.append(("""  $('dailyDate').textContent=d.d+' 오늘의 수열';
  $('dailyBest').innerHTML = d.best ? ('<b style="color:#ffd34d">'+d.best.toLocaleString()+'</b>점 <span style="font-size:14px;color:#8892b0">· '+d.hits+'연속</span>') : '<span style="color:#5a6684">아직 기록 없음</span>';
  let dots=''; for(let i=0;i<DAILY_TRIES;i++) dots+='<span class="dtry'+(i<d.tries?' used':'')+'"></span>';
  $('dailyTries').innerHTML='남은 도전 <b style="color:'+(left?'#7cf6ff':'#ff5a6e')+'">'+left+'</b>/'+DAILY_TRIES+' '+dots;""",
"""  $('dailyDateChip').textContent=d.d;
  $('dailyBest').innerHTML = d.best
    ? ('<span style="color:#ffd34d">'+d.best.toLocaleString()+'</span><span style="font-size:19px;color:#8892b0;font-weight:800">점</span>')
    : '<span style="font-size:25px;color:#5a6684">아직 기록 없음</span>';
  $('dailySub').textContent = d.best ? (d.hits+'연속 달성') : '세 번의 기회가 있어요';
  let dots=''; for(let i=0;i<DAILY_TRIES;i++) dots+='<span class="dtry'+(i<d.tries?' used':'')+'"></span>';
  $('dailyTriesRow').innerHTML='<span class="dk">남은 도전</span>'+dots
    +'<span class="dk" style="color:'+(left?'#7cf6ff':'#ff5a6e')+'">'+left+'/'+DAILY_TRIES+'</span>';"""))

# ── 닫기 버튼 제거에 따른 핸들러 정리 ─────────────────────────────
S.append(("""$('dailyClose').onclick=()=>closeDaily();
$('dailyX').onclick=()=>closeDaily();""",
          """$('dailyX').onclick=()=>closeDaily();"""))

# ── 빈 상태 안내도 가운데로 ───────────────────────────────────────
S.append(("""  if(!rows){ box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.6;padding:12px">아직 글로벌 일일 랭킹이 열리지 않았어요.<br/>내 기록은 안전하게 저장되고 있어요 📝</div>'; return; }""",
          """  if(!rows){ box.innerHTML='<div class="sub" style="font-size:12.5px;opacity:.55;padding:40px 12px;text-align:center;line-height:1.7">아직 글로벌 일일 랭킹이<br/>열리지 않았어요 📝<br/><span style="opacity:.8">내 기록은 안전하게 저장되고 있어요</span></div>'; return; }"""))

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
print('UI 리디자인 %d건 완료' % len(S))
