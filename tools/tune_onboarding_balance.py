# -*- coding: utf-8 -*-
"""신규 유저 첫 경험 + 보상 밸런스 튜닝 (1회성 패치, v4.0)

출시 전 재미 검증에서 '버그는 아니지만 재미를 깎는' 네 가지가 수치로 나왔다.
치명 버그(v3.9)와 달리 전부 순수 튜닝이다. 라운드 타입 구성·연출·LB_HIDE 는 건드리지 않는다.


① 첫 화면 설명이 길다 — 7항목 370자
   신규 설치 때 뜨는 #help 가 ①~⑦ 7줄이다. 그중 ④롤링·⑤선택형·⑥체인은 각각
   4·6·6연속은 가야 처음 등장하는데, 아직 본 적도 없는 걸 먼저 읽힌다.
   게임 안에는 이미 첫 2라운드 슬로모 + "⚡ 다음이 목표! 탭!" 텔레그래프가 있어서
   ①②③만 알면 바로 플레이가 된다.
   → 첫 실행은 '핵심 3줄'만, 전문 7줄은 홈의 📖 방법 버튼에 그대로 남긴다.
     두 벌을 따로 적어 어긋나는 걸 막으려고, 전문은 기존 HTML 에서 그대로 뽑아
     HELP_FULL 배열로 옮긴다(문구는 한 글자도 안 바뀐다).


② 점수가 곱으로 폭발한다
   hitOK() 의 gain = base × mult × link × modScore × (score2?2:1) 에서
   콤보 배수(최대 ×5~8)·체인 링크(1+0.5*chainIdx, 최대 ×2)·강화(modScore 최대 ×3.71)가
   전부 '곱'이라 셋이 겹치면 한 번의 성공이 수십 배가 된다.

   실측(시드 1~10 중앙값, 자동 플레이):
     배수 없이 20연속    852점     ← 초보
     숙련 40연속      30,656점     ← 36배
     숙련 60연속     114,448점     ← 134배
   랭킹이 실력보다 '그 판에 어떤 강화가 떴나'로 갈린다.

   → 곱을 두 군데에서 덧셈으로 바꾼다. 초보 구간(배수 1·체인 없음·강화 없음)은
     값이 1 이라 한 점도 안 변하고, 겹칠수록 눌린다.
     A. 체인 링크: mult × link  →  (mult + 0.5*chainIdx)
        mult 5 · 3번째 고리면 5×2=10 이던 것이 5+1=6.
     B. 강화 배율: 곱 누적 → 덧셈 누적 (카드 설명도 '×1.3' → '+20%' 로 정직하게 고침)
        가속 ×1.3^5=3.71 → 1+0.20*5=2.00
          (가속은 점수를 노리는 플레이어가 무조건 1순위로 집는 카드라 사실상 항상 5중첩이
           된다. 여기가 제일 크게 눌려야 '어떤 카드가 떴나'로 갈리는 운 요소도 같이 준다.
           +30% 로 한 번 재 보니 18연속이 7%밖에 안 줄어서 +20% 로 내렸다.)
        황금 ×1.35^2=1.82 → 1+0.35*2=1.70
        행운 ×1.6^2=2.56 → 1+0.60*2=2.20
        체인특화 ×1.35^3=2.46 → 1+0.35*3=2.05
        (감속 ×0.88^3=0.68 → 1-0.12*3=0.64, 해독 ×0.92 → -0.08 — 마이너스 카드도
         같은 방식으로 맞춰야 '곱과 덧셈이 섞여 감속이 상대적으로 유리해지는' 일이 없다)


③ 코인이 한 판에 너무 많다
   addCoins 가 ceil(gain/8) 이라 ②의 점수 폭발이 코인으로 그대로 전이된다.
   실측 한 판 코인(중앙값): 초보 20연속 116 / 숙련 18연속 523 / 숙련 40연속 3,851.
   테마가 150~4,000 인데(전부 8,950) 잘한 한 판이면 상점이 통째로 열린다.
   → 판당 코인 상한 250. 초보 한 판이 30~135 라 상한에 닿지 않고 상단만 눌린다.
     상한은 '판' 단위다 — 죽고 생명·부활로 이어가면 commitCoins() 가 runCoins 를
     runEarned 로 옮기고 0 으로 비우므로, runCoins 만 보면 부활 횟수만큼 상한이
     되살아난다. 그래서 runEarned + runCoins 합계로 건다.
     상한에 닿으면 결과창에 '판당 상한'이라고 적는다(조용히 깎으면 버그로 보인다).
   승급 보너스((랭크+1)×250)는 그대로 둔다 — 깊이에 대한 보상은 거기서 준다.


④ 일일 미션 '🌟 골든 라운드 1회'가 첫날 유저에게 거의 불가능하다
   makeRule() 에서 골든은 hits>=6 && hits%10===0 이라 10연속을 해야 한 번 나온다.
   MDEF 의 goals 가 [1,2,3] 이라 숫자를 더 낮출 수도 없다.
   → 브론즈(누적 3,000점 미만)에게만 주기를 6연속으로 당긴다.
     ⚠️ 일일 챌린지는 제외한다. 주기가 rankIdx(total) 에 걸리면 사람마다 라운드
     전개가 달라져서 '같은 날이면 모두 같은 판'이라는 전제가 깨진다.
     실버 이상은 10연속 그대로라 검증된 라운드 분포도 안 변한다.
"""
import io, os, re, sys, json

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()


