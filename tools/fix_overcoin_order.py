# -*- coding: utf-8 -*-
"""결과창의 '보유 코인'이 승급 보너스 반영 전 숫자로 찍히던 것을 고친다. (1회성 패치)

증상: 결과창에 「💰 +250 판당 상한 (보유 520)」 과 「🎉 실버 승급! 💰+500」 이
  나란히 떠 있는데, 실제 보유는 1,020 이다. 더할 숫자가 바로 아랫줄에 보이는데
  안 더해져 보인다.

원인: die() 안에서 그리는 순서가 뒤집혀 있다.

  1424:  commitCoins(); $('overCoin').innerHTML = ... '(보유 '+coins+')';   <- 먼저 그리고
  1428:  const up=addTotal(score-totalCommitted);                            <- 여기서 coins 가 오른다
           (addTotal 안: if(a>b){ const rw=(a+1)*250; coins+=rw; saveCoins(); })

  즉 '보유'를 찍은 다음에 승급 보너스가 들어간다. saveCoins() 가 상단 HUD 는
  다시 그리지만 결과창의 저 문구는 이미 문자열로 박혀 있어서 안 바뀐다.

  미션 보상(mBump)·일일 전체완료 보너스(mCheckAll)는 플레이 중에 들어가므로
  이 순서 문제와 무관하다. die() 이후 coins 를 올리는 곳은 addTotal 뿐이다.

고치는 법: addTotal() 을 먼저 돌리고 그 뒤에 overCoin 을 그린다.
  '+N' 은 이번 판 획득분(runEarned) 그대로 두고 '보유'만 최신으로 맞춘다 —
  승급 보너스는 바로 아랫줄에 따로 보이므로 합쳐 버리면 오히려 출처가 흐려진다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

S.append(("""  commitCoins(); $('overCoin').innerHTML = uic('coin','\U0001F4B0',16)+' <b style="color:#ffd34d">+'+runEarned+'</b>'
    + (runEarned>=runCoinCap() ? ' <span style="opacity:.55;font-size:11px">판당 상한</span>' : '')
    + ' <span style="opacity:.6">(보유 '+coins+')</span>';
  // \U0001F3C5 랭크: 이번 판 점수를 누적(부활로 이어간 판은 증가분만)
  const up=addTotal(score-totalCommitted); totalCommitted=score;""",
"""  commitCoins();
  // \U0001F3C5 랭크: 이번 판 점수를 누적(부활로 이어간 판은 증가분만)
  // ⚠️ overCoin 보다 먼저 돌려야 한다 — addTotal() 이 승급 보너스를 coins 에 더하는데,
  //    '보유'를 그 앞에서 그리면 바로 아랫줄의 '승급! +500' 이 안 더해진 숫자가 찍힌다.
  const up=addTotal(score-totalCommitted); totalCommitted=score;
  $('overCoin').innerHTML = uic('coin','\U0001F4B0',16)+' <b style="color:#ffd34d">+'+runEarned+'</b>'
    + (runEarned>=runCoinCap() ? ' <span style="opacity:.55;font-size:11px">판당 상한</span>' : '')
    + ' <span style="opacity:.6">(보유 '+coins+')</span>';"""))

S.append(("""  <div id="changelog">🆕 <b id="clVer">v4.0</b>""",
          """  <div id="changelog">🆕 <b id="clVer">v4.1</b>"""))
S.append(("""<div id="ver">v4.0 · 첫 설명·점수/코인 밸런스</div>""",
          """<div id="ver">v4.1 · 결과창 보유 코인</div>"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:72]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('matched %d, expected 1: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('overCoin order: %d patches' % len(S))
