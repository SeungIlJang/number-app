# -*- coding: utf-8 -*-
"""앱에서 이미지가 안 나오던 것을 고친다. (1회성 패치)

증상: 앱 홈 화면의 아이콘이 깨진 이미지로 뜬다.

원인: 앱(index.html)은 라이브 HTML을 fetch 해서 document.write 로 기기 안
로컬 문서에 주입한다. document.write 는 문서의 기준 주소를 바꾸지 않으므로
'img/number/ui/...' 같은 상대경로가 전부 앱 속 www/ 를 가리킨다.
그런데 스토어에 올라간 AAB 는 npm run sync 가 www/ 를 지우던 시절(4fb914d 이전)에
빌드돼서 그 안에 아트가 없다. 그래서 자산이 전부 404 다 —
CSS 배경과 art() 이미지는 조용히 사라지니 티가 안 났고, 폴백이 없는
홈 아이콘 <img> 만 깨진 그림으로 보였다.

고침: 앱에서 열렸을 때만 자산 기준 주소(base)를 라이브 사이트로 돌린다.
스토어 업데이트 없이 이미 설치된 앱에서도 바로 적용된다.
"""
import io, os, sys

GAMES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'games', 'number.html'))
LOADER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www', 'index.html'))

G = []

# ── 1. 자산 기준 주소 ─────────────────────────────────────────────
G.append(("""<meta charset="utf-8"/>""",
"""<meta charset="utf-8"/>
<script>
/* 앱은 이 파일을 fetch 해서 기기 안 로컬 문서에 document.write 로 주입한다.
   document.write 는 문서의 기준 주소를 바꾸지 않으므로 'img/...' 같은 상대경로가
   앱 속 www/ 를 가리키는데, 스토어 AAB 는 www/ 가 비어 있던 시절에 빌드돼서
   자산이 전부 404 다. 그래서 주입된 경우에만 자산을 라이브 사이트에서 받게 한다.

   주입 여부는 문서 주소로 안다 — 직접 열면 주소가 number.html 로 끝나고,
   주입되면 로더(index.html)의 주소 그대로다. */
(function(){
  if(/\\/number\\.html$/.test(location.pathname)) return;  /* 웹·개발서버에서 직접 열람 */
  if(/\\/game\\.html$/.test(location.pathname)) return;    /* 앱 속 오프라인 폴백 */
  if(window.__OTA_LOCAL) return;                         /* 로더가 캐시로 띄운 경우 */
  var b=document.createElement('base'); b.href='https://seungiljang.github.io/games/';
  document.head.insertBefore(b, document.head.firstChild);
})();
</script>"""))

# ── 2. 아이콘 경량화 (480KB -> 14KB) ──────────────────────────────
G.append(("""<link rel="icon" type="image/png" href="img/number/ui/icon_512.png"/>
<link rel="apple-touch-icon" href="img/number/ui/icon_512.png"/>""",
"""<link rel="icon" type="image/png" href="img/number/ui/icon_256.png"/>
<link rel="apple-touch-icon" href="img/number/ui/icon_256.png"/>"""))

# ── 3. 홈 아이콘 — base 가 안 먹는 상황에서도 깨진 그림을 안 보이게 ──
G.append(("""  <img id="startIcon" src="img/number/ui/icon_512.png" alt="" width="72" height="72"/>""",
"""  <img id="startIcon" src="img/number/ui/icon_256.png" alt="" width="72" height="72"
    onerror="if(this.dataset.r){this.style.display='none'}else{this.dataset.r=1;this.src='https://seungiljang.github.io/games/img/number/ui/icon_256.png'}"/>"""))

# ── 4. 로더: 캐시로 띄울 땐 원격 자산을 보지 않게 (다음 빌드부터) ──
L = [("""if(c){ render(c); }""",
      """if(c){ window.__OTA_LOCAL=true; render(c); }""")]


def patch(path, subs, label):
    s = io.open(path, encoding='utf-8').read()
    fail = []
    for a, b in subs:
        c = s.count(a)
        if c != 1:
            fail.append((c, a[:70]))
        else:
            s = s.replace(a, b)
    if fail:
        for c, a in fail:
            print('%s — 매칭 %d건: %s' % (label, c, a))
        return False
    io.open(path, 'w', encoding='utf-8').write(s)
    print('%s %d건 완료' % (label, len(subs)))
    return True


ok = patch(GAMES, G, 'games/number.html')
ok = patch(LOADER, L, 'www/index.html') and ok
sys.exit(0 if ok else 1)
