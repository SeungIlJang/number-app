# -*- coding: utf-8 -*-
"""죽은 뒤 생명으로 이어갈 때 '앞에 숫자가 하나 더 붙던' 것을 고친다. (1회성 패치)

증상: 💛 생명으로 부활한 뒤부터 현재 숫자 앞에 '죽을 때 멈췄던 숫자'가 계속 붙어 있다.
  수열이 12 → 15 → 18 인데 화면에는 5318 로 보인다(53 에서 죽었던 판).
  숫자가 패널 밖으로 넘쳐 잘리고, 목표와 비교가 안 돼 그 판은 사실상 못 한다.

원인은 두 가지가 겹친 것이다.

1) die() 가 스프라이트 모드(.spr)인 채로 textContent 를 쓴다.
     1395:  $('cur').classList.add('miss'); $('cur').textContent=stopped;
   이러면 <i> 자식들이 날아가고 그 자리에 텍스트 노드가 남는다.
   부활 후 setNum() 이 다시 불리는데,
     if(!el.classList.contains('spr')){ el.textContent=''; ... }
   .spr 이 이미 붙어 있으므로 이 청소 줄을 건너뛴다. 그래서 텍스트 노드는 그대로 남고
   그 뒤에 <i> 들이 새로 append 된다 → [텍스트 "53"] + <i>1</i><i>8</i>.

2) 그 텍스트가 왜 보이는가. #cur.spr 에 font-size:0 이 있는데도 보이는 이유는
   setNum() 의 글자 렌더링 분기가 남긴 **인라인** font-size 때문이다.
     el.style.fontSize = fs+'px';
   인라인 스타일은 클래스 규칙을 이기므로 font-size:0 이 무시된다.
   이 분기는 digit_*.webp 가 아직 안 받아진 게임 초반에 반드시 한 번 지나간다
   (initDigits 가 비동기 프리로드라 digitOK 가 잠깐 false 다).
   즉 인라인 126px 이 판 내내 남아 있다가, 1) 이 텍스트를 넣는 순간 눈에 보인다.

고치는 법 — 두 군데 다 막는다(한쪽만 막으면 다른 경로로 또 샌다):
  A. setNum() 스프라이트 분기에서 인라인 font-size 를 지우고,
     <i> 가 아닌 자식 노드(텍스트)를 전부 걷어낸다. 어느 경로로 들어와도 깨끗해진다.
  B. die() 가 textContent 대신 setNum() 으로 멈춘 숫자를 그린다.
     결과도 더 낫다 — 실패 화면의 숫자도 스프라이트로 보인다(지금은 글꼴로 바뀐다).
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# A. setNum 스프라이트 분기 — 들어올 때마다 잔재를 청소한다
S.append(("""  if(!el.classList.contains('spr')){ el.textContent=''; el.classList.add('spr'); }
  el.style.setProperty('--dh',dh+'px');""",
"""  if(!el.classList.contains('spr')){ el.textContent=''; el.classList.add('spr'); }
  // ⚠️ 글자 분기가 남긴 인라인 font-size 는 .spr 의 font-size:0 을 이긴다.
  //    지우지 않으면 아래에서 걷어낸 뒤에도 또 생긴 텍스트가 눈에 보인다.
  if(el.style.fontSize) el.style.fontSize='';
  // ⚠️ die() 처럼 .spr 인 채로 textContent 를 쓴 흔적(텍스트 노드)을 걷어낸다.
  //    남겨두면 숫자 앞에 죽을 때 값이 붙어서 5318 처럼 보인다.
  for(let n=el.firstChild; n; ){ const nx=n.nextSibling; if(n.nodeType!==1) el.removeChild(n); n=nx; }
  el.style.setProperty('--dh',dh+'px');"""))

# A-2. 자식 수 맞추기도 '엘리먼트' 기준으로 — 텍스트 노드가 섞여도 안 꼬인다
S.append(("""  while(el.children.length>s.length) el.removeChild(el.lastChild);""",
          """  while(el.children.length>s.length) el.removeChild(el.lastElementChild);"""))

# B. die() — 멈춘 숫자도 스프라이트로 그린다(텍스트 노드를 아예 안 만든다)
S.append(("""    $('cur').classList.remove('hit'); $('cur').classList.add('miss'); $('cur').textContent=stopped;""",
          """    $('cur').classList.remove('hit'); $('cur').classList.add('miss'); setNum($('cur'), stopped, [126,126,104,80]);"""))

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
print('ghost digits: %d patches' % len(S))
