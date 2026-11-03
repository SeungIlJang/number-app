# 멈춰라 숫자 — Firestore 보안 규칙 안내

일일 챌린지 **글로벌 랭킹**을 켜려면 규칙에 컬렉션 하나를 추가해야 합니다.
**게임 코드는 이미 준비돼 있습니다.** 규칙만 열면 수정·재배포 없이 바로 동작합니다.
(열기 전까지는 "아직 글로벌 일일 랭킹이 열리지 않았어요"가 뜨고 내 기록은 로컬에 저장됩니다.)

---

## 1. 어디서 바꾸나

[Firebase 콘솔](https://console.firebase.google.com/) → 프로젝트 **gallog-return-be90f**
→ 왼쪽 **Firestore Database** → 상단 **규칙(Rules)** 탭

## 2. 추가할 규칙

기존 `number_lb` 규칙은 **그대로 두고**, `match /databases/{database}/documents { … }` 안에
아래 블록만 추가한 뒤 **게시(Publish)** 를 누르세요.

```
// 멈춰라 숫자 — 일일 챌린지 랭킹
// 경로: number_daily/{YYYY-MM-DD}/scores/{기기ID}
match /number_daily/{day}/scores/{uid} {
  allow read: if true;
  allow create, update: if
       request.resource.data.keys().hasOnly(['name','score','hits','ts'])
    && request.resource.data.name is string
    && request.resource.data.name.size() > 0
    && request.resource.data.name.size() <= 16
    && request.resource.data.score is int
    && request.resource.data.score >= 0
    && request.resource.data.score <= 5000000
    && request.resource.data.hits is int
    && request.resource.data.hits >= 0
    && request.resource.data.hits <= 100000
    && day.matches('^[0-9]{4}-[0-9]{2}-[0-9]{2}$');
  allow delete: if false;
}
```

## 3. 이 구조를 고른 이유

| 선택 | 이유 |
|---|---|
| **날짜를 경로에** (`number_daily/{날짜}/scores/…`) | 문서 안에 날짜 필드를 두면 `where(날짜) + orderBy(점수)` 조합이라 **복합 색인을 따로 만들어야** 합니다. 경로에 넣으면 점수 단일 정렬이라 색인이 자동으로 됩니다 |
| **문서 ID = 기기 ID** | `setDoc` 덮어쓰기라 **한 사람당 한 줄**이 저절로 보장됩니다. 기존 `number_lb`에서 한 사람이 상위권을 여러 줄 차지하던 문제가 구조적으로 안 생깁니다 |
| **필드 화이트리스트** (`hasOnly`) | 장난 데이터로 문서를 부풀리는 걸 막습니다 |
| **점수 상한** | 터무니없는 값이 1위를 차지하는 걸 막습니다 |
| **`allow delete: if false`** | 남의 기록을 지울 수 없게 |

> ⚠️ 로그인이 없는 게임이라 **"내 기기 ID 자리에만 쓸 수 있다"는 보장은 없습니다.**
> 마음먹으면 남의 자리에 덮어쓸 수 있습니다. 익명 로그인(Firebase Anonymous Auth)을 붙이고
> `allow create, update: if request.auth != null && request.auth.uid == uid` 를 추가하면 막을 수 있는데,
> 지금 규모에서는 과한 작업이라 넣지 않았습니다. 필요해지면 그때 올리면 됩니다.

## 4. 확인 방법

규칙을 게시한 뒤 게임에서 **📅 일일 챌린지 → 🌍 오늘의 랭킹** 을 열어보세요.
"아직 열리지 않았어요" 대신 순위 목록(또는 "오늘 첫 기록의 주인공이 되어보세요")이 나오면 성공입니다.

---

## 참고 — 기존 `number_lb`의 제약

전체 랭킹이 쓰는 `number_lb` 컬렉션은 현재 **`{name, score, ts}` 세 필드만** 허용합니다.
여기에 필드를 하나라도 더 넣으면 **등록이 통째로 거부**되니,
전체 랭킹 쪽을 손볼 때는 이 제약을 먼저 확인하세요. (코드에도 주석으로 적어뒀습니다.)