def sub(a, b):
    """정확히 한 번 나올 때만 치환한다."""
    global s
    n = s.count(a)
    if n != 1:
        print('matched %d, expected 1: %r' % (n, a[:90]))
        sys.exit(1)
    s = s.replace(a, b)


# ─────────────────────────────────────────────────────────────────
# ① 첫 화면 설명 — 핵심 3줄 / 전문은 '방법' 버튼
# ─────────────────────────────────────────────────────────────────
H0 = s.index('<div id="help" class="hidden">')
H1 = s.index('  <button class="btn" id="helpClose"', H0)
rows = re.findall(r'<div class="hrow">(.*?)</div>\n', s[H0:H1])
if len(rows) != 7:
    print('help rows: got %d, expected 7' % len(rows))
    sys.exit(1)

s = s[:H0] + (
    '<div id="help" class="hidden">\n'
    '  <h1><img class="art" src="img/number/ui/ui_help.webp" alt="" width="24" height="24"'
    ' data-fb="\U0001F4D6" onerror="uiFB(this)"/> <span id="helpTitle">게임 방법</span></h1>\n'
    '  <div id="helpRows"></div>\n'
    '  <div id="helpMore" class="hidden">나머지 규칙(⚡롤링 · 🔢선택형 · 🔗체인)은 처음 나올 때'
    ' 화면이 알려줘요. 전체 설명은 홈의 <b>📖 방법</b>에 있어요.</div>\n'
) + s[H1:]

# .hrow 가 #help 직계에서 #helpRows 안으로 한 겹 들어갔으니 간격·정렬을 거기로 옮긴다
sub("""  #help .hrow{font-size:15.5px;line-height:1.65;max-width:330px;color:#cfe}""",
    """  #help .hrow{font-size:15.5px;line-height:1.65;max-width:330px;color:#cfe}
  #help #helpRows{display:flex;flex-direction:column;align-items:center;gap:8px}
  #help #helpMore{font-size:12.5px;line-height:1.55;max-width:330px;color:#8892b0;text-align:center}""")

HELP_CORE = [
    '① 숫자가 <b>일정한 규칙</b>으로 올라갑니다. 아래 수열(<b>3 → 6 → 9</b>)에서 규칙을 읽으세요.',
    '② 위의 <b>목표 숫자</b>와 <b>똑같아지는 순간</b> 아무 곳이나 탭!',
    '③ 빠를수록 <b style="color:#ffe14d">PERFECT</b> — 연속하면 점수 배수가 올라갑니다.',
]

