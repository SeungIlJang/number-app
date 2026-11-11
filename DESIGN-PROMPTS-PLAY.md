# 멈춰라 숫자 — **플레이 화면** 아트 발주서 (neon-v3)

> 지난 neon-v2(아이콘·랭크·부스터)는 전부 **메뉴·상점·결과 화면**용이었습니다.
> 정작 플레이어가 시간의 95%를 보내는 **플레이 화면에는 아트가 0개**이고,
> 전부 시스템 폰트 텍스트입니다. 이번 발주는 **플레이 화면만** 다룹니다.

- 생성물 보관: `D:/AI/workspace/game/images/number/neon-v3/`
- 프로젝트 사본: `games/img/number/play/`, `number-app/www/img/number/play/`
- **현재 화면 직접 보기**: https://seungiljang.github.io/games/number.html (시작 → 몇 판)
- **영역 지도**: `images/number/_brief/play_layout.png`

---

## 0. 지금 화면의 문제 (발주 배경)

| 요소 | 현재 상태 |
|---|---|
| 배경 | 거의 단색 `#0a0e1a` + 약한 비네트. 깊이 없음 |
| 현재 숫자 | 126px 시스템 폰트. **게임의 주인공인데 가장 밋밋함** |
| 목표 숫자 | 46px 시안 텍스트. 눈에 안 띔 |
| 판정(GOOD/PERFECT) | 그냥 글자가 떠올랐다 사라짐 |
| 화면 하단 35% | **완전히 빈 공간** |
| 생명·콤보 | 이모지 💛 🔥 (기기마다 모양 다름) |

핵심은 **"숫자가 주인공처럼 보이게"** 하는 것입니다.
숫자를 감싸는 무대(패널)와 목표를 잠그는 조준링, 그리고 깊이 있는 배경 — 이 셋이면 인상이 바뀝니다.

---

## 1. 공통 스타일 (모든 프롬프트 뒤에 붙이기)

게임 내 실제 색입니다. 벗어나면 UI와 따로 놉니다.

| 용도 | HEX |
|---|---|
| 배경(딥) | `#0a0e1a` |
| 배경(중심부) | `#12182e` |
| 시안(현재 숫자·주 액센트) | `#7cf6ff` |
| 골드(목표·콤보·보상) | `#ffd34d` |
| 민트(성공) | `#5cffb0` |
| 퍼플(롤링 라운드) | `#c9a3ff` |
| 레드(실패·위험) | `#ff5a6e` |

```
Style: neon arcade game UI art, dark navy background (#0a0e1a),
glowing cyan (#7cf6ff) and gold (#ffd34d) light, glass and holographic surfaces,
crisp clean edges, subtle bloom, high contrast, mobile portrait game.
Negative: photorealistic, 3D render of real objects, text, letters, numbers unless
specified, watermark, busy clutter, low contrast, muddy colors, realistic faces.
```

> ⚠️ **숫자·글자를 넣지 마세요.** 숫자는 게임이 실시간으로 그립니다.
> (예외: 4번 숫자 스프라이트)

---

## 2. 🔴 1순위 — 이 3장이면 화면이 바뀝니다

### 2-1. 배경 3종 (각 1080×1920, 불투명 PNG)

`play_bg_normal.png` / `play_bg_golden.png` / `play_bg_roll.png`

