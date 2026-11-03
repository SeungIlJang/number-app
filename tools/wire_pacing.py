# -*- coding: utf-8 -*-
"""페이싱 수술: 라운드 단축 + 체인 조기화 + 전환 텀 단축 (1회성 패치)

측정 결과 플레이 시간의 84%가 대기였다(틱 5.21번 중 1.36번만 탭, 라운드 시간의 37.5%가 전환 텀).
읽을 만큼만 보여주고 바로 누르게 바꾼다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# 1) 전환 텀 1000 -> 450ms. 중복 입력 방지는 짧은 입력 잠금으로 따로 건다.
S.append(("""const GAP_MS=1000;   // 스테이지 전환 텀(성공 후 다음 라운드까지)""",
          """const GAP_MS=450;    // 라운드 전환 텀 — 1000ms는 죽은 시간이 너무 길어 450으로 단축"""))

# 2) 체인을 더 일찍, 더 자주 — 라운드당 탭 횟수를 늘린다
S.append(("""function chainCount(){
  if(rule.type!=='add' && rule.type!=='alt' && rule.type!=='stepup') return 1;   // 롤링·선택형·곱하기는 단일 목표
  if(hits>=22){ const r=Math.random(); return r<0.16?3:(r<0.52?2:1); }
  if(hits>=12) return Math.random()<0.28?2:1;
  return 1;
}""",
          """function chainCount(){
  if(rule.type!=='add' && rule.type!=='alt' && rule.type!=='stepup') return 1;   // 롤링·선택형·곱하기는 단일 목표
  const b=modChain;                                   // 모디파이어로 체인 확률 보정
  if(hits>=16){ const r=Math.random(); return r<0.22+b?3:(r<0.60+b*2?2:1); }
  if(hits>=6)  return Math.random()<0.35+b?2:1;
  return 1;
}"""))

# 3) 라운드 길이 k 3~5 -> 2~4. 규칙을 읽을 만큼만 보여주고 바로 목표로.
S.append(("""    const tg=[]; let t=cur, si=0;
    for(let c=0;c<nC;c++){ const k=rule.type==='mul'?rnd(2,3):rnd(3,5); for(let j=0;j<k;j++){ t=advance(t,si); si++; } tg.push(t); }""",
          """    const tg=[]; let t=cur, si=0;
    // 첫 목표는 규칙을 읽을 수 있게 3칸 이상, 이어지는 체인 고리는 2칸부터(대기 시간 단축)
    for(let c=0;c<nC;c++){ const k=rule.type==='mul'?rnd(2,3):(c===0?rnd(3,4):rnd(2,4)); for(let j=0;j<k;j++){ t=advance(t,si); si++; } tg.push(t); }"""))

# 4) 감소 수열 시작값도 짧아진 라운드에 맞춰 조정(목표가 음수로 가지 않게)
S.append(("""    else if(rule.type==='add' && rule.s<0) cur = rnd(10,20) + nC*5*(-rule.s);   // 감소 수열은 목표가 음수로 안 가게 높게 시작""",
          """    else if(rule.type==='add' && rule.s<0) cur = rnd(10,20) + nC*4*(-rule.s);   // 감소 수열은 목표가 음수로 안 가게 높게 시작"""))

fail = []
for a, b in S:
    c = s.count(a)
    if c != 1:
        fail.append((c, a[:70]))
    else:
        s = s.replace(a, b)
if fail:
    for c, a in fail:
        print('매칭 %d건: %s' % (c, a))
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('페이싱 패치 %d건 완료' % len(S))