helpjs = (
    "// \U0001F4D6 게임 방법 — 첫 실행은 '핵심 3줄'만.\n"
    "// 롤링(4연속)·선택형(6)·체인(6)은 아직 본 적도 없는 규칙이라 먼저 읽히면 그냥 닫는다.\n"
    "// 전문 7줄은 홈의 '방법' 버튼에서 그대로 볼 수 있다.\n"
    "const HELP_CORE=" + json.dumps(HELP_CORE, ensure_ascii=False) + ";\n"
    "const HELP_FULL=" + json.dumps(rows, ensure_ascii=False) + ";\n"
    "function openHelp(full){\n"
    "  $('helpTitle').textContent = full?'게임 방법':'30초면 끝';\n"
    "  $('helpRows').innerHTML = (full?HELP_FULL:HELP_CORE).map(t=>'<div class=\"hrow\">'+t+'</div>').join('');\n"
    "  $('helpMore').classList.toggle('hidden', !!full);\n"
    "  $('helpClose').textContent = full?'닫기':'알겠어요, 시작!';\n"
    "  $('help').classList.remove('hidden');\n"
    "}\n"
    "$('helpBtn').onclick=()=>openHelp(true);\n"
)
sub("""$('helpBtn').onclick=()=>{ $('help').classList.remove('hidden'); };\n""", helpjs)

sub("""try{ if(!localStorage.getItem('num_seen_help')) $('help').classList.remove('hidden'); }catch(e){}""",
    """try{ if(!localStorage.getItem('num_seen_help')) openHelp(false); }catch(e){}""")


# ─────────────────────────────────────────────────────────────────
# ② 점수 — 곱을 덧셈으로
# ─────────────────────────────────────────────────────────────────
# A. 체인 링크를 배수에 더한다 (mult × link → mult + link)
sub("""  const link = chainAll.length>1 ? (1 + 0.5*chainIdx) : 1;        // \U0001F517 체인 뒷 링크일수록 배점↑""",
    """  const link = chainAll.length>1 ? 0.5*chainIdx : 0;              // \U0001F517 체인 뒷 링크 — 곱이 아니라 콤보 배수에 더한다(겹칠 때 폭주 억제)""")
sub("""  const gain=Math.round(base*mult*link*modScore*(runBoost.score2?2:1));""",
    """  const gain=Math.round(base*(mult+link)*modScore*(runBoost.score2?2:1));""")

# B. 강화 배율을 덧셈 누적으로 (카드 설명도 실제와 맞게 고친다)
sub("""  {id:'speed',  i:'⚡', n:'가속',     d:'속도 +14% · 점수 ×1.3',        max:5, a:()=>{ modSpeed*=0.86; modScore*=1.3; }},""",
    """  {id:'speed',  i:'⚡', n:'가속',     d:'속도 +14% · 점수 +20%',        max:5, a:()=>{ modSpeed*=0.86; modScore+=0.20; }},""")
sub("""  {id:'slow',   i:'\U0001F422', n:'감속',     d:'속도 -15% · 점수 ×0.88',       max:3, a:()=>{ modSpeed*=1.15; modScore*=0.88; }},""",
    """  {id:'slow',   i:'\U0001F422', n:'감속',     d:'속도 -15% · 점수 -12%',        max:3, a:()=>{ modSpeed*=1.15; modScore-=0.12; }},""")
sub("""  {id:'chain',  i:'\U0001F517', n:'체인 특화', d:'체인 등장↑ · 완성 보너스 ×1.5', max:3, a:()=>{ modChain+=0.12; modChainBonus*=1.35; }},""",
    """  {id:'chain',  i:'\U0001F517', n:'체인 특화', d:'체인 등장↑ · 완성 보너스 +35%', max:3, a:()=>{ modChain+=0.12; modChainBonus+=0.35; }},""")
sub("""  {id:'golden', i:'\U0001F31F', n:'황금',     d:'골든 라운드 2배 자주 · 골든 ×1.5', max:2, a:()=>{ modGolden++; modGoldenScore*=1.35; }},""",
    """  {id:'golden', i:'\U0001F31F', n:'황금',     d:'골든 라운드 2배 자주 · 골든 +35%', max:2, a:()=>{ modGolden++; modGoldenScore+=0.35; }},""")
sub("""  {id:'read',   i:'\U0001F9EE', n:'해독',     d:'수열을 6개까지 표시 · 점수 ×0.92', max:1, a:()=>{ modSeq=6; modScore*=0.92; }},""",
    """  {id:'read',   i:'\U0001F9EE', n:'해독',     d:'수열을 6개까지 표시 · 점수 -8%', max:1, a:()=>{ modSeq=6; modScore-=0.08; }},""")
