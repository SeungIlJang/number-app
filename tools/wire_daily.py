# -*- coding: utf-8 -*-
"""일일 챌린지 — 같은 날이면 누구나 똑같은 순서의 라운드 (1회성 패치)

게임 로직을 결정하는 난수만 시드 PRNG로 바꾼다. 파티클·칭찬문구 같은 연출용 난수는
플레이에 따라 호출 횟수가 달라지므로 시드 스트림에서 분리해야 재현성이 깨지지 않는다.
"""
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
s = io.open(P, encoding='utf-8').read()
S = []

# ── 1) 시드 PRNG ──────────────────────────────────────────────────
S.append(("""const pick=a=>a[Math.floor(Math.random()*a.length)];
const rnd=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;""",
"""const pick=a=>a[Math.floor(Math.random()*a.length)];
const rnd=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
// ── 시드 난수 (일일 챌린지) ───────────────────────────────────────
// 게임 로직용 스트림. 연출용 pick/rnd 와 분리해야 같은 시드에서 같은 라운드가 나온다.
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0;
  let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
let rngF=Math.random;                       // 평소엔 그냥 랜덤
const rngS=()=>rngF();
const pickS=a=>a[Math.floor(rngF()*a.length)];
const rndS=(a,b)=>Math.floor(rngF()*(b-a+1))+a;
function dayKey(d){ d=d||new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function daySeed(key){ let h=2166136261; for(let i=0;i<key.length;i++){ h^=key.charCodeAt(i); h=Math.imul(h,16777619); } return h>>>0; }"""))

# ── 2) 로직 난수를 시드 스트림으로 교체 ──────────────────────────
S.append(("""function baseRule(){
  const r=Math.random();""",
          """function baseRule(){
  const r=rngS();"""))
S.append(("""  if(hits>=14 && r<rollCh+0.31) return {type:'stepup', s:pick([2,3,4])}; // 📈 계단 — 스텝이 매번 +1""",
          """  if(hits>=14 && r<rollCh+0.31) return {type:'stepup', s:pickS([2,3,4])}; // 📈 계단 — 스텝이 매번 +1"""))
S.append(("""  if(hits<6)  return {type:'add', s:pick([2,3,4,5])};
  if(hits<11) return Math.random()<0.62? {type:'add', s:pick([2,3,4,5,6,7])} : {type:'alt', a:pick([2,3,4]), b:pick([1,2,3])};
  const q=Math.random();
  return q<0.38? {type:'add', s:pick([-4,-3,3,4,5,6,7,8])} : q<0.78? {type:'alt', a:pick([2,3,4,5]), b:pick([1,2,3,4])} : {type:'add', s:pick([6,7,8,9])};""",
          """  if(hits<6)  return {type:'add', s:pickS([2,3,4,5])};
  if(hits<11) return rngS()<0.62? {type:'add', s:pickS([2,3,4,5,6,7])} : {type:'alt', a:pickS([2,3,4]), b:pickS([1,2,3])};
  const q=rngS();
  return q<0.38? {type:'add', s:pickS([-4,-3,3,4,5,6,7,8])} : q<0.78? {type:'alt', a:pickS([2,3,4,5]), b:pickS([1,2,3,4])} : {type:'add', s:pickS([6,7,8,9])};"""))
S.append(("""  if(hits>=6 && hits%gEvery===0){ const g={type:'add', s:pick([3,4,5])}; g.golden=true; return g; }""",
          """  if(hits>=6 && hits%gEvery===0){ const g={type:'add', s:pickS([3,4,5])}; g.golden=true; return g; }"""))
S.append(("""  if(hits>=16){ const r=Math.random(), c3=Math.min(0.42,0.22+b), c2=Math.min(0.84,0.60+b); return r<c3?3:(r<c2?2:1); }
  if(hits>=6)  return Math.random()<Math.min(0.62,0.35+b)?2:1;""",
          """  if(hits>=16){ const r=rngS(), c3=Math.min(0.42,0.22+b), c2=Math.min(0.84,0.60+b); return r<c3?3:(r<c2?2:1); }
  if(hits>=6)  return rngS()<Math.min(0.62,0.35+b)?2:1;"""))

