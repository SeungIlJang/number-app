# -*- coding: utf-8 -*-
"""18~20연속 구간 점수를 더 누른다 (1회성 패치, v4.1)

v4.0 에서 곱을 덧셈으로 바꿨더니 깊은 판은 많이 눌렸는데(60연속 −41%)
18~20연속 구간은 10%밖에 안 줄었다. 그 구간을 다시 재 보니 이유가 둘이었다.

  (측정: 자동 플레이 시드 1~10 중앙값, 숙련 18연속 3,732점)

  1) 콤보 배수가 너무 빨리 천장에 닿는다.
     PERFECT 한 번마다 +1 이라 4연속이면 벌써 ×5 다. 그 뒤로는 모든 성공이
     ×5 로 깔리니, 18~20연속 점수는 사실상 '×5 × 깊이' 하나로만 결정됐다.
     판이 길어져도 배수에서 더 가져갈 게 없어서 '어디까지 갔나'보다
     '그 판에 뭐가 떴나'가 순위를 가른다.

  2) 골든 라운드가 기본점을 2배 하는데, 그게 다시 배수와 곱해진다.
     seed 1 의 18연속 한 판을 뜯어보니 골든 3번이 전체 점수의 43% 였다.
     기본점 ×2 가 배수 ×5 와 곱해지면 한 번의 성공이 기본점의 10배가 된다.
     초보(배수 1)에게는 ×2 밖에 안 되는데 숙련자에게만 ×10 으로 커지는,
     딱 '잘하는 사람만 더 터지는' 구조다.

고치는 법 — 둘 다 '천장'이 아니라 '도달 속도'와 '합산 방식'을 바꾼다.
광고된 문구(최대 ×5)는 그대로 지킨다.

  A. 콤보 배수를 PERFECT 2연속마다 +1 로 바꾼다.
     ×5 는 4번째가 아니라 8번째 PERFECT 에서 나온다. 상한은 그대로 ×5 라
     도움말 ③ '최대 ×5' 도 손댈 필요가 없고, ×5 가 '길게 간 판의 보상'이 된다.
     PERFECT 를 아예 못 내는 초보는 배수가 늘 1 이라 한 점도 안 변한다.

  B. 골든을 '기본점 ×2' 에서 '배수 +2' 로 바꾼다. (체인 링크와 같은 방식)
     숙련(배수 5): ×2 → ×1.4 로 눌리고
     초보(배수 1): ×2 → ×3 으로 오히려 커진다.
     브론즈는 v4.0 에서 골든을 6연속마다 보게 됐으니(④) 초보 쪽은 같이 좋아진다.
     황금 강화 카드도 곱(+35%)에서 '배수 +1'로 바꾼다 — 골든에서 최대 +4.
     카드·배너 문구도 실제와 맞게 고친다.

  ⚠️ 체인 완성 보너스(cb)는 base 로 계산하는데, base 에서 골든 ×2 가 빠지므로
     골든+체인이 겹친 판의 보너스도 같이 내려간다. 의도한 것이다 —
     그게 바로 '곱이 세 개 겹치던' 자리다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()


def sub(a, b):
    global s
    n = s.count(a)
    if n != 1:
        # 콘솔이 cp949 라 한글/이모지를 그대로 찍으면 죽는다 — ascii 로 이스케이프해서 보여준다
        print('matched %d, expected 1: %s' % (n, ascii(a[:90])))
        sys.exit(1)
    s = s.replace(a, b)


# ─────────────────────────────────────────────────────────────────
# A. 콤보 배수 — PERFECT 2연속마다 +1
# ─────────────────────────────────────────────────────────────────
sub("""let mult=1, targetShownAt=0, inGap=false;   // 콤보 배수 · 목표 표시 시각 · 라운드 전환 텀""",
    """let mult=1, targetShownAt=0, inGap=false;   // 콤보 배수 · 목표 표시 시각 · 라운드 전환 텀
// \U0001F525 배수를 한 칸 올리는 데 필요한 PERFECT 연속 횟수.
// 1 이면 4연속 만에 ×5 에 닿아서 그 뒤 모든 점수가 ×5 로 깔린다(=판이 길어져도
// 배수에서 더 가져갈 게 없다). 2 로 두면 ×5 는 8번째 PERFECT 의 보상이 되고,
// 상한은 ×5 그대로라 도움말 문구도 안 바뀐다. PERFECT 가 없는 초보는 영향 없음.
const MULT_STEP=2; let pstreak=0;""")

