# 멈춰라 숫자 — 디자인 발주 프롬프트 (v2.0)

생성한 이미지는 `D:/AI/workspace/game/images/number/` 에 **영문 파일명**으로 저장한 뒤
프로젝트(`number-app/`, `games/img/`)로 복사해 쓰세요.

---

## 0. 공통 스타일 가이드 (모든 프롬프트에 붙여서 사용)

게임 화면에서 실제로 쓰는 색입니다. 이 팔레트를 벗어나면 인게임과 따로 놀아요.

| 용도 | HEX |
|---|---|
| 배경(딥) | `#0a0e1a` |
| 배경(그라데이션 중심) | `#12182e` |
| 메인 액센트(시안) | `#7cf6ff` |
| 성공/민트 | `#5cffb0` |
| 골드/콤보 | `#ffd34d` |
| 롤링/퍼플 | `#c9a3ff` |
| 실패/레드 | `#ff5a6e` |
| 버튼 블루 | `#3a7bff` (그림자 `#1f52c0`) |

**공통 스타일 문구 (영문 프롬프트 뒤에 붙이기)**

```
Style: modern mobile hyper-casual game art, flat vector with soft neon glow,
deep navy background (#0a0e1a), cyan (#7cf6ff) and gold (#ffd34d) accents,
crisp geometric shapes, high contrast, no gradients banding, no text unless specified,
centered composition, clean silhouette readable at small size.
Negative: photorealistic, 3D render, cluttered, drop-shadow noise, watermark,
lens flare, low contrast, muddy colors, realistic human faces.
```

---

## 1. 앱 아이콘 ✅ 적용 완료

`python tools/make_icons.py` 로 생성·적용했습니다 (조준링에 멈춘 숫자 7 + 잔상 숫자).
숫자·색을 바꾸고 다시 돌리면 런처 아이콘·적응형·스플래시가 전부 갱신됩니다.
**아래 프롬프트는 외부 AI로 더 공들인 아트를 뽑고 싶을 때의 대안입니다.**
(그 경우 `assets/icon-only.png` · `assets/icon-foreground.png` 를 교체하고
`npx @capacitor/assets generate` 를 돌리면 됩니다.)

- 산출물: `icon_1024.png` (1024×1024, 모서리 여백 없는 풀블리드)
- 추가: `icon_foreground.png` (1024×1024, 중앙 66% 안에 요소 배치 · 투명 배경),
  `icon_background.png` (1024×1024, 단색/그라데이션) — 안드로이드 적응형 아이콘용

```
A mobile game app icon for a number-timing game called "Stop the Number".
Centerpiece: a large bold glowing cyan numeral styled like a digital counter,
frozen mid-flip, with a bright gold crosshair ring locking onto it.
Motion-blur ghost digits trailing behind the frozen numeral to imply it just stopped.
Deep navy rounded-square background (#0a0e1a) with a subtle radial glow (#12182e).
Numeral in #7cf6ff with neon bloom, crosshair ring in #ffd34d.
Style: modern mobile hyper-casual game art, flat vector with soft neon glow,
crisp geometric shapes, high contrast, bold silhouette readable at 48px.
Negative: photorealistic, 3D render, cluttered, text, watermark, realistic faces.
```

**대안 시안 B (캐릭터형 — 시리즈 인지도용)**

```
App icon: a cute round robot hand slamming a glowing red STOP button,
a cyan digital numeral frozen above it mid-change.
Deep navy rounded square background, gold rim light, neon cyan glow.
Flat vector mobile game icon style, bold readable silhouette at 48px.
```

---

## 2. 구글 플레이 피처 그래픽 (1024×500) ✅ 생성 완료

`images/number/feature_graphic_1024x500.png` — 타이틀까지 포함된 완성본입니다.
**아래 프롬프트는 외부 AI로 다시 뽑고 싶을 때의 대안입니다.**

```
Google Play feature graphic, 1024x500 landscape banner for a number-timing arcade game.
Right 60%: a dramatic cascade of glowing cyan numerals (3 6 9 12 15) flying diagonally
toward the viewer, one numeral frozen and locked inside a gold targeting ring,
gold particle burst radiating from it, purple (#c9a3ff) slot-machine reel blur in the background.
Left 40%: clean empty dark navy space reserved for a title, no text.
Deep navy background with radial glow, neon bloom, high contrast.
Style: modern mobile hyper-casual game art, flat vector with neon glow, cinematic energy.
Negative: text, logo, watermark, characters, photorealism, clutter.
```

---

## 3. 랭크 엠블럼 7종 (v2.0 신규) ⬅️ 남은 작업

시작 화면 랭크 카드에서 이모지(🥉🥈🥇💎🔷👑🌟) 자리에 쓸 이미지입니다.
**7장을 한 세트로, 같은 실루엣·같은 조명**으로 뽑아야 승급감이 살아요.

- 산출물: `rank_1_bronze.png` … `rank_7_grandmaster.png` (각 256×256, 투명 배경)

