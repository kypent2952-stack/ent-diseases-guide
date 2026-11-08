# 이비인후과 건강 가이드 모음 (ent-diseases-guide)

이비인후과 전문의가 만든 건강 가이드들을 한곳에서 찾는 **허브 포털**입니다.

- 사이트: https://kypent2952-stack.github.io/ent-diseases-guide/ *(GitHub Pages 주소 — 배포 후 확인 필요)*

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 허브 첫 화면 — 분야별 카드, 검색·대상(환자/의료진) 필터, 곧 추가될 가이드 |
| `guides.json` | **가이드 목록의 단일 원본.** index.html이 읽어서 카드를 그립니다 |
| `assets/kyp-theme.css` | 공통 테마(색 토큰·다크모드·Pretendard). 다른 저장소에서도 재사용 |
| `tools/build_fallback.py` | guides.json → index.html 내장 폴백(정적 HTML + JSON) 재생성 |
| `sjogren.html` | 쇼그렌 가이드 **구판**(최신판은 sjogrens-guide로 이동 배너 포함) |
| `narcolepsy.html` | narcolepsy-guide로 보내는 리다이렉트 안내 페이지 |
| `archive/` | 이전 원본 보관 (`archive/narcolepsy.html`) |
| `404.html`, `sitemap.xml`, `robots.txt` | 사이트 기본 파일 |
| `docs/screenshots/` | 검수용 스크린샷 |

## 가이드 추가·수정하는 법

1. `guides.json`의 `guides` 배열에 항목을 추가합니다.
   ```json
   {
     "id": "voice-hygiene",
     "category": "voice",          // sleep | voice | oral | etc
     "title": "음성위생 가이드",
     "summary": "한 줄 설명",
     "audience": ["patient"],      // pro(의료진) / patient(환자), 둘 다 가능
     "url": "https://kypent2952-stack.github.io/voice-hygiene/",
     "keywords": ["검색어", "동의어"],
     "verified": false
   }
   ```
   준비 중 항목이 완성됐다면 `upcoming`에서 지워 주세요.
2. 폴백을 갱신합니다: `python3 tools/build_fallback.py`
3. 커밋·푸시하면 GitHub Pages에 반영됩니다.

> index.html은 `guides.json`을 먼저 읽고, 실패하면(파일로 직접 열기, 네트워크 오류) 내장 JSON을,
> JavaScript가 꺼져 있으면 정적 HTML 카드를 보여 줍니다. 2단계를 빼먹으면 이 폴백만 옛 목록으로 남습니다.

## 공통 테마 재사용

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://kypent2952-stack.github.io/ent-diseases-guide/assets/kyp-theme.css">
```

토큰 목록과 사용 가능한 클래스는 `assets/kyp-theme.css` 상단 주석에 정리돼 있습니다.
강조색 `#1F5FA8`, 시스템 다크모드 자동 대응, `<html data-theme="dark|light">`로 강제 가능.

## 로컬 미리보기

```bash
# 상위 폴더에서 실행해야 404.html의 /ent-diseases-guide/ 절대 경로가 맞습니다
cd .. && python3 -m http.server 8000
# → http://localhost:8000/ent-diseases-guide/
```

## 안내

이 사이트의 내용은 건강 정보 제공용이며 개인의 진단·치료를 대신하지 않습니다.