sub("""  {id:'lucky',  i:'\U0001F3B2', n:'행운',     d:'롤링 2배 자주 · 롤링 점수 ×1.6', max:2, a:()=>{ modRoll+=0.10; modRollScore*=1.6; }},""",
    """  {id:'lucky',  i:'\U0001F3B2', n:'행운',     d:'롤링 2배 자주 · 롤링 점수 +60%', max:2, a:()=>{ modRoll+=0.10; modRollScore+=0.60; }},""")


# ─────────────────────────────────────────────────────────────────
# ③ 코인 — 판당 상한
# ─────────────────────────────────────────────────────────────────
sub("""function addCoins(pts){ runCoins += Math.max(1, Math.ceil(pts/8)) * (runBoost&&runBoost.coin2?2:1); }""",
    """// \U0001F4B0 판당 코인 상한 — 점수가 곱으로 커지면 코인도 같이 터져서 잘한 한 판이 상점을 통째로 열었다.
// 초보 한 판이 30~135 코인이라 250 은 초보에겐 닿지 않고 상단만 누른다.
// 부활로 이어간 판도 '한 판'이다 — commitCoins() 가 runCoins 를 비우므로 runEarned 와 합쳐서 건다.
const RUN_COIN_CAP=250;
function runCoinCap(){ return RUN_COIN_CAP * (runBoost&&runBoost.coin2?2:1); }
function addCoins(pts){ const m=(runBoost&&runBoost.coin2?2:1);
  runCoins = Math.max(0, Math.min(runCoinCap()-runEarned, runCoins + Math.max(1, Math.ceil(pts/8))*m)); }""")

sub("""  commitCoins(); $('overCoin').innerHTML = uic('coin','\U0001F4B0',16)+' <b style="color:#ffd34d">+'+runEarned+'</b> <span style="opacity:.6">(보유 '+coins+')</span>';""",
    """  commitCoins(); $('overCoin').innerHTML = uic('coin','\U0001F4B0',16)+' <b style="color:#ffd34d">+'+runEarned+'</b>'
    + (runEarned>=runCoinCap() ? ' <span style="opacity:.55;font-size:11px">판당 상한</span>' : '')
    + ' <span style="opacity:.6">(보유 '+coins+')</span>';""")


# ─────────────────────────────────────────────────────────────────
# ④ 골든 주기 — 브론즈만 6연속 (일일 챌린지 제외)
# ─────────────────────────────────────────────────────────────────
sub("""  const gEvery=modGolden?5:10;                                  // \U0001F31F 황금 강화를 먹으면 5연속마다""",
    """  // \U0001F31F 골든 주기 — 10연속은 첫날 유저가 거의 못 봐서 일일 미션 '골든 1회'가 사실상 불가능했다.
  // 브론즈(누적 3,000점 미만)만 6연속으로 당긴다. 일일 챌린지는 모두 같은 전개여야 하므로 제외.
  const gEvery=modGolden?5:((!dailyMode && rankIdx(total)<1)?6:10);""")


# ─────────────────────────────────────────────────────────────────
# 버전 문자열
# ─────────────────────────────────────────────────────────────────
sub("""<div id="changelog">\U0001F195 <b id="clVer">v3.9</b> · <span id="clNote"><b>신기록 결과창</b>과 <b>생명 부활 후 숫자 겹침</b> 수정 · 이제 끝까지 제대로 보여요</span></div>""",
    """<div id="changelog">\U0001F195 <b id="clVer">v4.0</b> · <span id="clNote">첫 설명은 <b>핵심 3줄</b>로 · 점수·코인 <b>밸런스 조정</b> · 🌟골든이 더 자주</span></div>""")
sub("""<div id="ver">v3.9 · 결과창·숫자 겹침</div>""",
    """<div id="ver">v4.0 · 첫 설명·점수/코인 밸런스</div>""")

if 'const ADS_ENABLED=false' not in s:
    print('ADS_ENABLED=false 가 사라졌다 — 중단')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('tune_onboarding_balance: ok')
