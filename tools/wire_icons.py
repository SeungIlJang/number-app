# -*- coding: utf-8 -*-
"""HUD 아이콘 8종을 이모지 자리에 끼운다. (1회성 패치)

원칙: **HTML 로 그려지는 자리만** 바꾼다.
  - 공유 문구(navigator.share), banner(), floatText() 는 textContent 로 나가는
    순수 텍스트다. 여기에 <img> 를 넣으면 태그가 그대로 보이거나, 다른 앱으로
    태그 문자열이 건너간다. 이모지를 그대로 둔다.
  - 부스터·모디파이어 목록의 i:'💛' 는 art() 가 쓰는 '못 불러왔을 때의 대체 문자'다.
    여기도 이모지로 남겨야 한다.

textContent -> innerHTML 로 바꾼 자리는 전부 '숫자 아니면 고정 문자열'만 들어간다.
닉네임 같은 사용자 입력이 섞이는 자리는 하나도 건드리지 않았다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()

LIFE, COMBO, COIN, TROPHY = '\U0001F49B', '\U0001F525', '\U0001F4B0', '\U0001F3C6'
DAILY, SHOP, HELP, TARGET = '\U0001F4C5', '\U0001F6D2', '\U0001F4D6', '\U0001F3AF'


def tag(name, emoji, px):
    """정적 마크업에 직접 넣을 <img>. 못 불러오면 이모지로 되돌린다."""
    return ('<img class="art" src="img/number/ui/ui_%s.webp" alt="" width="%d" height="%d" '
            'data-fb="%s" onerror="uiFB(this)"/>' % (name, px, px, emoji))


S = []   # (찾을 것, 바꿀 것, 기대 건수)

# ── 헬퍼 ──────────────────────────────────────────────────────────
S.append(("""function art(file,emoji,px){""",
"""// HUD 아이콘 — 이모지는 기기·OS마다 모양이 달라서 아트로 바꿨다.
// 못 불러오면 data-fb 의 이모지로 되돌아간다(뜻은 그대로 통한다).
function uiFB(el){ try{ el.replaceWith(document.createTextNode(el.dataset.fb||'')); }catch(e){} }
function uic(n,e,px){ return '<img class="art" src="'+ART+'ui_'+n+'.webp" alt="" width="'+px+'" height="'+px+'" data-fb="'+e+'" onerror="uiFB(this)">'; }
function art(file,emoji,px){""", 1))

# ── 정적 마크업 ───────────────────────────────────────────────────
S.append(('<div id="target">%s 이 숫자에서 멈춰!</div>' % TARGET,
          '<div id="target">%s 이 숫자에서 멈춰!</div>' % tag('target', TARGET, 15), 1))

S.append(('<div class="sl">%s 최고 기록</div>' % TROPHY,
          '<div class="sl">%s 최고 기록</div>' % tag('trophy', TROPHY, 13), 1))

S.append(('<div class="sl">%s 보유 코인</div>' % COIN,
          '<div class="sl">%s 보유 코인</div>' % tag('coin', COIN, 13), 1))

S.append(('<button class="btn" id="dailyBtn">%s 일일 챌린지' % DAILY,
          '<button class="btn" id="dailyBtn">%s 일일 챌린지' % tag('daily', DAILY, 18), 1))

S.append(('<button class="btn" id="lbBtn">%s 랭킹</button>' % TROPHY,
          '<button class="btn" id="lbBtn">%s 랭킹</button>' % tag('trophy', TROPHY, 16), 1))

S.append(('<button class="btn" id="shopBtn">%s 상점</button>' % SHOP,
          '<button class="btn" id="shopBtn">%s 상점</button>' % tag('shop', SHOP, 16), 1))

S.append(('<button class="btn" id="helpBtn">%s 방법</button>' % HELP,
          '<button class="btn" id="helpBtn">%s 방법</button>' % tag('help', HELP, 16), 1))

S.append(('<h1>%s 게임 방법</h1>' % HELP,
          '<h1>%s 게임 방법</h1>' % tag('help', HELP, 24), 1))

S.append(('<h1>%s 랭킹</h1>' % TROPHY,
          '<h1>%s 랭킹</h1>' % tag('trophy', TROPHY, 24), 1))

S.append(('<h1>%s 일일 챌린지</h1>' % DAILY,
          '<h1>%s 일일 챌린지</h1>' % tag('daily', DAILY, 24), 1))

S.append(('<h1 style="font-size:32px">%s 상점</h1>' % SHOP,
          '<h1 style="font-size:32px">%s 상점</h1>' % tag('shop', SHOP, 26), 1))

S.append(('color:#ffd34d">%s 랭킹</div>' % TROPHY,
          'color:#ffd34d">%s 랭킹</div>' % tag('trophy', TROPHY, 15), 1))

S.append(('font-size:17px;background:#20263c;box-shadow:0 6px 0 #10131f">%s 공유</button>' % TROPHY,
          'font-size:17px;background:#20263c;box-shadow:0 6px 0 #10131f">%s 공유</button>' % tag('trophy', TROPHY, 17), 1))

S.append(('<button class="btn" id="dailyShare">%s 결과 공유</button>' % TROPHY,
          '<button class="btn" id="dailyShare">%s 결과 공유</button>' % tag('trophy', TROPHY, 16), 1))

S.append(('<div class="sub">보유 %s <b id="shopCoins"' % COIN,
          '<div class="sub">보유 %s <b id="shopCoins"' % tag('coin', COIN, 15), 1))

# ── 이미 innerHTML 인 자리 ────────────────────────────────────────
S.append(("""'<button class="sbtn buyb" data-id="'+B.id+'">%s '+B.cost+'</button>'""" % COIN,
          """'<button class="sbtn buyb" data-id="'+B.id+'">'+uic('coin','%s',13)+' '+B.cost+'</button>'""" % COIN, 1))

S.append(("""'<button class="sbtn buy" data-id="'+t.id+'">%s '+t.cost+'</button>'""" % COIN,
          """'<button class="sbtn buy" data-id="'+t.id+'">'+uic('coin','%s',13)+' '+t.cost+'</button>'""" % COIN, 1))

S.append(("""' · 전부 완료 %s+'+DAILY_BONUS""" % COIN,
          """' · 전부 완료 '+uic('coin','%s',12)+'+'+DAILY_BONUS""" % COIN, 1))

S.append(("""<span style="color:#ffd34d">%s'+D.rw+'</span>'""" % COIN,
          """<span style="color:#ffd34d">'+uic('coin','%s',12)+D.rw+'</span>'""" % COIN, 1))

