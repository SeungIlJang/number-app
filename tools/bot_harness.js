/* 멈춰라 숫자 — 밸런스 측정용 자동 플레이 하네스 (측정 전용, 배포본에는 절대 넣지 않는다)
 *
 * 왜 필요한가:
 *   점수·코인 밸런스를 "고치기 전후 실측값"으로 비교하려면 같은 난수 시드로
 *   같은 라운드 전개를 두 번 재생해야 한다. 실제 타이머로 돌리면 40연속 한 판에
 *   20초 이상 걸리고 재현도 안 되므로, 가상 시계로 게임 루프를 즉시 돌린다.
 *
 * 안전장치 (가장 먼저 실행된다):
 *   window.fbSubmit / window.dailySubmit 을 무력화한다. 안 막으면 테스트 점수가
 *   실제 전세계 랭킹(Firestore number_lb)에 올라가고 클라이언트에서 지울 수 없다.
 *
 * 사용법 (브라우저 콘솔 / javascript_tool):
 *   __runBot({seed:1, hits:40, perfect:true, mods:true})
 *     → {hits, score, runCoins, mult, mods, state}
 */
(function () {
  if (window.__H) return 'already';
  var H = { blocked: [], log: [] };
  window.__H = H;

  // ── 1) 랭킹 제출 차단 (무엇보다 먼저) ─────────────────────────────
  window.fbSubmit = function () { H.blocked.push('fbSubmit'); };
  window.dailySubmit = function () { H.blocked.push('dailySubmit'); };

  // ── 2) 가상 시계 — setTimeout 을 큐로 바꿔 즉시 소화한다 ──────────
  var vt = 0, seq = 0, q = new Map();
  H.now = function () { return vt; };
  H.vt = function () { return vt; };
  window.setTimeout = function (fn, ms) { var id = ++seq; q.set(id, { t: vt + (+ms || 0), fn: fn }); return id; };
  window.clearTimeout = function (id) { q.delete(id); };
  window.setInterval = function () { return ++seq; };
  window.clearInterval = function () { };
  window.requestAnimationFrame = function () { return 0; };
  window.cancelAnimationFrame = function () { };
  try { performance.now = function () { return vt; }; } catch (e) { }

  // ── 3) 소리·파티클 무음화 (속도 + AudioContext 폭주 방지) ─────────
  ['tone', 'chord', 'vib', 'burst', 'burstFx', 'hitFlash', 'floatText',
    'banner', 'hideBanner', 'setBG', 'setRing'].forEach(function (n) {
      if (typeof window[n] === 'function') window[n] = function () { };
    });
  window.sfx = function () { return true; };   // 샘플 재생했다고 응답 → 폴백 톤도 안 울림

  H.fire = function () {
    var bt = Infinity, bid = null;
    q.forEach(function (e, id) { if (e.t < bt) { bt = e.t; bid = id; } });
    if (bid === null) return false;
    var e = q.get(bid); q.delete(bid); vt = e.t;
    try { e.fn(); } catch (err) { H.log.push('ERR ' + (err && err.message)); }
    return true;
  };
  H.pending = function () { return q.size; };
  return 'ok';
})();
