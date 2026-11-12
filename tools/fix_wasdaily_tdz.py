# -*- coding: utf-8 -*-
"""신기록을 낼 때마다 결과창이 안 뜨고 게임이 멈추던 것을 고친다. (1회성 패치)

증상: 점수를 내고 죽으면 판정만 보이고 결과창(#over)이 영영 안 열린다.
  홈으로도 못 가고 다시 시작도 안 된다. 앱을 껐다 켜야 한다.

원인: die() 안에서 wasDaily 를 '선언보다 먼저' 읽는다.

  1419:  if(fbReady && score>0 && rec && !wasDaily){ ... }   <- 여기서 읽고
  1423:  const wasDaily=dailyMode; finishDaily();            <- 여기서 선언

  const 는 호이스팅되지만 TDZ(일시적 사각지대)라 선언 전에 읽으면
  ReferenceError 가 난다. var 였으면 undefined 로 조용히 넘어갔을 자리다.
  die() 가 그 줄에서 통째로 중단되므로 뒤에 있는 것이 전부 실행되지 않는다:
    deathCount++ / finishDaily() / 부활버튼 / 배너·전면광고 /
    setTimeout(... $('over').classList.remove('hidden')) <- 결과창을 여는 바로 그 줄

언제 터지나: fbReady && score>0 && rec.
  && 가 단락 평가라 앞 셋이 모두 참일 때만 !wasDaily 까지 간다.
  rec 는 '최고 기록 경신'이다. 즉 **최고 기록을 깰 때마다** 터진다.
  - 신규 설치 유저는 best=0 이라 첫 판부터 100% 터진다.
  - 이미 기록이 높은 사람은 경신이 드물어 잘 안 터진다 → 그래서 9일간 안 걸렸다.
  일일 챌린지는 finishDaily() 가 안 돌아 그날 기록 제출도 같이 날아간다.

유입: v2.7(2026-11-03, 일일 챌린지)에서 !wasDaily 조건이 추가될 때.

고치는 법: 선언을 쓰는 곳보다 위로 올린다. finishDaily() 는 제자리에 둔다
  (dailyMode 를 지우는 쪽이라 캡처는 그보다 먼저여야 한다).
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# 1) 쓰기 전에 선언해 둔다
S.append(("""  const rank = score>0 ? insertScore(score) : 0;
  if(fbReady && score>0 && rec && !wasDaily){""",
          """  const rank = score>0 ? insertScore(score) : 0;
  // ⚠️ finishDaily() 가 dailyMode 를 지우므로 먼저 잡아둔다.
  //    이 선언이 아래로 내려가면 !wasDaily 를 읽는 순간 TDZ ReferenceError 가 나고
  //    die() 가 거기서 멈춰 결과창이 영영 안 열린다(신기록마다 재현).
  const wasDaily=dailyMode;
  if(fbReady && score>0 && rec && !wasDaily){"""))

# 2) 원래 자리의 중복 선언 제거 — finishDaily() 호출은 그대로 둔다
S.append(("""  const wasDaily=dailyMode; finishDaily();""",
          """  finishDaily();"""))

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
print('wasDaily TDZ: %d patches' % len(S))
