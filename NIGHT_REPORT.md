# 야간 작업 보고서 — 2026-11-08

브랜치: `claude/night-2026-11-08` (main 푸시·PR 없음)

## 바뀐 것

1. **허브 첫 화면 `index.html` 신설**
   - 히어로 “이비인후과 건강 가이드 모음”, 분야별 카드(수면 / 음성·후두 / 구강·침샘·자가면역 / 기타*)
   - 카드마다 제목·한 줄 설명·대상 배지(의료진/환자)·바로가기 버튼
   - 검색(제목·설명·키워드·분야, 여러 단어 AND, 대소문자 무시) + 대상 필터(전체/환자/의료진), 결과 수 안내(aria-live), 결과 없음 → “검색 초기화”
   - `?q=검색어` 주소 지원(404 페이지 검색창이 이걸 씀)
   - “곧 추가될 가이드”: 구강내 병변 / 수면다원검사 안내 / 음성위생
   - \* ‘기타’ 분야는 현재 가이드가 없어 화면에 표시되지 않음(항목이 생기면 자동으로 나타남)
2. **`guides.json`** — 가이드 목록 단일 원본. index가 fetch로 읽고, 실패 시 내장 JSON → JS 꺼짐 시 정적 HTML 카드 순으로 폴백. 폴백은 `tools/build_fallback.py`로 자동 생성.
3. **`schogren` → `sjogren.html`** (git mv로 이력 보존). 본문 맨 위에 “최신판은 sjogrens-guide로 이동” 배너, description 메타·Pretendard 링크·제목 “(구판)” 추가. 그 외 본문은 손대지 않음.
   - 옛 주소 `/schogren`으로 들어오면 404.html이 `sjogren.html`로 자동 이동.
4. **`narcolepsy.html`** — 원본은 `archive/narcolepsy.html`로 이동(바이트 동일, git mv). 그 자리는 narcolepsy-guide로 보내는 안내 페이지(meta refresh 3초 + 버튼 링크 + canonical + noindex).
5. **`404.html`**(검색창 포함), **`sitemap.xml`**, **`robots.txt`**, **`README.md`** 추가.
6. **`assets/kyp-theme.css`** — 공통 테마. 색 토큰(:root), 다크모드(시스템 + `data-theme` 강제), Pretendard 글꼴 스택, 버튼·카드·배지·배너·입력창·건너뛰기 링크. 상단에 토큰 문서 주석.

## 검증 결과 (로컬 서버 + Playwright)

| 항목 | 결과 |
|---|---|
| 375px 가로 스크롤 | 없음 (scrollWidth 375) — index / narcolepsy / 404 / sjogren 모두 |
| 1280px | 3열 카드 정상 |
| 다크모드 | 정상 (스크린샷 `docs/screenshots/index-1280-dark.png`) |
| 검색 “기면증” | 1개 · “cpap”(소문자) 1개 · 의료진 필터 3개 · “zzzz” 결과 없음 → 초기화 시 5개 |
| guides.json 차단 시 | 내장 JSON으로 5개 렌더, 검색 동작 |
| JS 꺼짐 | 정적 카드 5개 표시 |
| 404 → `/schogren` | `sjogren.html`로 이동 확인(Pages 404 동작을 모의) |
| 404 검색창 | `?q=쇼그렌` → 1개 |
| 콘솔 에러 | **우리 코드 에러 0.** 유일한 에러는 이 작업 환경에서 외부 CDN(jsdelivr) 접속이 막혀 Pretendard CSS를 못 받은 것 |
| 명도 대비 | 주요 글자/배경 조합 모두 4.5:1 이상 (라이트 최저 5.61, 다크 최저 6.75) |

※ `sjogren.html`의 “Chart is not defined” 에러는 기존 코드가 쓰는 tailwind·chart.js CDN이 이 환경에서 막혀서 나는 것으로, 실제 사이트에선 정상일 것으로 봅니다(기존 동작 그대로).

스크린샷: `docs/screenshots/` (index 375/1280/다크/결과없음, narcolepsy 안내, 404)

## 원장님 확인 체크리스트

