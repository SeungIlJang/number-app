# -*- coding: utf-8 -*-
"""홈(시작) 화면 리디자인 (1회성 패치)

문제: 블록마다 폭이 달라 좌우가 들쭉날쭉하고, 시작 버튼과 일일 챌린지가
같은 무게로 경쟁했다. 최고 기록·코인이 설명 문장에 묻혀 있었다.
일일 챌린지 화면과 같은 규칙(폭 352 통일, 명확한 위계)으로 맞춘다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── CSS ───────────────────────────────────────────────────────────
S.append(("""  #start{overflow-y:auto;-webkit-overflow-scrolling:touch}""",
"""  #start{overflow-y:auto;-webkit-overflow-scrolling:touch;background:transparent;gap:0;padding-left:20px;padding-right:20px}
  /* 테마 배경이 비치도록 두고, 플레이 배경 아트를 아주 옅게 겹쳐 톤을 맞춘다 */
  #start::before{content:'';position:fixed;inset:0;background:url(img/number/play/play_bg_normal.png) center/cover;
    opacity:.2;pointer-events:none}
  #start::after{content:'';position:fixed;inset:0;background:linear-gradient(180deg,rgba(8,11,23,.72),rgba(5,7,15,.9));
    pointer-events:none}
  #start>*{position:relative;z-index:1;flex:0 0 auto}
  #startIcon{border-radius:18px;box-shadow:0 0 28px rgba(124,246,255,.16);margin-bottom:4px}
  #startTitle{font-size:31px;margin:0 0 12px}
  #startTag{font-size:13px;color:#9fb0cc;font-weight:700;margin-bottom:11px}
  #statRow{display:flex;gap:9px;width:min(92vw,352px);margin-top:10px}
  .hstat{flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
    border-radius:13px;padding:9px 13px;text-align:left}
  .hstat .sl{font-size:10.5px;color:#8fa8c4;font-weight:800;letter-spacing:.4px}
  .hstat .sv{font-size:19px;font-weight:900;margin-top:1px;color:#ffd34d}
  #startBtn{width:min(92vw,352px);margin-top:13px;padding:17px;font-size:21px}
  #dailyBtn{width:min(92vw,352px);margin-top:9px;padding:13px;font-size:16px;
    background:rgba(23,52,68,.85);box-shadow:none;border:1px solid rgba(124,246,255,.42);position:relative}
  #dailyBtn:active{background:rgba(33,74,96,.9);transform:none}
  #navRow{display:flex;gap:8px;width:min(92vw,352px);margin-top:9px}
  #navRow .btn{flex:1;padding:11px 0;font-size:14.5px;box-shadow:none;
    background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.12)}
  #navRow .btn:active{background:rgba(255,255,255,.14);transform:none}
  #navRow #shopBtn{background:rgba(56,44,12,.75);border-color:rgba(255,211,77,.32)}"""))

S.append(("""  #boostRow{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;margin-top:4px}""",
          """  #boostRow{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;align-items:center;
    width:min(92vw,352px);margin-top:11px}"""))

S.append(("""  #rankCard{width:min(92vw,330px);""",
          """  #rankCard{width:min(92vw,352px);"""))

S.append(("""  #dailyBox{width:min(92vw,330px);""",
          """  #dailyBox{width:min(92vw,352px);"""))

S.append(("""  #changelog{margin-top:18px;font-size:13px;""",
          """  #changelog{width:min(92vw,352px);margin-top:16px;font-size:12px;"""))

# ── HTML 재구성 ───────────────────────────────────────────────────
S.append(("""  <img src="img/number/ui/icon_512.png" alt="" width="72" height="72" style="flex-shrink:0;border-radius:18px;box-shadow:0 0 28px #7cf6ff20"/>
  <h1 style="font-size:34px">멈춰라 숫자</h1>""",
"""  <img id="startIcon" src="img/number/ui/icon_512.png" alt="" width="72" height="72"/>
  <h1 id="startTitle">멈춰라 숫자</h1>"""))

S.append(("""  <div class="sub" style="font-size:14px">수열을 읽고 <b style="color:#7cf6ff">목표 숫자</b>에서 <b>탭</b>! · <b style="color:#ffd34d">최고 <span id="best2">0</span></b> · 💰 <b id="coins" style="color:#ffd34d">0</b></div>
  <button class="btn" id="startBtn">시작</button>
  <div id="boostRow"></div>
  <div style="display:flex;gap:8px;margin-top:10px">
    <button class="btn" id="lbBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f;padding:10px 16px;font-size:15px">🏆 랭킹</button>
    <button class="btn" id="shopBtn" style="background:#2a2109;box-shadow:0 6px 0 #141005;padding:10px 16px;font-size:15px">🛒 상점</button>
    <button class="btn" id="helpBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f;padding:10px 16px;font-size:15px">📖 방법</button>
  </div>
  <div style="display:flex;margin-top:9px">
    <button class="btn" id="dailyBtn" style="position:relative;background:#1b3a4a;box-shadow:0 6px 0 #0d2029;padding:12px 26px;font-size:16px;border:1px solid rgba(124,246,255,.45)">📅 일일 챌린지<span id="dailyBadge" class="hidden">NEW</span></button>
  </div>""",
"""  <div id="statRow">
    <div class="hstat"><div class="sl">🏆 최고 기록</div><div class="sv"><span id="best2">0</span></div></div>
    <div class="hstat"><div class="sl">💰 보유 코인</div><div class="sv"><span id="coins">0</span></div></div>
  </div>
  <button class="btn" id="startBtn">시작</button>
  <button class="btn" id="dailyBtn">📅 일일 챌린지<span id="dailyBadge" class="hidden">NEW</span></button>
  <div id="navRow">
    <button class="btn" id="lbBtn">🏆 랭킹</button>
    <button class="btn" id="shopBtn">🛒 상점</button>
    <button class="btn" id="helpBtn">📖 방법</button>
  </div>
  <div id="boostRow"></div>"""))

# 설명 한 줄은 타이틀 바로 아래로
S.append(("""  <h1 id="startTitle">멈춰라 숫자</h1>""",
          """  <h1 id="startTitle">멈춰라 숫자</h1>
  <div id="startTag">수열을 읽고 <b style="color:#7cf6ff">목표 숫자</b>에서 <b>탭</b>!</div>"""))

# ── 부스터 줄도 폭에 맞춰 단정하게 ────────────────────────────────
S.append(("""    box.innerHTML='<div class="bprev">'+BOOSTS.map(B=>art('boost_'+B.id,B.i,30)).join('')
      +'</div><div class="sub" style="font-size:12px;opacity:.6;width:100%">⚡ 부스터 4종 · 상점에서 코인으로 구매</div>';""",
"""    box.innerHTML='<div class="bprev" style="gap:7px">'+BOOSTS.map(B=>art('boost_'+B.id,B.i,26)).join('')
      +'</div><div class="sub" style="font-size:11.5px;opacity:.55;width:100%;margin-top:3px">⚡ 부스터 4종 · 상점에서 코인으로 구매</div>';"""))

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
print('홈 리디자인 %d건 완료' % len(S))
