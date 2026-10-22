# -*- coding: utf-8 -*-
"""랭크 엠블럼·부스터 아트가 실제로 보이도록 노출 지점을 늘린다 (1회성 패치)."""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #muteBtn.off{opacity:.45}""",
"""  #muteBtn.off{opacity:.45}
  #rankHead{display:flex;align-items:center;gap:12px}
  #rankEmblemBox{flex:0 0 auto;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:38px;line-height:1}
  #rankCard{cursor:pointer}
  #rankMore{font-size:11.5px;color:#7cf6ff;opacity:.85;margin-top:7px;font-weight:700}
  /* 랭크 전체 보기 */
  #ranks{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;background:rgba(8,10,22,.95);gap:4px;padding:24px;padding-top:calc(26px + env(safe-area-inset-top,0px));z-index:12;overflow-y:auto;-webkit-overflow-scrolling:touch}
  #ranksX{position:absolute;top:calc(12px + env(safe-area-inset-top,0px));right:16px;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#cfe;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:50%;cursor:pointer;z-index:13}
  #ranksList{width:100%;max-width:360px;margin:6px 0}
  .rrow{display:flex;align-items:center;gap:13px;padding:10px 13px;margin:7px 0;border-radius:13px;background:rgba(255,255,255,.05);text-align:left}
  .rrow.now{background:rgba(124,246,255,.15);border:1px solid rgba(124,246,255,.55)}
  .rrow.locked{opacity:.4}
  .rrow.locked img{filter:grayscale(1) brightness(.75)}
  .rrow .rn{flex:1;font-weight:800;font-size:17px}
  .rrow .rp{font-size:12px;color:#8892b0;font-weight:700;text-align:right}
  /* 결과창 랭크 */
  #overRankNow{display:flex;align-items:center;justify-content:center;gap:10px;margin:4px 0 0}
  #overRankNow .obar{width:104px;height:6px;background:rgba(255,255,255,.13);border-radius:3px;overflow:hidden}
  #overRankNow .ofill{height:100%;background:linear-gradient(90deg,#7cf6ff,#5cffb0);border-radius:3px}
  .bprev{display:flex;gap:9px;justify-content:center;align-items:center;opacity:.5}"""))

# ── 랭크 카드 구조 ────────────────────────────────────────────────
S.append(("""  <div id="rankCard">
    <div id="rankTop"><span id="rankName">🥉 브론즈</span><span id="rankPts" style="font-size:13px;color:#8892b0">0</span></div>
    <div id="rankBar"><div id="rankFill"></div></div>
    <div id="rankSub">다음 랭크까지 –</div>
  </div>""",
"""  <div id="rankCard" role="button">
    <div id="rankHead">
      <span id="rankEmblemBox"></span>
      <div style="flex:1;min-width:0">
        <div id="rankTop"><span id="rankName">브론즈</span><span id="rankPts" style="font-size:13px;color:#8892b0">0</span></div>
        <div id="rankBar"><div id="rankFill"></div></div>
        <div id="rankSub">다음 랭크까지 –</div>
      </div>
    </div>
    <div id="rankMore">👑 랭크 7단계 전체 보기 ›</div>
  </div>"""))

# ── 랭크 전체 보기 화면 ───────────────────────────────────────────
S.append(("""<div id="shop" class="hidden">""",
"""<div id="ranks" class="hidden">
  <div id="ranksX" role="button" aria-label="닫기">✕</div>
  <h1 style="font-size:30px">👑 랭크</h1>
  <div class="sub" id="ranksMine">누적 점수로 올라갑니다</div>
  <div id="ranksList"></div>
  <button class="btn" id="ranksClose" style="margin-top:4px">닫기</button>
</div>

<div id="shop" class="hidden">"""))

# ── 결과창 랭크 줄 ────────────────────────────────────────────────
S.append(("""  <div class="sub" id="overRankUp" style="font-weight:800;min-height:0"></div>""",
"""  <div id="overRankNow"></div>
  <div class="sub" id="overRankUp" style="font-weight:800;min-height:0"></div>"""))

