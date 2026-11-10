# 멈춰라 숫자 — 4순위 발주서 **HUD 아이콘 8종** (neon-v3)

> 지금 게임은 이모지 48종을 쓰고 있습니다. 이모지는 **기기·OS마다 모양이 다르고**,
> 삼성·구글·애플이 각자 다르게 그립니다. 플레이어마다 다른 게임을 보고 있는 셈입니다.
> 그중 **가장 오래, 가장 자주 보이는 8개**만 교체합니다.

**산출물: 8장 (각 96×96, 투명 PNG, full-color)**
**저장 위치: `D:/AI/workspace/game/images/number/neon-v3/`** (프로젝트 복사·코드 수정·커밋 금지)
**규격 참고도: `images/number/_brief/icon_metrics.png` — 먼저 열어보세요**

---

## 0. 3순위(숫자)와 형식이 다릅니다

| | 3순위 숫자 | **4순위 아이콘 (이번)** |
|---|---|---|
| 배경 | 검정 불투명 | **투명** |
| 색 | 흑백 (코드가 색을 입힘) | **full-color (그린 색 그대로 나감)** |
| 이유 | 게임이 숫자 색을 매 프레임 바꿈 | 아이콘은 색이 고정 |

**이번엔 색을 직접 칠해 주세요.** 코드가 건드리지 않습니다.
1순위·2순위와 같은 형식(투명 PNG)으로 돌아왔습니다.

---

## 1. 8장 목록

| 파일 | 지금 이모지 | 쓰이는 곳 | 색 방향 |
|---|---|---|---|
| `ui_life.png` | 💛 | **플레이 중 항상** — 남은 생명(최대 3개 나란히) | 골드 `#ffd34d` 하트 |
| `ui_combo.png` | 🔥 | **플레이 중 항상** — `3 연속` 앞, 신기록 표시 | 주황→노랑 불꽃 |
| `ui_coin.png` | 💰 | 홈 보유 코인 · 상점 가격 · 미션 보상 (13곳) | 골드 코인 |
| `ui_trophy.png` | 🏆 | 홈 최고 기록 · 랭킹 버튼 · 결과 공유 (10곳) | 골드 트로피 |
| `ui_daily.png` | 📅 | 홈의 큰 `일일 챌린지` 버튼 | 시안 `#7cf6ff` 달력 |
| `ui_shop.png` | 🛒 | 홈 `상점` 버튼 | 골드 카트 |
| `ui_help.png` | 📖 | 홈 `방법` 버튼 | 밝은 회청색 책 |
| `ui_target.png` | 🎯 | 플레이 화면 `이 숫자에서 멈춰!` 앞 | 레드+화이트 과녁 |

> 나머지 40종(메달·랭크 배지·부스터·도움말 등)은 **이번에 안 합니다.**
> 랭크 배지와 부스터는 이미 전용 아트가 있고, 나머지는 노출이 적습니다.

---

## 2. 규격

| 항목 | 값 |
|---|---|
| 캔버스 | **96 × 96 px** (8장 전부 동일) |
| 형식 | PNG, **투명 배경**, full-color |
| 안전영역 | 그림은 가운데 **80 × 80** 안에 (사방 여백 8 px) |
| 광학 크기 | 둥근 것은 지름 76까지 / 가로로 긴 것은 폭 80 / 세로로 긴 것은 높이 80 |

### ⚠️ 선 굵기 하한 — 이번 발주에서 제일 중요합니다

이 아이콘들은 게임에서 **10.5 ~ 16 px**로 표시됩니다. 96px 캔버스가 **16%로 줄어듭니다.**

| 96px에서 | 16px 화면에서 | 결과 |
|---|---|---|
| 선 8 px | 1.25 px | 살아남음 ✅ |
| 선 3 px | 0.47 px | **사라짐** ❌ |

- **96px 기준 선·틈은 최소 8 px.** 참고도 B 패널에 8px와 3px를 16px로 줄인 비교가 있습니다
- 세부 묘사를 줄이고 **실루엣을 굵고 단순하게**. 작게 줄여서 뭔지 알아보는 게 전부입니다
- 글자·숫자를 넣지 마세요 (16px에서 절대 안 읽힙니다)

### 어두운 배경 위에 올라갑니다

배경은 딥네이비 `#0a0e1a`입니다.

- ❌ **어두운 외곽선 금지** — 배경에 묻혀 사라집니다
- 외곽선을 쓴다면 **채움색보다 밝게**
- 채도 높고 밝은 색으로. 어두운 부분은 아주 조금만

### 8장이 한 세트로 보여야 합니다

