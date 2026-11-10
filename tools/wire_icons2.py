# -*- coding: utf-8 -*-
"""게임오버 화면에 남아 있던 코인 이모지 3곳을 마저 맞춘다. (1회성 패치)

#overCoin 은 아이콘인데 바로 밑 미션 토스트와 승급 줄은 이모지라 한 화면에서
같은 코인이 두 모양으로 보였다. 셋 다 innerHTML 로 들어가는 자리다.

주의: L868 한 줄에 mToast(HTML)와 floatText(순수 텍스트)가 같이 있다.
floatText 쪽은 건드리지 않는다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
COIN = '\U0001F4B0'

S = [
    # 일일 미션 전부 완료 토스트
    ("""mToast.push('\U0001F389 일일 미션 전부 완료! %s+'+DAILY_BONUS);""" % COIN,
     """mToast.push('\U0001F389 일일 미션 전부 완료! '+uic('coin','%s',13)+'+'+DAILY_BONUS);""" % COIN),
    # 미션 하나 완료 토스트 (같은 줄의 floatText 는 그대로 둔다)
    ("""mToast.push('✅ 미션 완료 · '+MBY[id].t(m.goal)+' %s+'+MBY[id].rw);""" % COIN,
     """mToast.push('✅ 미션 완료 · '+MBY[id].t(m.goal)+' '+uic('coin','%s',13)+'+'+MBY[id].rw);""" % COIN),
    # 랭크 승급 줄
    ("""' 승급! %s+'+up.rw+'</span></span>'""" % COIN,
     """' 승급! '+uic('coin','%s',14)+'+'+up.rw+'</span></span>'""" % COIN),
]

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
print('game-over coin icons: %d patches' % len(S))
