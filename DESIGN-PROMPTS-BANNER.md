# 멈춰라 숫자 — 5순위 발주서 **라운드 배너 아이콘 6종** (neon-v3)

> 라운드가 시작될 때 화면 가운데 0.9초간 뜨는 배너입니다.
> **"이번 라운드는 규칙이 다르다"를 알리는 자리**라 플레이어가 반드시 봅니다.
> 지금은 이모지라 기기마다 모양이 다릅니다.

**산출물: 6장 (각 96×96, 투명 PNG, full-color)**
**저장 위치: `D:/AI/workspace/game/images/number/neon-v3/`** (프로젝트 복사·코드 수정·커밋 금지)
**규격 참고도: `images/number/_brief/banner_metrics.png` — 먼저 열어보세요**

---

## 0. 4순위와 같은 형식입니다

| | 4순위 HUD 아이콘 | **5순위 (이번)** |
|---|---|---|
| 캔버스 | 96×96 | **96×96 동일** |
| 형식 | 투명 PNG, full-color | **동일** |
| 표시 크기 | 10.5~16 px | **28~34 px** |

**달라진 건 표시 크기뿐입니다.** 4순위는 16px로 줄어들어 선 굵기 하한(8px)이 빡빡했는데,
이번엔 28~34px라 여유가 있습니다. 그래도 세부를 과하게 넣지는 마세요 — 아래 1절이 더 중요합니다.

---

## 1. ⚠️ 가장 중요 — 이미 들어간 8종과 한 가족이어야 합니다

게임에는 이미 HUD 아이콘 8종이 들어가 있습니다. 새 6종이 그 옆에 섰을 때
**"같은 사람이 그렸다"로 보여야 합니다.** 참고도 A 패널에 실물 8장을 붙여뒀습니다.

실제 파일도 열어보세요:

```
D:/AI/workspace/game/games/img/number/ui/ui_life.webp
                                         ui_combo.webp   ui_coin.webp    ui_trophy.webp
                                         ui_daily.webp   ui_shop.webp    ui_help.webp
                                         ui_target.webp
```

맞춰야 할 것:

- **같은 광원** — 위에서 아래로, 상단에 부드러운 하이라이트
- **같은 선 굵기**와 **같은 디테일 수준**
- **정면 평면** — 원근·기울임 없음
- **어두운 외곽선 금지** — 배경이 딥네이비(`#0a0e1a`)라 검은 테두리는 사라집니다
- 채도 높고 밝은 색

---

## 2. 6장 목록

| 파일 | 지금 | 배너 문구 | 색 |
|---|---|---|---|
| `ui_roll.png` | ⚡ | **롤링!** 감으로 STOP | 퍼플 `#c9a3ff` |
| `ui_golden.png` | 🌟 | **골든 라운드!** 점수 ×2 | 골드 `#ffd34d` |
| `ui_stepup.png` | 📈 | **계단!** 간격이 커져요 | 시안 `#7cf6ff` |
| `ui_mul.png` | ✖️ | **곱하기!** ×2 | 퍼플 `#c9a3ff` |
| `ui_choice.png` | 🔢 | **다음 숫자는?** · 5.0초 | 시안 `#7cf6ff` |
| `ui_fail.png` | ❌ | **틀렸어요** / **실패!** | 레드 `#ff5a6e` |

### 「실패」가 5종에서 6종으로 늘어난 이유

처음엔 라운드 타입 5종만 생각했는데, 세어보니 **❌ 가 가장 많이 보입니다.**
배너(`❌ 틀렸어요`, `❌ 19 → 목표 22`)에도 뜨고 **게임오버 제목(`❌ 실패!`, 40px)에도** 뜹니다.
매 판 반드시 한 번은 보는 아이콘이라 같이 넣었습니다.

### 이번에 안 하는 것

`🔗 체인` `🔥 슬로모` `💛 생명` `🎉 승급` 배너도 있지만,
앞의 셋은 이미 전용 아트가 있고(`chain_link` · `ui_combo` · `ui_life`) 승급은 아주 드뭅니다.

---

## 3. ⚠️ 곱하기(✖️)와 실패(❌)는 반드시 달라 보여야 합니다

둘 다 X 모양이라 **이번 발주에서 제일 헷갈리기 쉬운 부분**입니다. 참고도 B 패널을 보세요.

