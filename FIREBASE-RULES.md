# 멈춰라 숫자 — Firestore 보안 규칙 안내

## ✅ 2026-11-12 게시 완료

콘솔에 적용됐고, 라이브(`games/number.html` v3.8)에서 읽기 경로를 직접 확인했습니다 —
일일 챌린지 → 🌍 오늘의 랭킹이 **"오늘 첫 기록의 주인공이 되어보세요"** 로 바뀌었습니다
(규칙이 닫혀 있으면 403 → "아직 열리지 않았어요"가 떴을 자리).

아래는 그때 적용한 내용과 이유 기록입니다.

---

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

### 2-1. 합쳐둔 전체 규칙 (2026-11-12 기준)

⚠️ **이 프로젝트는 갤로그·한발·뽑기 등 다른 게임과 같이 씁니다.**
아래는 그날 콘솔에 있던 내용에 일일 랭킹 블록 하나만 끼워 넣은 것입니다.
**그 뒤 다른 게임이 규칙을 고쳤을 수 있으니, 통째로 덮어쓰기 전에 콘솔의 현재 내용과 먼저 대조하세요.**

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /scores/{id} {
      allow read: if true;
      allow write: if request.resource.data.keys().hasOnly(['name','stage','kills','ts'])
        && request.resource.data.name is string && request.resource.data.name.size() <= 16
        && request.resource.data.stage is int && request.resource.data.stage >= 0 && request.resource.data.stage <= 100
        && request.resource.data.kills is int && request.resource.data.kills >= 0 && request.resource.data.kills <= 10000000;
    }
    match /hanbal_scores/{doc} {
      allow read: if true;
      allow write: if request.resource.data.score is int
        && request.resource.data.score >= 0;
    }
    match /ppopgi_lb/{doc} {
      allow read: if true;
      allow write: if request.resource.data.keys().hasOnly(['name','best','total','dex','secret','title'])
        && request.resource.data.name is string && request.resource.data.name.size() <= 16
        && request.resource.data.best is int && request.resource.data.best >= 0 && request.resource.data.best <= 1000000
        && request.resource.data.total is int && request.resource.data.total >= 0 && request.resource.data.total <= 10000000
        && request.resource.data.dex is int && request.resource.data.dex >= 0 && request.resource.data.dex <= 200
        && request.resource.data.secret is int && request.resource.data.secret >= 0 && request.resource.data.secret <= 50
        && request.resource.data.title is string && request.resource.data.title.size() <= 24;
    }
    match /number_lb/{doc} {
      allow read: if true;
      allow write: if request.resource.data.keys().hasOnly(['name','score','ts'])
        && request.resource.data.name is string && request.resource.data.name.size() <= 16
        && request.resource.data.score is int && request.resource.data.score >= 0 && request.resource.data.score <= 100000000;
    }

    // 멈춰라 숫자 — 일일 챌린지 랭킹 (2026-11-12 추가)
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

    // 갤로그 원격 밸런스 설정 — 읽기는 누구나, 쓰기는 관리자 1명만
    match /config/tune {
      allow read: if true;
      allow write: if request.auth != null
        && request.auth.uid == 'XgcoWnAnXqWALdpIL7I9JCPKLAO2'
        && request.resource.data.keys().hasOnly(['tune','ts','by'])
        && request.resource.data.tune is map
        && request.resource.data.tune.size() <= 40;
    }
  }
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

> 📌 `name.size() <= 16` 의 단위는 **글자 수**입니다(바이트 아님 — 바이트는 `toUtf8().size()`).
> 한글 닉네임 8자도 8로 세므로 안전합니다. 기본 닉네임은 `도전자XXXX`(7자)라
> `size() > 0` 에 걸릴 일도 없습니다. 닉네임 변경은 코드가 8자로 자릅니다.

## 4. 확인 방법

규칙을 게시한 뒤 게임에서 **📅 일일 챌린지 → 🌍 오늘의 랭킹** 을 열어보세요.
"아직 열리지 않았어요" 대신 순위 목록(또는 "오늘 첫 기록의 주인공이 되어보세요")이 나오면 성공입니다.

---

## 참고 — 기존 `number_lb`의 제약

전체 랭킹이 쓰는 `number_lb` 컬렉션은 현재 **`{name, score, ts}` 세 필드만** 허용합니다.
여기에 필드를 하나라도 더 넣으면 **등록이 통째로 거부**되니,
전체 랭킹 쪽을 손볼 때는 이 제약을 먼저 확인하세요. (코드에도 주석으로 적어뒀습니다.)
