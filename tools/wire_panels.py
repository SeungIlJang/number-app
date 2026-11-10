# -*- coding: utf-8 -*-
"""상점·랭킹·랭크·게임오버 화면 다듬기 (1회성 패치)

문제 1 — 네 패널 모두 반투명이라(.92~.95) 뒤 화면이 유령처럼 비친다.
  전체를 덮는 패널인데 홈 화면의 금색 글자와 게임 화면의 큰 숫자가 겹쳐 보인다.
  일일 챌린지 화면은 지난 리디자인 때 불투명으로 바꿔서 이 문제가 없다. 같은 처방을 쓴다.

문제 2 — 블록마다 폭이 제각각이다(320 / 340 / 360). 일일 챌린지의 352로 통일한다.

문제 3 — 게임오버 화면에 위계가 없다. 같은 무게의 한 줄짜리가 일곱 개 쌓여 있고,
  정작 제일 궁금한 '점수'가 세 번째 줄에 작게 박혀 있다. 점수를 카드 안에서 크게 키운다.

문제 4 — ✕ 와 '닫기'가 같은 무게로 경쟁한다. 닫기는 보조 스타일로 내린다.
  (없애지는 않는다 — 한 손으로 쓸 때 우상단 ✕ 는 멀다.)
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

W = 'min(92vw,352px)'

# ── 1. 불투명 배경 ────────────────────────────────────────────────
S.append(("""  #over,#start,#lb{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(8,10,22,.92);gap:10px;padding:24px;text-align:center;z-index:10}""",
"""  #over,#start,#lb{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(8,10,22,.92);gap:10px;padding:24px;text-align:center;z-index:10}
  /* 전체를 덮는 패널은 불투명해야 한다 — 반투명이면 뒤 화면 글자가 겹쳐 읽힌다.
     일일 챌린지 화면과 같은 처리(배경 그라디언트 + 아주 옅은 플레이 배경 아트). */
  #over,#lb{background:linear-gradient(180deg,#0c1427 0%,#080b17 55%,#05070f 100%)}
  #over::before,#lb::before,#shop::before,#ranks::before{content:'';position:fixed;inset:0;
    background:url(img/number/play/play_bg_normal.png) center/cover;opacity:.22;pointer-events:none}
  #over>*,#lb>*,#shop>*,#ranks>*{position:relative;z-index:1;flex:0 0 auto}
  #lb h1,#ranks h1{font-size:26px}
  /* ✕ 가 있으니 아래 '닫기'는 보조로 — 없애면 한 손으로 쓸 때 우상단이 멀다 */
  #shopClose,#lbClose,#ranksClose{background:transparent;box-shadow:none;border:1px solid rgba(255,255,255,.22);
    color:#cfe;padding:11px 26px;font-size:15px}
  #shopClose:active,#lbClose:active,#ranksClose:active{background:rgba(255,255,255,.1);transform:none}"""))

S.append(("""background:rgba(8,10,22,.94);gap:10px;padding:24px;padding-top:calc(28px + env(safe-area-inset-top,0px));text-align:center;z-index:12}""",
          """background:linear-gradient(180deg,#0c1427 0%,#080b17 55%,#05070f 100%);gap:10px;padding:24px;padding-top:calc(28px + env(safe-area-inset-top,0px));text-align:center;z-index:12}"""))

S.append(("""background:rgba(8,10,22,.95);gap:4px;padding:24px;""",
          """background:linear-gradient(180deg,#0c1427 0%,#080b17 55%,#05070f 100%);gap:4px;padding:24px;"""))

# ── 2. 폭 통일 352 ────────────────────────────────────────────────
S.append(("""  #shopList{width:100%;max-width:360px;""", """  #shopList{width:%s;""" % W))
S.append(("""  #lbList{width:100%;max-width:340px;""", """  #lbList{width:%s;""" % W))
S.append(("""  #ranksList{width:100%;max-width:360px;""", """  #ranksList{width:%s;""" % W))
S.append(("""  #overLbList{width:100%;max-width:320px;""", """  #overLbList{width:%s;""" % W))

S.append(("""  #dailyCard,#dailyTabs,#dailyStart,#dailyLbList,#dailyLog,#ranksList,#shopList{box-sizing:border-box}""",
          """  #dailyCard,#dailyTabs,#dailyStart,#dailyLbList,#dailyLog,#ranksList,#shopList,
  #lbList,#overLbList,#overCard,#overBtns,#reviveBtn,#shopTabs{box-sizing:border-box}"""))