sub("""  if(grade==='PERFECT'){ mult=Math.min(modMultCap, mult+1); mprog('perfect',1); } else mult=1;   // 퍼펙트 연속 → 배수↑, 굿이면 리셋""",
    """  if(grade==='PERFECT'){ pstreak++; if(pstreak%MULT_STEP===0) mult=Math.min(modMultCap, mult+1); mprog('perfect',1); }
  else { pstreak=0; mult=1; }   // 퍼펙트 MULT_STEP 연속마다 배수↑, 굿이면 둘 다 리셋""")

sub("""  score=0; hits=0; hearts=1+(runBoost.life?2:0); mult=1; runCoins=0; runEarned=0; totalCommitted=0; inGap=false; showMult(); slowEndShown=false; reviveCount=0; adPlaying=false;""",
    """  score=0; hits=0; hearts=1+(runBoost.life?2:0); mult=1; pstreak=0; runCoins=0; runEarned=0; totalCommitted=0; inGap=false; showMult(); slowEndShown=false; reviveCount=0; adPlaying=false;""")

sub("""  mult=1; showMult();   // 콤보 배수 리셋""",
    """  mult=1; pstreak=0; showMult();   // 콤보 배수 리셋(부활로 이어가도 처음부터)""")


# ─────────────────────────────────────────────────────────────────
# B. 골든 — '기본점 ×2' 를 '배수 +2' 로
# ─────────────────────────────────────────────────────────────────
sub("""    modGolden=0, modGoldenScore=1, modSeq=4, modRoll=0, modRollScore=1, heartMax=3,""",
    """    modGolden=0, modGoldenBonus=0, modSeq=4, modRoll=0, modRollScore=1, heartMax=3,""")
sub("""  modGolden=0; modGoldenScore=1; modSeq=4; modRoll=0; modRollScore=1; heartMax=3;""",
    """  modGolden=0; modGoldenBonus=0; modSeq=4; modRoll=0; modRollScore=1; heartMax=3;""")
sub("""  {id:'golden', i:'\U0001F31F', n:'황금',     d:'골든 라운드 2배 자주 · 골든 +35%', max:2, a:()=>{ modGolden++; modGoldenScore+=0.35; }},""",
    """  {id:'golden', i:'\U0001F31F', n:'황금',     d:'골든 라운드 2배 자주 · 골든 배수 +1', max:2, a:()=>{ modGolden++; modGoldenBonus+=1; }},""")

sub("""  const base=((wasRoll?25*modRollScore:10) + (hits-1)*2) * (wasGolden?2*modGoldenScore:1);   // \U0001F31F 골든 라운드 점수 ×2
  const gain=Math.round(base*(mult+link)*modScore*(runBoost.score2?2:1));""",
    """  const gb = wasGolden ? (2 + modGoldenBonus) : 0;   // \U0001F31F 골든 — 기본점을 2배 하지 않고 배수에 +2 (체인 링크와 같은 방식)
  const base=(wasRoll?25*modRollScore:10) + (hits-1)*2;
  const gain=Math.round(base*(mult+link+gb)*modScore*(runBoost.score2?2:1));""")

sub("""    if(rule.golden){ banner(''+uic('golden','\U0001F31F',22)+' 골든 라운드! 점수 ×2','#ffd34d');""",
    """    if(rule.golden){ banner(''+uic('golden','\U0001F31F',22)+' 골든 라운드! 배수 +2','#ffd34d');""")


# ─────────────────────────────────────────────────────────────────
# 버전 문자열
# ─────────────────────────────────────────────────────────────────
# v4.1(결과창 '보유 코인' 수정)은 다른 세션이 먼저 올렸다 — 그 위에 v4.2 로 얹는다
sub("""<b id="clVer">v4.1</b> · <span id="clNote">첫 설명은 <b>핵심 3줄</b>로 · 점수·코인 <b>밸런스 조정</b> · \U0001F31F골든이 더 자주</span>""",
    """<b id="clVer">v4.2</b> · <span id="clNote">콤보 배수는 <b>길게 갈수록</b> 올라가요 · \U0001F31F골든은 <b>배수 +2</b>로</span>""")
sub("""<div id="ver">v4.1 · 결과창 보유 코인</div>""",
    """<div id="ver">v4.2 · 콤보 배수·골든 재조정</div>""")

if 'const ADS_ENABLED=false' not in s:
    print('ADS_ENABLED=false 가 사라졌다 — 중단')
    sys.exit(1)
if 'modGoldenScore' in s:
    print('modGoldenScore 잔재가 남았다 — 중단')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('tune_combo_golden: ok')