```
A set of 7 game rank emblem badges in one consistent style, transparent background,
each a hexagonal shield plate with a stylized numeral motif engraved in the center
and small orbiting digit particles. Same silhouette and lighting across all 7,
only material, color and ornament complexity change, escalating in prestige:
1) Bronze  - matte bronze (#c88a5a), plain plate, no gems
2) Silver  - polished silver (#cfd8e3), thin engraving
3) Gold    - bright gold (#ffd34d), laurel edge
4) Platinum- cyan-white platinum (#7cf6ff), faceted rim, faint glow
5) Diamond - blue crystal (#5c9dff), diamond inlay, refraction sparkle
6) Master  - violet (#c9a3ff), crown on top, aura ring
7) Grandmaster - rose-gold (#ff6ea8), winged crown, radiant halo, strongest bloom
Style: flat vector game badge with soft neon glow, crisp edges, readable at 64px,
deep navy friendly (designed to sit on #0a0e1a).
Negative: text, numbers written out, photorealism, 3D render, drop shadow on background.
```

> 한 번에 7장이 안 나오면 1~7을 각각 따로 생성하되,
> 프롬프트의 "same silhouette: hexagonal shield plate with engraved numeral motif" 문장을 **반드시 그대로 유지**하세요.

---

## 4. 부스터 아이콘 4종 (v2.0 신규) ⬅️ 남은 작업

상점 `⚡ 부스터` 탭과 시작 화면 칩에서 쓰는 아이콘입니다.

- 산출물: `boost_life.png` / `boost_slow.png` / `boost_coin2.png` / `boost_score2.png` (각 128×128, 투명 배경)

```
A set of 4 mobile game power-up icons, one consistent style, transparent background,
each inside a soft rounded-square glass tile with neon rim light:
1) "Extra Life"   - a glowing golden heart (#ffd34d) with a small "+2" spark, warm bloom
2) "Slow Start"   - a cyan turtle shell shaped like a clock face (#7cf6ff), slow motion streaks
3) "Double Coin"  - two overlapping gold coins (#ffd34d) each stamped with a numeral, sparkle
4) "Double Score" - a violet multiplication sign (#c9a3ff) made of light, with a rising score arrow
Style: flat vector game UI icon with soft neon glow, bold silhouette readable at 32px,
designed to sit on a dark navy UI (#0a0e1a).
Negative: text labels, photorealism, 3D render, busy background, watermark.
```

---

## 5. 스플래시 / 로딩 화면 ✅ 적용 완료

`tools/make_icons.py` 가 11종(세로·가로 각 density)을 함께 생성합니다.
아래는 외부 AI로 다시 뽑을 때의 대안 프롬프트입니다.

- 산출물: `splash_portrait_1080x1920.png`, `splash_land_1920x1080.png`

```
A vertical mobile game splash screen, deep navy (#0a0e1a) with a centered radial glow.
Center: a single huge glowing cyan numeral (#7cf6ff) with neon bloom,
surrounded by a faint gold targeting ring (#ffd34d) and slow-drifting digit particles.
Lots of calm empty space above and below for a title and a loading spinner.
Style: minimal, elegant, flat vector with neon glow, no text.
Negative: text, logo, characters, clutter, photorealism.
```

---

## 6. 인게임 라운드 배지 3종 (선택 · 이모지 대체용)

지금은 `⚡ 🔢 🌟 🔗` 이모지로 처리 중입니다. 기기별로 모양이 달라지는 게 거슬리면 교체하세요.

- 산출물: `badge_roll.png`, `badge_choice.png`, `badge_golden.png`, `badge_chain.png` (각 96×96, 투명)

```
A set of 4 round game event badges, consistent style, transparent background:
1) "Roll"   - a violet (#c9a3ff) slot-machine reel spinning with motion blur and a lightning bolt
2) "Choice" - a cyan (#7cf6ff) branching path of three glowing numeral tiles with a question mark tile
3) "Golden" - a gold (#ffd34d) radiant star burst with a "x2" light ribbon
4) "Chain"  - two gold interlocking rings threaded by a cyan numeral line, links glowing in sequence
Style: flat vector game UI badge with neon glow, bold silhouette readable at 24px, dark-UI friendly.
Negative: photorealism, 3D, text beyond the specified symbols, watermark.
```

---

## 7. 스토어 스크린샷 카피 (디자인 아니지만 전환율 영향 큼)

스크린샷 상단에 얹을 한 줄 카피 순서 추천 (1080×1920, 5장):

1. **“규칙을 읽고 목표에서 STOP!”** — 수열이 올라가는 플레이 화면
2. **“체인 목표를 연달아 맞히면 점수 폭발 🔗”** — 3연속 체인 + 골든 라운드 화면
3. **“💛 롤링 성공하면 생명 +1”** — 롤링 라운드 화면
4. **“랭크를 올려 그랜드마스터로”** — 랭크 카드 화면
5. **“전세계 랭킹에 도전”** — 리더보드 화면