# ── renderRankCard: 큰 엠블럼 + 이름 분리 ─────────────────────────
S.append(("""  const nm=$('rankName'); if(nm){ nm.innerHTML=rankArt(i,34)+' <span style="vertical-align:middle">'+R.n+'</span>'; nm.style.color=R.c; }""",
"""  const eb=$('rankEmblemBox'); if(eb) eb.innerHTML=rankArt(i,60);
  const nm=$('rankName'); if(nm){ nm.textContent=R.n; nm.style.color=R.c; }"""))

# ── 랭크 목록 / 결과창 랭크 렌더 ──────────────────────────────────
S.append(("""function addTotal(inc){""",
"""function renderRanks(){
  const box=$('ranksList'); if(!box) return;
  const cur=rankIdx(total);
  const mine=$('ranksMine');
  if(mine) mine.innerHTML='내 누적 <b style="color:#ffd34d">'+total.toLocaleString()+'</b>점 · 현재 <b style="color:'+RANKS[cur].c+'">'+RANKS[cur].n+'</b>';
  box.innerHTML=RANKS.map((R,i)=>{
    const got=i<=cur, now=i===cur;
    const need= got ? (now?'현재 랭크':'달성') : ('누적 '+R.at.toLocaleString()+'점<br><span style="color:#ffd34d">'+(R.at-total).toLocaleString()+'점 남음</span>');
    return '<div class="rrow'+(now?' now':'')+(got?'':' locked')+'">'+art(R.f,R.i,56)
      +'<span class="rn" style="color:'+(got?R.c:'#8892b0')+'">'+R.n+'</span><span class="rp">'+need+'</span></div>';
  }).join('');
}
function openRanks(){ $('ranks').classList.remove('hidden'); renderRanks(); }
function closeRanks(){ $('ranks').classList.add('hidden'); }
function renderOverRank(){
  const el=$('overRankNow'); if(!el) return;
  const i=rankIdx(total), R=RANKS[i], N=RANKS[i+1];
  const p=N? Math.max(0,Math.min(100,(total-R.at)/(N.at-R.at)*100)) : 100;
  el.innerHTML=art(R.f,R.i,40)+'<span style="font-weight:800;color:'+R.c+'">'+R.n+'</span>'
    +'<span class="obar"><span class="ofill" style="display:block;width:'+p.toFixed(0)+'%"></span></span>'
    +'<span style="font-size:11.5px;color:#8892b0;font-weight:700">'+(N?(N.n+'까지 '+(N.at-total).toLocaleString()):'최고 랭크')+'</span>';
}
function addTotal(inc){"""))

# ── 결과창에서 호출 ───────────────────────────────────────────────
S.append(("""  renderRankCard(); renderDaily(); renderBoostRow();""",
"""  renderRankCard(); renderOverRank(); renderDaily(); renderBoostRow();"""))

# ── 부스터: 미보유여도 아이콘 미리보기 ────────────────────────────
S.append(("""  if(!have.length){ box.innerHTML='<div class="sub" style="font-size:12px;opacity:.5">⚡ 부스터는 상점에서 살 수 있어요</div>'; return; }""",
"""  if(!have.length){
    box.innerHTML='<div class="bprev">'+BOOSTS.map(B=>art('boost_'+B.id,B.i,30)).join('')
      +'</div><div class="sub" style="font-size:12px;opacity:.6;width:100%">⚡ 부스터 4종 · 상점에서 코인으로 구매</div>';
    return; }"""))

# ── 버튼 연결 ─────────────────────────────────────────────────────
S.append(("""$('shopBtn').onclick=()=>openShop();""",
"""$('shopBtn').onclick=()=>openShop();
$('rankCard').onclick=()=>{ sfx('ui_tap'); openRanks(); };
$('ranksClose').onclick=()=>closeRanks();
$('ranksX').onclick=()=>closeRanks();"""))

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