**필수 제약 — 이걸 어기면 숫자가 안 읽힙니다**
- 세로 **32%~66% 구간은 거의 비워 둘 것**(아주 어둡고 디테일 없게). 그 위에 큰 숫자가 올라갑니다.
- 화려한 디테일은 **하단 66%~100%**(지금 텅 빈 구간)과 **상단 0~20%**에 배치
- 전체적으로 어두워야 함. 평균 밝기가 지금(#0a0e1a)보다 크게 밝아지면 안 됩니다.

```
(normal) A vertical mobile game background, deep navy (#0a0e1a) void with a faint
cyan light well in the upper middle. Lower third: a wide perspective grid floor of
thin glowing cyan lines receding to a horizon, with soft floating dust motes and a
few blurred drifting numerals far in the background at very low opacity.
The vertical middle band of the image is almost empty and very dark so bright
foreground elements stay readable. Subtle vignette on all edges.
Style: neon arcade game UI art, glass and holographic surfaces, subtle bloom,
high contrast, mobile portrait 9:16. Negative: text, large numerals in focus,
clutter in the center, bright center, photorealism, watermark.
```

```
(golden) Same composition and layout as the normal background, but the light well
and grid floor glow warm gold (#ffd34d), with slow rising gold sparks and a faint
sunburst behind the upper middle. Richer and more celebratory, still dark overall,
middle band still nearly empty. Style and negatives identical to the normal version.
```

```
(roll) Same composition and layout as the normal background, but violet (#c9a3ff):
the lower grid becomes a spinning slot-machine reel surface with motion blur streaks,
and faint circular light trails orbit the upper middle. Tense and kinetic,
still dark overall, middle band still nearly empty. Style and negatives identical.
```

### 2-2. 목표 조준링 `target_ring.png` (512×512, 투명)

목표 숫자가 **링 한가운데에 얹힙니다.** 앱 아이콘과 같은 조형이라 브랜드가 이어집니다.

```
A glowing gold targeting reticle ring for a game HUD, transparent background.
A thin bright gold (#ffd34d) circle with four tick marks at top, bottom, left and right,
small corner brackets just outside the circle, soft warm bloom around the stroke.
The inside of the ring is completely empty and transparent — a number will be
placed in the center by the game.
Ring stroke thin and crisp, readable at 120px.
Style: neon arcade game UI art, clean vector-like edges, subtle bloom.
Negative: text, numbers, filled center, thick heavy ring, photorealism, watermark.
```

추가로 **잠금 상태** 1장 더: `target_ring_locked.png` (같은 규격)
```
Same gold targeting reticle, but locked on: the ring is brighter and doubled with a
second thin inner ring, the four tick marks extended into longer brackets,
and a sharp radial flare burst behind it. Still completely empty and transparent inside.
```

### 2-3. 숫자 무대 `number_stage.png` (768×448, 투명)

현재 숫자가 **이 패널 위에 얹힙니다.** 숫자가 "떠 있는 글자"가 아니라 "장치에 표시된 값"처럼 보이게 하는 핵심입니다.

```
A horizontal holographic display panel for a game HUD, transparent background.
A wide dark glass plate with softly rounded corners, thin glowing cyan (#7cf6ff)
edge light, faint horizontal scanlines inside, small bracket marks at the left and
right ends, and a gentle cyan glow pooling under the plate.
The center of the plate is dark, flat and uncluttered — a large number will be
drawn on top of it by the game.
Style: neon arcade game UI art, glass and holographic surface, subtle bloom,
crisp edges. Negative: text, numbers, busy texture in the center, opaque background,
photorealism, watermark.
```

---

## 3. 🟠 2순위 — 판정 순간의 쾌감

### 3-1. 판정 스탬프 3종 (각 640×320, 투명)

`stamp_perfect.png` / `stamp_good.png` / `stamp_miss.png`
**글자는 게임이 올립니다. 글자 없는 리본/배지 틀만** 만들어 주세요.

```
A set of 3 game judgment banner plates in one consistent style, transparent background,
wide horizontal ribbon badges with angled ends and a glowing outline, empty inside
(no text — the game draws the word on top):
1) PERFECT tier - bright gold (#ffd34d) ribbon with radiating light spikes behind it,
   strongest glow, small sparkles at the corners
2) GOOD tier    - mint green (#5cffb0) ribbon, simpler, medium glow
3) MISS tier    - red (#ff5a6e) ribbon, cracked and slightly broken edges, dim glow
Same silhouette and proportions across all three, only color, ornament and intensity change.
Style: neon arcade game UI art, clean edges, subtle bloom, readable at 160px wide.
Negative: text, letters, numbers, filled opaque center, photorealism, watermark.
```

### 3-2. 성공 버스트 `burst_hit.png` (512×512, 투명)

목표를 맞힌 순간 숫자 뒤에서 한 번 터집니다(게임이 확대·페이드 처리).

```
A single radial impact burst for a game effect, transparent background:
a thin bright ring expanding outward with sharp light shards radiating from the center,
white-hot core fading to cyan (#7cf6ff) at the edge, fine sparks scattered around.
Centered, symmetrical, empty in the very middle.
Style: neon arcade game VFX, crisp, high contrast, subtle bloom.
Negative: text, numbers, solid fill, smoke, photorealism, watermark.
```

같은 구도로 색만 바꾼 2장 더:
- `burst_perfect.png` — 골드(#ffd34d), 더 강하게
- `burst_chain.png` — 민트(#5cffb0), 고리 모양이 겹쳐 터지는 형태

### 3-3. 체인 연결 `chain_link.png` (128×128, 투명)

```
A small glowing gold chain link icon for a game HUD, transparent background:
two interlocking rings at a slight angle, thin stroke, warm gold (#ffd34d),
soft bloom, readable at 24px.
Style: neon arcade game UI icon, clean vector-like edges.
Negative: text, numbers, thick heavy shape, photorealism, watermark.
```

---

## 4. 🟡 3순위 — 숫자 스프라이트

> ⚠️ **이 항목은 별도 발주서로 분리됐습니다 → [`DESIGN-PROMPTS-DIGITS.md`](DESIGN-PROMPTS-DIGITS.md)**
>
> 아래 초안은 **폐기**합니다. 규격이 두 군데 달라 혼선이 생기니 새 문서만 보세요.
>
> 바뀐 점:
> - 캔버스 `256×352` → **`224×320`** (실제 렌더 비율을 측정해서 다시 잡음)
> - 투명 PNG + 연한 시안 → **검정 배경 위 흰 숫자(흑백) 불투명 PNG**
>   게임이 색을 매 프레임 바꾸므로 마스크로 쓰고, 색·글로우는 코드가 입힙니다
> - 베이스라인·글자 높이를 **y=288 / 256 px** 로 수치 고정 + 자가 검수 스크립트 포함
> - 규격 참고도 `images/number/_brief/digit_metrics.png` 추가

---

## 5. 🟢 4순위 — HUD 아이콘

> ⚠️ **이 항목은 별도 발주서로 분리됐습니다 → [`DESIGN-PROMPTS-ICONS.md`](DESIGN-PROMPTS-ICONS.md)**
>
> 아래 초안은 **폐기**합니다. 규격이 두 군데 달라 혼선이 생기니 새 문서만 보세요.
>
> 바뀐 점:
> - 3종(생명·콤보·코인) → **8종** (트로피·일일챌린지·상점·방법·목표 추가)
>   게임 전체 이모지 48종의 노출 빈도를 세서 가장 오래 보이는 것들을 골랐습니다
> - "readable at 20px" → **실측 10.5~16px**. 96px 캔버스가 16%로 줄어든다는 뜻이라
>   **선 굵기 하한 8px**을 수치로 못 박고, 16px 미리보기 납품을 필수로 했습니다
> - 어두운 배경(`#0a0e1a`) 위에 올라가므로 **어두운 외곽선 금지** 조항 추가
> - 규격 참고도 `images/number/_brief/icon_metrics.png` 추가

---

## 5-2. 🟢 5순위 — 라운드 배너 아이콘

> 별도 발주서 → [`DESIGN-PROMPTS-BANNER.md`](DESIGN-PROMPTS-BANNER.md)
>
> 라운드 시작 배너의 이모지 6종(`⚡ 🌟 📈 ✖️ 🔢 ❌`). 4순위와 같은 규격(96×96 투명 full-color)이고
> 표시 크기만 28~34px로 큽니다. 핵심은 **이미 들어간 HUD 아이콘 8종과 한 가족으로 보이는 것**,
> 그리고 **곱하기(✖️)와 실패(❌)를 확실히 구분하는 것**입니다.

---

## 6. 납품 체크리스트

- [ ] 1080×1920 배경 3종 — **세로 32~66% 구간이 어둡고 비어 있는지 꼭 확인**
- [ ] 배경은 1장당 **250KB 이하**로 저장(웹에서 매번 로드됩니다)
- [ ] 투명이 필요한 자산은 실제 알파 채널 확인
- [ ] 숫자 10장은 **베이스라인·글자높이·좌우여백 동일**
- [ ] 글자·숫자를 그려 넣지 않았는지 (4번 제외)
- [ ] 기존 파일을 덮지 말고 `neon-v3/` 아래에 저장

## 7. 받은 뒤 제가 할 일

| 자산 | 연결 작업 |
|---|---|
| 배경 3종 | 라운드 종류에 따라 교체 + 부드러운 전환 |
| 조준링 | 목표 숫자 뒤에 배치, 목표 도달 시 `locked` 버전으로 교체 |
| 숫자 무대 | 현재 숫자 뒤에 배치 |
| 판정 스탬프·버스트 | 판정 순간 확대→페이드 연출 |
| 숫자 스프라이트 | 텍스트 렌더링을 이미지 조합으로 교체 + CSS 필터로 색 상태 처리 |
| HUD 소품 | 이모지 치환(실패 시 이모지로 자동 복구) |

분량이 많으면 **2번(1순위) 5장만 먼저** 주셔도 됩니다. 그것만으로도 플레이 화면 인상이 가장 크게 바뀝니다.
