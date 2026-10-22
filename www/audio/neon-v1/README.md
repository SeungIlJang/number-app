# 멈춰라 숫자 — 네온 아케이드 효과음 v1

직접 합성한 오리지널 효과음 20종입니다. 외부 샘플이나 기존 곡을 사용하지 않았습니다.
시안·골드 네온 디자인에 맞춘 맑은 전자음과 짧은 타격음을 사용했습니다.

- 형식: 48,000 Hz / 16-bit PCM / 스테레오 WAV
- 전체 플레이 미리듣기: `preview_sequence.wav` (15.6초)
- 개별 재생: `listen.html`을 브라우저에서 열기
- 파일별 이벤트·길이·피크: `manifest.json`

| 파일 | 용도 |
|---|---|
| ui_tap.wav | 메뉴·탭 선택 |
| game_start.wav | 게임 시작 |
| countdown.wav | 시작 전 카운트다운 |
| number_tick.wav | 일반 숫자 전환 |
| rolling_tick.wav | 롤링 숫자 전환 |
| slow_enter.wav | 슬로 모드 진입 |
| stop_tap.wav | STOP 입력의 짧은 타격음 |
| hit_good.wav | GOOD 판정 |
| hit_perfect.wav | PERFECT 판정 |
| combo_5.wav | 5연속 콤보 |
| chain_step.wav | 체인 중간 목표 성공 |
| chain_complete.wav | 체인 전체 완성 |
| rolling_success.wav | 롤링 성공·생명 획득 |
| golden_enter.wav | 골든 라운드 진입 |
| miss.wav | 일반 실패 |
| rolling_miss.wav | 패널티 없는 롤링 놓침 |
| life_continue.wav | 생명 소모 후 재개 |
| coin_reward.wav | 코인 획득·구매 완료 |
| rank_up.wav | 랭크 승급 |
| game_over.wav | 최종 게임 종료 |

## 적용 시 권장

숫자 틱은 가장 조용하게 두고, STOP 타격음은 판정음보다 낮게 재생합니다.
PERFECT 판정에는 GOOD를 중복 재생하지 않습니다.
체인 완성·롤링 성공 같은 큰 보상에는 짧은 일반 성공음을 생략하거나 줄입니다.
승급음은 결과 화면이 열린 뒤 재생해 종료음과 분리합니다.
소리만으로 목표 도달 시점을 알려주지 않도록 숫자 틱의 음높이는 일정하게 설계했습니다.
브라우저에서는 첫 터치 이후 오디오를 활성화하고, 틱은 미리 디코딩한 AudioBuffer로 재생하는 편이 좋습니다.

이번 작업은 효과음 파일 제작과 납품입니다. 게임의 기존 사운드 호출은 수정하지 않았습니다.
BGM은 포함하지 않았습니다.