홈 화면에서 `🏆 랭킹` `🛒 상점` `📖 방법`이 **한 줄에 나란히** 섭니다.

- 같은 광원 방향(위에서 아래로), 같은 선 굵기, 같은 디테일 수준
- 같은 원근(정면 평면). 한 장만 비스듬하면 바로 티납니다
- 수치보다 **"같은 무게로 보이는지"**가 중요합니다

---

## 3. 프롬프트

공통으로 붙일 스타일:

```
Style: flat neon game UI icon, bold simple silhouette, thick strokes,
saturated bright colors on transparent background, soft inner highlight from above,
flat front view, no perspective, designed to stay readable at 16 pixels.
Negative: text, letters, numbers, dark outline, black stroke, thin lines, fine detail,
gradient background, drop shadow, 3D perspective, photorealistic, cluttered, watermark.
```

개별 프롬프트:

| 파일 | 프롬프트 (위 공통 스타일을 뒤에 붙일 것) |
|---|---|
| `ui_life` | `A bold rounded heart icon, warm gold (#ffd34d) fill with a brighter highlight on the upper left.` |
| `ui_combo` | `A bold stylized flame icon with two tongues, orange (#ff7a3a) at the base fading to yellow (#ffd34d) at the tip.` |
| `ui_coin` | `A thick round gold coin seen face on, bright gold rim and a slightly darker gold face, simple and chunky.` |
| `ui_trophy` | `A chunky gold trophy cup with two handles and a solid base, thick even strokes.` |
| `ui_daily` | `A simple calendar page icon with a thick border and two rings on top, cyan (#7cf6ff) on a dark navy face.` |
| `ui_shop` | `A chunky shopping cart icon in gold (#ffd34d), thick strokes, two bold round wheels.` |
| `ui_help` | `An open book icon seen from the front, two pages, pale blue-white (#dbe7ff) with a thicker spine.` |
| `ui_target` | `A bold target with three rings, red (#ff5a6e) outer ring and white middle ring, solid red center dot.` |

---

## 4. 납품 전 자가 검수

```python
from PIL import Image
for n in ['life','combo','coin','trophy','daily','shop','help','target']:
    im = Image.open(f'ui_{n}.png').convert('RGBA')
    a  = im.getchannel('A')
    bb = a.point(lambda v: 255 if v > 8 else 0).getbbox()
    print(n, im.size, 'bbox', bb, 'w=%d h=%d' % (bb[2]-bb[0], bb[3]-bb[1]),
          'alpha_max', a.getextrema()[1])
```

| 확인 | 기준 |
|---|---|
| 캔버스 | 8장 모두 `(96, 96)` |
| 투명 배경 | 네 모서리 8×8 픽셀의 알파 최대값 **0** |
| 안전영역 | 알파 경계상자가 x 8~88 · y 8~88 **안에** |
| 광학 크기 | 경계상자의 **긴 변이 72~80** (너무 작으면 혼자 작아 보입니다) |
| 불투명 영역 | 알파 최대값 **250 이상** |

**미리보기 2장을 꼭 같이 주세요** — 이번 발주에서 제일 중요한 검수입니다.

1. `icons_preview_96.png` — 8장을 96px로 가로로 나란히
2. `icons_preview_16.png` — **똑같은 8장을 16px로 줄여** 가로로 나란히

16px 줄에서 **무엇인지 못 알아보는 아이콘이 있으면 그 장은 다시 그려야 합니다.**
실제 게임에서 보이는 크기가 그 크기입니다.

---

## 5. 받은 뒤 제가 할 일

1. 위 검수 항목 전수 재측정 + **16px로 줄여 직접 확인**
2. WebP 전환·최적화 (8장 합계 40KB 이하 목표)
3. 이모지 → `<img>` 교체
   - 게임에 이미 `art(파일, 이모지, px)` 헬퍼가 있습니다. **못 불러오면 지금 이모지로 자동 복구**됩니다
   - `textContent`로 쓰던 자리(`#combo`, `#hearts` 등)를 `innerHTML`로 바꿔야 해서 20곳 가까이 손봅니다.
     닉네임처럼 사용자 입력이 섞이는 자리는 이스케이프를 확인하면서 바꾸겠습니다
4. 이모지 vs 아이콘 **나란히 비교**해서 확인받고, 더 나을 때만 배포

### 다음에 할 만한 것 (지금은 안 함)

라운드가 시작될 때 뜨는 배너 아이콘 5종 — `⚡ 롤링` `🔢 선택형` `🌟 골든` `📈 계단` `✖️ 곱하기`.
크게 뜨지만 잠깐이고, 이번 8장이 자리 잡은 뒤에 같은 톤으로 맞추는 게 안전합니다.