- [ ] **주소 확인 필요** — 이 환경은 외부 접속이 막혀 아래 주소를 실제로 열어보지 못했습니다. `guides.json`의 `url`을 확인 후 `verified: true`로 바꿔 주세요.
  - [ ] https://kypent2952-stack.github.io/ent-diseases-guide/ (이 허브 — Settings → Pages에서 main 브랜치 배포 켜져 있는지)
  - [ ] https://kypent2952-stack.github.io/narcolepsy-guide/
  - [ ] https://kypent2952-stack.github.io/sjogrens-guide/
  - [ ] https://kypent2952-stack.github.io/speech/
  - [ ] https://kypent-cpap.netlify.app — CPAP 관련이 맞는지, 카드 제목·설명(“CPAP 양압기 안내”, 환자용)이 내용과 맞는지
  - [ ] ⚠️ **AASM 가이드**: 저장소 이름이 `kypent2952.github.io`인데 계정이 `kypent2952-stack`이라, 사용자 사이트(루트 주소)로 동작하지 않고 `https://kypent2952-stack.github.io/kypent2952.github.io/`에 게시될 가능성이 큽니다. 일단 그 주소로 넣어 두었습니다. 루트 주소를 원하시면 저장소 이름을 `kypent2952-stack.github.io`로 바꾸는 방법이 있습니다(바꾸면 guides.json url도 수정).
- [ ] 각 카드의 한 줄 설명·대상(의료진/환자) 구분이 의도와 맞는지
- [ ] 히어로 문구(“이비인후과 전문의가 직접 만든 …”) 괜찮은지 — 병원명·원장님 성함을 넣고 싶으시면 index.html 히어로 부분 수정
- [ ] “곧 추가될 가이드” 3개 설명 문구
- [ ] 휴대폰에서 실제 주소로 열어 Pretendard 글꼴 적용 확인
- [ ] 브랜치 검토 후 main 머지 (PR은 만들지 않았습니다)

## 다른 저장소가 머지된 뒤 할 일

1. **sjogrens-guide** (오늘 밤 index.html 재구축 중) 머지·배포 후
   - 주소 확인 → `guides.json` sjogren 항목 `verified: true`
   - 새 판에 이 허브로 돌아오는 링크(“← 가이드 모음”) 추가 권장
   - 원하시면 `sjogren.html`도 narcolepsy처럼 리다이렉트 페이지로 바꾸고 원본은 `archive/`로 (지금은 구판을 볼 수 있게 남겨 둠)
2. **speech** (SOVT 앱 수리 중) 머지·배포 후 주소 확인 → `verified: true`, 카드 설명이 실제 기능과 맞는지 점검
3. **공통 테마 적용**: 각 저장소에 `assets/kyp-theme.css`를 복사(또는 허브 주소로 링크)하면 색·글꼴이 통일됩니다. 다른 세션에서 각자 만든 스타일과 토큰 이름이 겹치지 않도록 `--kyp-` 접두사를 썼습니다.
4. 각 가이드 페이지 상단/하단에 허브 링크 넣기 → 서로 오갈 수 있게
5. 가이드를 추가할 때마다: `guides.json` 수정 → `python3 tools/build_fallback.py` → 필요하면 `sitemap.xml`에 추가

## 참고·한계

- GitHub Pages **프로젝트 사이트**의 `robots.txt`(`/ent-diseases-guide/robots.txt`)는 검색엔진이 읽지 않습니다(도메인 루트만 읽음). 파일은 요청대로 넣어 두었고, 실제 효과를 내려면 사용자 사이트(`kypent2952-stack.github.io` 저장소) 루트에 두어야 합니다. 대신 리다이렉트·404 페이지에는 `noindex` 메타를 넣어 두었습니다.
- `sitemap.xml`에는 허브와 쇼그렌 구판만 넣었습니다(외부 저장소 페이지는 각 저장소 사이트맵에서 관리하는 것이 원칙).
- 404.html은 하위 경로에서도 열리기 때문에 `/ent-diseases-guide/…` 절대 경로를 씁니다. 저장소 이름을 바꾸면 이 경로도 바꿔야 합니다.
- `archive/narcolepsy.html`은 원본 그대로라 Pretendard·배너가 없습니다(의도적으로 무수정 보관).
