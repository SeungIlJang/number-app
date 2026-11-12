# -*- coding: utf-8 -*-
"""const/let 을 선언보다 먼저 읽는 자리(TDZ)를 찾는다. 검사 도구 — 파일을 고치지 않는다.

wasDaily 버그(die() 안에서 선언 전에 읽어 ReferenceError)가 9일간 안 걸린 이유는
짧은 단락 평가 뒤에 숨어 있어서 특정 조건에서만 터졌기 때문이다.
같은 모양이 또 있는지 함수 단위로 훑는다.

판정: 함수 본문에서 `const X` / `let X` 선언 위치보다 **앞줄에** X 가 쓰이면 보고.
오탐이 섞인다(그 앞의 use 가 콜백 안이라 나중에 실행되는 경우 등).
그래서 자동 수정은 하지 않고 눈으로 확인할 목록만 뽑는다.
"""
import io, os, re, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
src = io.open(P, encoding='utf-8').read()
lines = src.split('\n')

# 최상위 function 블록을 중괄호 균형으로 잘라낸다
starts = [(i, m.group(1)) for i, l in enumerate(lines)
          for m in [re.match(r'function\s+(\w+)\s*\(', l)] if m]

KEYWORDS = set('''if else for while return function const let var new typeof in of do switch case break
continue try catch finally throw true false null undefined this class'''.split())

hits = []
for si, name in starts:
    depth, end = 0, None
    for i in range(si, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if i > si or '{' in lines[si]:
            if depth <= 0 and i >= si:
                end = i
                break
    if end is None:
        continue
    body = lines[si:end + 1]
    for off, l in enumerate(body):
        for m in re.finditer(r'\b(?:const|let)\s+(\w+)\s*=', l):
            v = m.group(1)
            if v in KEYWORDS:
                continue
            # 선언 줄보다 앞줄에서 쓰였는지
            for pof in range(0, off):
                if re.search(r'\b' + re.escape(v) + r'\b', body[pof]):
                    hits.append((name, si + 1 + pof, si + 1 + off, v, body[pof].strip()[:90]))
                    break

if not hits:
    print('TDZ 의심 없음')
else:
    print('TDZ 의심 %d건 (함수 / 쓴줄 / 선언줄 / 이름)' % len(hits))
    for name, uline, dline, v, txt in hits:
        print('  %-14s use L%-5d decl L%-5d  %s' % (name, uline, dline, v))
        print('      %s' % txt)