# newRound
S.append(("""    target = rnd(8,40); rollLo=target-6;""",
          """    target = rndS(8,40); rollLo=target-6;"""))
S.append(("""    if(rule.type==='mul') cur=rnd(2,5);                            // 곱하기는 작게 시작(폭주 방지)
    else if(rule.type==='add' && rule.s<0) cur = rnd(10,20) + nC*4*(-rule.s);   // 감소 수열은 목표가 음수로 안 가게 높게 시작
    else if(!keepCur || !isFinite(cur)) cur = hits<2 ? 1 : rnd(4,16);   // cur 손상(NaN) 시 복구""",
          """    if(rule.type==='mul') cur=rndS(2,5);                           // 곱하기는 작게 시작(폭주 방지)
    else if(rule.type==='add' && rule.s<0) cur = rndS(10,20) + nC*4*(-rule.s);  // 감소 수열은 목표가 음수로 안 가게 높게 시작
    else if(!keepCur || !isFinite(cur)) cur = hits<2 ? 1 : rndS(4,16);  // cur 손상(NaN) 시 복구"""))
S.append(("""    for(let c=0;c<nC;c++){ const k=rule.type==='mul'?rnd(2,3):(c===0?rnd(3,4):rnd(2,4)); for(let j=0;j<k;j++){ t=advance(t,si); si++; } tg.push(t); }""",
          """    for(let c=0;c<nC;c++){ const k=rule.type==='mul'?rndS(2,3):(c===0?rndS(3,4):rndS(2,4)); for(let j=0;j<k;j++){ t=advance(t,si); si++; } tg.push(t); }"""))

# setupChoice
S.append(("""  const ladder = hits>=20 && Math.random()<0.35;
  const step = hits<8? pick([1,2,3]) : hits<16? pick([2,3,4,5]) : pick([3,4,5,6,7]);
  const k = hits<16?3:4, start0=rnd(1,9); const terms=[]; let t=start0, st=step;""",
          """  const ladder = hits>=20 && rngS()<0.35;
  const step = hits<8? pickS([1,2,3]) : hits<16? pickS([2,3,4,5]) : pickS([3,4,5,6,7]);
  const k = hits<16?3:4, start0=rndS(1,9); const terms=[]; let t=start0, st=step;"""))
S.append(("""  while(arr.length<nc && g++<60){ const d=correct+pick([-2,-1,1,2,step,-step]); if(d!==correct && d>0 && !set.has(d)){ set.add(d); arr.push(d); } }
  while(arr.length<nc){ const d=correct+rnd(1,6); if(!set.has(d)){ set.add(d); arr.push(d); } }
  for(let i=arr.length-1;i>0;i--){ const j=rnd(0,i); const tmp=arr[i];arr[i]=arr[j];arr[j]=tmp; }""",
          """  while(arr.length<nc && g++<60){ const d=correct+pickS([-2,-1,1,2,step,-step]); if(d!==correct && d>0 && !set.has(d)){ set.add(d); arr.push(d); } }
  while(arr.length<nc){ const d=correct+rndS(1,6); if(!set.has(d)){ set.add(d); arr.push(d); } }
  for(let i=arr.length-1;i>0;i--){ const j=rndS(0,i); const tmp=arr[i];arr[i]=arr[j];arr[j]=tmp; }"""))

# 강화 카드도 같은 순서로 제시돼야 공정하다
S.append(("""  while(pick3.length<3 && bag.length) pick3.push(bag.splice(Math.floor(Math.random()*bag.length),1)[0]);""",
          """  while(pick3.length<3 && bag.length) pick3.push(bag.splice(Math.floor(rngF()*bag.length),1)[0]);"""))

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
print('시드 교체 %d건 완료' % len(S))