S.append(("""$('overCoin').innerHTML = '%s <b style="color:#ffd34d">+'+runEarned""" % COIN,
          """$('overCoin').innerHTML = uic('coin','%s',16)+' <b style="color:#ffd34d">+'+runEarned""" % COIN, 1))

# ── textContent -> innerHTML (숫자·고정 문자열만 들어가는 자리) ──
S.append(("""function renderHearts(){ const e=$('hearts'); if(e) e.textContent = hearts>0 ? ('%s'.repeat(Math.min(hearts,heartMax))) : ''; }""" % LIFE,
          """// hearts 는 숫자뿐이라 innerHTML 이어도 안전하다
function renderHearts(){ const e=$('hearts'); if(e) e.innerHTML = hearts>0 ? uic('life','%s',14).repeat(Math.min(hearts,heartMax)) : ''; }""" % LIFE, 1))

S.append(("""  if(score>best) el.textContent='%s 신기록 진행중! +'+(score-best);
  else if(score>=best*0.5) el.textContent='%s 최고까지 '+(best-score)+'점';""" % (COMBO, TROPHY),
          """  if(score>best) el.innerHTML=uic('combo','%s',13)+' 신기록 진행중! +'+(score-best);
  else if(score>=best*0.5) el.innerHTML=uic('trophy','%s',13)+' 최고까지 '+(best-score)+'점';""" % (COMBO, TROPHY), 1))

S.append(("""$('combo').textContent=hits>=2?('%s '+hits+' 연속'):''""" % COMBO,
          """$('combo').innerHTML=hits>=2?(uic('combo','%s',15)+' '+hits+' 연속'):''""" % COMBO, 3))

S.append(("""$('overTitle').textContent = rec?'%s 신기록!':'❌ 실패!';""" % TROPHY,
          """$('overTitle').innerHTML = rec?(uic('trophy','%s',24)+' 신기록!'):'❌ 실패!';""" % TROPHY, 1))

S.append(("""if(wasDaily) $('overTitle').textContent = rec?'%s 신기록!':'%s 오늘의 도전 종료';""" % (TROPHY, DAILY),
          """if(wasDaily) $('overTitle').innerHTML = rec?(uic('trophy','%s',24)+' 신기록!'):(uic('daily','%s',24)+' 오늘의 도전 종료');""" % (TROPHY, DAILY), 1))

S.append(("""else $('overRank').textContent = rank>0 ? ('%s 랭킹 '+rank+'위'""" % TROPHY,
          """else $('overRank').innerHTML = rank>0 ? (uic('trophy','%s',15)+' 랭킹 '+rank+'위'""" % TROPHY, 1))

fail = []
for a, b, n in S:
    c = s.count(a)
    if c != n:
        fail.append((c, n, a[:70]))
    else:
        s = s.replace(a, b)
if fail:
    for c, n, a in fail:
        print('matched %d, expected %d: %s' % (c, n, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('icon wiring: %d rules, %d replacements' % (len(S), sum(n for _, _, n in S)))