| | 곱하기 `ui_mul` | 실패 `ui_fail` |
|---|---|---|
| 형태 | **선만** — 가는 사선 십자 | **면** — 굵은 X 가 채워진 둥근 사각 안에 |
| 굵기 | 가늘게 | 굵게 |
| 색 | 퍼플 `#c9a3ff` | 레드 `#ff5a6e` |
| 읽히는 뜻 | 수학 기호 | "틀렸다" |

**16px로 줄여 나란히 놓고 헷갈리면 다시 그려주세요.**

---

## 4. 프롬프트

공통으로 붙일 스타일 (4순위와 동일):

```
Style: flat neon game UI icon, bold simple silhouette, thick strokes,
saturated bright colors on transparent background, soft inner highlight from above,
flat front view, no perspective, part of a matching icon set.
Negative: text, letters, numbers, dark outline, black stroke, thin lines, fine detail,
gradient background, drop shadow, 3D perspective, photorealistic, cluttered, watermark.
```

| 파일 | 프롬프트 (위 공통 스타일을 뒤에 붙일 것) |
|---|---|
| `ui_roll` | `A bold lightning bolt icon, bright violet (#c9a3ff) with a lighter core, chunky angular zigzag.` |
| `ui_golden` | `A bold five-pointed star icon in warm gold (#ffd34d), slightly rounded points, one small sparkle at the upper right.` |
| `ui_stepup` | `Three ascending blocks like rising stairs, cyan (#7cf6ff), chunky and even, with a small upward arrow above the tallest block.` |
| `ui_mul` | `A multiplication sign: two thin diagonal strokes crossing, violet (#c9a3ff), no background shape, no outline, clean geometric.` |
| `ui_choice` | `Three small rounded cards side by side, the middle one raised and highlighted, cyan (#7cf6ff), suggesting a choice between options.` |
| `ui_fail` | `A thick white X mark inside a filled rounded square of red (#ff5a6e), bold and compact.` |

---

## 5. 납품 전 자가 검수

4순위와 같은 기준입니다.

```python
from PIL import Image
for n in ['roll','golden','stepup','mul','choice','fail']:
    im = Image.open(f'ui_{n}.png').convert('RGBA')
    a  = im.getchannel('A')
    bb = a.point(lambda v: 255 if v > 8 else 0).getbbox()
    print(n, im.size, 'bbox', bb, 'w=%d h=%d' % (bb[2]-bb[0], bb[3]-bb[1]),
          'alpha_max', a.getextrema()[1])
```

| 확인 | 기준 |
|---|---|
| 캔버스 | 6장 모두 `(96, 96)` |
| 투명 배경 | 네 모서리 8×8 픽셀의 알파 최대값 **0** |
| 안전영역 | 알파 경계상자가 x 8~88 · y 8~88 **안에** |
| 광학 크기 | 경계상자의 **긴 변이 72~80** |
| 불투명 영역 | 알파 최대값 **250 이상** |

**미리보기 3장을 같이 주세요:**

1. `banner_preview_96.png` — 새 6장을 96px로 나란히
2. `banner_preview_28.png` — 똑같은 6장을 **28px**로 줄여 나란히 (실제 배너 크기)
3. `banner_preview_family.png` — **기존 8장 + 새 6장을 한 줄에 섞어서** 96px로

3번이 이번 검수의 핵심입니다. 섞어 놓고 어느 게 새로 그린 건지 티가 나면 다시 맞춰야 합니다.

---

## 6. 받은 뒤 제가 할 일

1. 위 검수 전수 재측정 + **28px로 줄여 직접 확인** + 기존 8종과 섞어서 눈으로 대조
2. `python tools/apply_icons.py` 에 6개 이름만 추가해 WebP 전개 (4순위와 같은 파이프라인)
3. 배너에 끼우기 — `banner()` 가 `textContent` 라 `innerHTML` 로 바꿔야 합니다.
   호출 11곳을 전부 확인했고 **고정 문자열 아니면 숫자만** 들어갑니다
   (`nC`, `rule.m`, 남은 시간, 멈춘 값·목표값, 랭크 이름은 전부 코드 상수).
   닉네임 같은 사용자 입력이 들어가는 자리는 없습니다.
4. 못 불러오면 지금 이모지로 자동 복구 — 기존 `uic()` 헬퍼가 그대로 처리합니다
5. 이모지 vs 아이콘 **나란히 비교**해서 확인받고, 더 나을 때만 배포
