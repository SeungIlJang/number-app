// www/ 를 games 레포의 원본과 맞춘다.
//
// 이 앱은 OTA 래퍼다. www/index.html 이 seungiljang.github.io/games/number.html 을
// 받아 document.write 로 띄우므로, 평소 게임 변경은 games 레포 푸시만으로 반영된다.
// www/ 안의 것들은 그래도 최신이어야 한다:
//
//   game.html            비행기 모드/네트워크 실패 시 쓰는 오프라인 폴백.
//                        games/number.html 과 바이트 동일해야 한다.
//   audio/number/sfx/    OTA HTML 을 document.write 로 올리면 상대경로가 로컬로
//   img/number/play/     풀린다. 그래서 에셋이 앱 번들에도 있어야 하고, 없으면
//   img/number/ui/       앱에서만 소리/아트가 빠진다 (로컬 웹 테스트로는 안 잡힌다).
//
// 이 세 폴더는 games/number.html 이 실제로 참조하는 경로다:
//   SFX_DIR='audio/number/sfx/'  PLAY_DIR='img/number/play/'  ART='img/number/ui/'
// games 레포에 같이 있는 audio/number/neon-v1/, img/number/neon-v2/ 는 아트 제작
// 원본 드롭이라 런타임에 안 쓴다. 앱 번들만 무겁게 하므로 복사하지 않는다.
//
// index.html(래퍼 자체)은 이 레포가 원본이므로 건드리지 않는다.
//
// ⚠️ 예전 package.json 의 copyweb 에는 idle-hero 에서 복사해 온 한 줄 스크립트가
//    남아 있었다. www/ 를 통째로 지우고 ../idle-hero/ 를 넣는 내용이라, 모르고
//    npm run sync 를 치면 이 앱 번들이 사라졌다. 지금은 games 레포만 바라본다.

import { existsSync, statSync, readFileSync, writeFileSync, mkdirSync, cpSync, rmSync, readdirSync } from 'node:fs';
import { resolve, dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const app = resolve(here, '..');
const games = resolve(app, '..', 'games');

const SRC_HTML = resolve(games, 'number.html');
const DST_HTML = resolve(app, 'www', 'game.html');

// games 레포 쪽 런타임 에셋 경로 그대로 www 아래에 들어간다.
const ASSET_DIRS = [
  'audio/number/sfx',
  'img/number/play',
  'img/number/ui',
];

function die(msg) {
  console.error('sync-web: ' + msg);
  process.exit(1);
}

// 뭐든 지우기 전에 원본이 다 있는지 먼저 본다. 중간에 멈추면 반쯤 지워진
// www/ 가 남는다.
if (!existsSync(SRC_HTML)) {
  die(`원본이 없다: ${SRC_HTML}\n  games 레포가 ../games 에 체크아웃돼 있어야 한다.`);
}
for (const dir of ASSET_DIRS) {
  const src = resolve(games, dir);
  if (!existsSync(src)) die(`원본 에셋 폴더가 없다: ${src}`);
}

// 바이트 그대로 복사한다. 줄끝을 바꾸면 두 벌이 cmp 로 달라진다.
const html = readFileSync(SRC_HTML);
mkdirSync(dirname(DST_HTML), { recursive: true });
writeFileSync(DST_HTML, html);
if (!readFileSync(DST_HTML).equals(html)) die('game.html 복사본이 원본과 다르다');

// 폴더 안을 재귀로 돌며 상대경로 목록을 만든다. 복사 후 검증에 쓴다.
function listFiles(root, base = root) {
  const out = [];
  for (const name of readdirSync(root)) {
    const p = join(root, name);
    if (statSync(p).isDirectory()) out.push(...listFiles(p, base));
    else out.push(relative(base, p));
  }
  return out.sort();
}

const counts = [];
for (const dir of ASSET_DIRS) {
  const src = resolve(games, dir);
  const dst = resolve(app, 'www', dir);

  rmSync(dst, { recursive: true, force: true });
  mkdirSync(dst, { recursive: true });
  cpSync(src, dst, { recursive: true });

  // 복사본이 원본과 같은지 파일 단위로 확인한 뒤에만 성공으로 처리한다.
  const want = listFiles(src);
  const got = listFiles(dst);
  if (want.join('\n') !== got.join('\n')) die(`${dir}: 복사된 파일 목록이 원본과 다르다`);
  for (const f of want) {
    if (!readFileSync(join(dst, f)).equals(readFileSync(join(src, f)))) {
      die(`${dir}/${f}: 복사본이 원본과 다르다`);
    }
  }
  counts.push(`${dir}  ${want.length} files`);
}

const ver = (html.toString('utf8').match(/v\d+\.\d+[^<\n]*/) || ['(버전 문자열 못 찾음)'])[0];
console.log(`sync-web: game.html  ${html.length} bytes  ${ver}`);
for (const line of counts) console.log(`sync-web: ${line}`);
