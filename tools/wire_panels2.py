# -*- coding: utf-8 -*-
"""랭킹 화면 두 가지 마무리 (1회성 패치)

1) 좌상단 음소거 버튼(12..48 x 46..82)이 닉네임 줄(46..329 x 76..96)과 겹친다.
   좌우 여백을 줘서 버튼 자리를 비워준다. (#chase·#modBar 에 썼던 것과 같은 처방)

2) 기록이 6줄뿐이면 화면의 42%(812 중 339px)가 빈 공간으로 남는다.
   세로 가운데 정렬로 바꾼다. 목록이 길어져도 #lbList 가 60vh 에서 스스로
   스크롤하므로 넘치지 않는다(360x640 기준으로도 여유가 있다).
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()

S = [
    ("""  #lb{z-index:12;justify-content:flex-start;padding-top:calc(28px + env(safe-area-inset-top,0px))}""",
     """  #lb{z-index:12;justify-content:center;padding-top:calc(28px + env(safe-area-inset-top,0px))}
  /* 좌상단 음소거 버튼 자리를 비워둔다 */
  #lbName{padding:0 52px}"""),
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
print('ranking panel: %d patches' % len(S))
