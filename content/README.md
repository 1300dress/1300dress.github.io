# 프로젝트 원고 (content/projects/NN.json)

상세 페이지 6개는 이 폴더의 JSON을 `tools/build.py`가 `projects/NN.html`로 만듭니다.
원고와 미디어 순서는 JSON에만 있고, 모양은 `assets/journal.css`가 맡습니다.

```
python3 tools/build.py        # JSON을 고친 뒤 실행
python3 -m http.server 4173   # 미리보기: http://127.0.0.1:4173/projects/01.html
```

## 페이지 정보

| 키 | 내용 |
|---|---|
| `num` | `"01"`~`"06"`. 파일 이름, 이전/다음 순서 |
| `status` | `"dummy"`면 머리에 '임시 시안' 안내가 뜸. 실제 원고로 다 바꾸면 지움 |
| `category` | 번호 옆 작은 글씨 (목차 오른쪽 캡션과 같게) |
| `title`, `why` | 제목과 WHY 질문 (목차 호버 질문과 같게) |
| `dek` | 도입 문단 |
| `meta` | `[{label, value}]`. `value`가 비면 `todo` 문구가 쑥색 빈칸으로 뜸 |
| `credits` | `[{label, value, href?}]`. 페이지 끝 링크·크레딧 |
| `body` | 본문 블록 목록. 위에서 아래로 그대로 그려짐 |

## 본문 블록과 노션 대응

| 노션 블록 | `type` | 키 |
|---|---|---|
| 제목 2 (Situation / Solution / Result) | `section` | `label`, `title`(선택: 한 줄 부제) |
| 텍스트 | `p` | `text` (`<em>`, `<a>`, `<br>` 사용 가능) |
| 인용 | `quote` | `text`, `cite`(선택) |
| 이미지 | `image` | `src`, `alt`, `caption`, `width`, `ratio`(선택) |
| 열 2개에 이미지 2장 | `pair` | `items: [{src, alt}, {src, alt}]`, `caption`, `width` |
| 이미지 여러 장(캐러셀) | `carousel` | `items: [{src, alt}…]`, `caption` (4:5 낱장을 옆으로 넘김) |
| 동영상 | `video` | `src`, `poster`, `ratio`(`"9:16"`·`"16:9"`…), `caption`, `layout: "aside"`(선택) |
| 구분선 | `break` | — |

`width`는 사진 크기입니다. `text`(본문 폭) · `wide`(본문보다 넓게) · `full`(화면 끝까지) · `small`(작게, 가운데).

세로 영상(`9:16`)에 `layout: "aside"`를 주면 넓은 화면에서 캡션이 영상 옆에 섭니다.

## 노션 원고 → JSON 규칙

원고는 노션 'subin teahouse 사이트 채우기' › '포트폴리오 작업' 표의 **각 행 본문**입니다.

- 페이지 머리: 작업명 → `title`, WHY 질문 → `why`, 도입문 → `dek`, 목록 메타 → `category`,
  연도 · 매체·클라이언트 · 역할 · 형식 → `meta`, 외부 링크 → `credits`
- 제목 2 `Situation · 부제` → `section` (`label`, `title`)
- 이미지 캡션 맨 앞 `[넓게]` `[끝까지]` `[작게]` → `width: wide | full | small` (없으면 `text`)
- 동영상 캡션 맨 앞 `[옆캡션]` → `layout: "aside"`
- 제목이 `캐러셀`로 시작하는 토글 안의 이미지들 → `carousel` (토글 제목의 `캐러셀:` 뒤가 캡션)
- 열 2개에 이미지 한 장씩 → `pair`
- `✎`로 시작하는 회색 글과 회색 안내 상자는 옮기지 않음
- '공개 가능'이 체크되지 않은 행의 이미지·영상은 사이트에 올리지 않음

## 미디어 파일

- 사진·영상은 `assets/media/NN/`에 넣고 `src`에 `assets/media/01/cover.jpg`처럼 적습니다. 외부 URL도 됩니다.
- 영상은 mp4(H.264)로, `poster`에 첫 장면 이미지를 함께 넣습니다. 모바일에서도 재생됩니다.
- 사진은 긴 변 2000px 안쪽 jpg/webp를 권장합니다.

## 임시 콘텐츠 걷어 내기

- 임시 블록에는 `"dummy": true`가 붙어 있습니다. 실제 원고로 바꾸면 이 표시를 지웁니다.
- 임시 이미지·영상은 모두 `assets/dummy/`에 있습니다(`tools/make_dummy.py`로 만듦). 다 바꾼 뒤 폴더째 지우면 됩니다.
- `grep -l '"dummy": true' content/projects/*.json`으로 아직 남은 페이지를 찾을 수 있습니다.
