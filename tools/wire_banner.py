# -*- coding: utf-8 -*-
"""라운드 배너 아이콘 6종을 끼운다. (1회성 패치)

banner() 가 textContent 라 innerHTML 로 바꾼다. 호출 11곳을 전부 확인했고
고정 문자열 아니면 숫자만 들어간다 — nC, rule.m, 남은 시간, stopped=cur,
tgt=target, 랭크 이름(코드 상수). 닉네임 같은 사용자 입력이 들어가는 자리는 없다.

새로 받은 6종(roll·golden·stepup·mul·choice·fail) 말고도, 이미 아트가 있는
체인(chain_link)·슬로모(combo)·생명(life) 배너도 같이 바꾼다. 한 배너 줄에서
어떤 건 아이콘이고 어떤 건 이모지면 그게 더 어색하다.

승급(🎉)만 이모지로 남는다 — 전용 아트가 없고 아주 드물게 뜬다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()

ROLL, GOLD, CHAIN, STEP = '⚡', '\U0001F31F', '\U0001F517', '\U0001F4C8'
MUL, FIRE, CHOICE, FAIL, LIFE = '✖️', '\U0001F525', '\U0001F522', '❌', '\U0001F49B'
BPX = 28          # #banner 글자 26px — 아이콘은 조금 크게
TPX = 24          # 게임오버 제목(기존 trophy·daily 와 같은 크기)


def ic(name, emoji, px=BPX):
    return """'+uic('%s','%s',%d)+'""" % (name, emoji, px)


S = []

# ── banner() 를 innerHTML 로 ──────────────────────────────────────
S.append(("""function banner(txt,col){ const b=$('banner'); b.textContent=txt;""",
"""// 아이콘을 넣기 위해 innerHTML 을 쓴다. 호출부는 전부 고정 문자열 아니면 숫자다
// (nC · rule.m · 남은 시간 · stopped=cur · tgt=target · 랭크 이름은 코드 상수).
function banner(txt,col){ const b=$('banner'); b.innerHTML=txt;"""))

# ── 라운드 타입 배너 ──────────────────────────────────────────────
S.append(("""banner('%s 롤링! 감으로 STOP','#c9a3ff')""" % ROLL,
          """banner('%s 롤링! 감으로 STOP','#c9a3ff')""" % ic('roll', ROLL)))

S.append(("""banner('%s 골든 라운드! 점수 ×2','#ffd34d')""" % GOLD,
          """banner('%s 골든 라운드! 점수 ×2','#ffd34d')""" % ic('golden', GOLD)))

S.append(("""banner('%s 체인 '+nC+'연속 목표!','#ffd34d')""" % CHAIN,
          """banner('<img class="art" src="'+PLAY_DIR+'chain_link.webp" alt="" width="%d" height="%d" data-fb="%s" onerror="uiFB(this)"> 체인 '+nC+'연속 목표!','#ffd34d')"""
          % (BPX, BPX, CHAIN)))

S.append(("""banner('%s 계단! 간격이 커져요','#7cf6ff')""" % STEP,
          """banner('%s 계단! 간격이 커져요','#7cf6ff')""" % ic('stepup', STEP)))

S.append(("""banner('%s 곱하기! ×'+(rule.m||2),'#c9a3ff')""" % MUL,
          """banner('%s 곱하기! ×'+(rule.m||2),'#c9a3ff')""" % ic('mul', MUL)))

S.append(("""banner('%s 슬로모 끝! 이제 실전','#ff9a5a')""" % FIRE,
          """banner('%s 슬로모 끝! 이제 실전','#ff9a5a')""" % ic('combo', FIRE)))

S.append(("""banner('%s 다음 숫자는? · '+(cms/1000).toFixed(1)+'초','#7cf6ff')""" % CHOICE,
          """banner('%s 다음 숫자는? · '+(cms/1000).toFixed(1)+'초','#7cf6ff')""" % ic('choice', CHOICE)))

# ── 실패·생명 ─────────────────────────────────────────────────────
S.append(("""banner('%s 틀렸어요','#ff5a6e')""" % FAIL,
          """banner('%s 틀렸어요','#ff5a6e')""" % ic('fail', FAIL)))

S.append(("""banner('%s '+stopped+'  →  목표 '+tgt,'#ff5a6e')""" % FAIL,
          """banner('%s '+stopped+'  →  목표 '+tgt,'#ff5a6e')""" % ic('fail', FAIL)))

S.append(("""banner('%s 생명 사용! 계속 GO!','#ffd34d')""" % LIFE,
          """banner('%s 생명 사용! 계속 GO!','#ffd34d')""" % ic('life', LIFE)))

# ── 게임오버 제목 ─────────────────────────────────────────────────
S.append(("""$('overTitle').innerHTML = rec?(uic('trophy','\U0001F3C6',24)+' 신기록!'):'%s 실패!';""" % FAIL,
          """$('overTitle').innerHTML = rec?(uic('trophy','\U0001F3C6',24)+' 신기록!'):(uic('fail','%s',%d)+' 실패!');""" % (FAIL, TPX)))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:78]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('matched %d, expected 1: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('banner icons wired: %d patches' % len(S))