# ── 3. 상점 탭을 세그먼트 컨트롤로 (일일 챌린지와 같은 모양) ──────
S.append(("""  #shopTabs{display:flex;gap:8px;margin:4px 0 2px}""",
"""  #shopTabs{display:flex;width:%s;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
    border-radius:14px;padding:4px;margin:10px 0 2px;gap:4px}
  #shopTabs .stab{flex:1;border:none;background:transparent;border-radius:10px;padding:9px 0;font-size:14px}
  #shopTabs .stab.on{background:#3a7bff;color:#fff;border-color:transparent}""" % W))

# ── 4. 게임오버 — 점수를 주인공으로 ───────────────────────────────
S.append(("""  #overRankNow{display:flex;align-items:center;justify-content:center;gap:8px;margin:4px 0 0;white-space:nowrap;max-width:100%}""",
"""  /* 점수가 제일 궁금한 정보인데 한 줄짜리들 사이에 묻혀 있었다. 카드로 묶어 키운다. */
  #overCard{width:%s;background:linear-gradient(160deg,rgba(124,246,255,.14),rgba(124,246,255,.03));
    border:1px solid rgba(124,246,255,.3);border-radius:20px;padding:14px 18px 12px;margin-top:4px;
    box-shadow:0 12px 34px rgba(0,0,0,.4)}
  #overCard .ok{font-size:11.5px;color:#8fa8c4;font-weight:800;letter-spacing:.5px}
  #overScore{font-size:46px;font-weight:900;line-height:1.05;margin:3px 0 1px;color:#ffd34d;
    text-shadow:0 0 24px rgba(255,211,77,.3)}
  #overRec{font-size:13px;min-height:18px;color:#9fb0cc;font-weight:700}
  #overMeta{display:flex;justify-content:center;align-items:center;gap:14px;flex-wrap:wrap;
    margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,.1);
    font-size:13px;color:#9fb0cc;font-weight:700}
  #overBtns{display:flex;gap:8px;width:%s;margin-top:8px}
  #overBtns .btn{flex:1;padding:13px 0;font-size:16px;margin-top:0}
  #reviveBtn{width:%s;font-size:16px;padding:14px 10px;margin-top:10px}
  #overRankNow{display:flex;align-items:center;justify-content:center;gap:8px;margin:10px 0 0;white-space:nowrap;max-width:100%%}""" % (W, W, W)))

# 마크업 재구성 — id 는 전부 유지(자바스크립트가 id 로만 쓴다)
S.append(("""  <div class="sub">점수 <b id="overScore">0</b> <span id="overRec"></span></div>
  <div class="sub" id="overCoin" style="min-height:20px"></div>
  <div id="overRankNow"></div>""",
"""  <div id="overCard">
    <div class="ok">점수</div>
    <div id="overScore">0</div>
    <div id="overRec"></div>
    <div id="overMeta">
      <span>최고 <b id="overBest" style="color:#cfe">0</b></span>
      <span id="overCoin"></span>
    </div>
    <div id="overRankNow"></div>
  </div>"""))

# 옛 '최고' 줄은 카드 안으로 옮겼으니 제거
S.append(("""  <div class="sub" style="opacity:.7">최고 <b id="overBest">0</b></div>\n""", ""))

S.append(("""  <div style="display:flex;gap:8px;margin-top:8px">
    <button class="btn" id="retryBtn" style="padding:13px 20px;font-size:18px">한 판 더</button>""",
"""  <div id="overBtns">
    <button class="btn" id="retryBtn">한 판 더</button>"""))

S.append(("""<button class="btn" id="homeBtn" style="padding:13px 18px;font-size:17px;background:#20263c;box-shadow:0 6px 0 #10131f">🏠 홈</button>""",
          """<button class="btn" id="homeBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f">🏠 홈</button>"""))

S.append(("""<button class="btn" id="shareBtn" style="padding:13px 18px;font-size:17px;background:#20263c;box-shadow:0 6px 0 #10131f">""",
          """<button class="btn" id="shareBtn" style="background:#20263c;box-shadow:0 6px 0 #10131f">"""))

# 상점 제목도 다른 패널과 같은 크기로
S.append(("""  <h1 style="font-size:32px">""", """  <h1 style="font-size:26px">"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:70]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('matched %d, expected 1: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('panel polish: %d patches' % len(S))
