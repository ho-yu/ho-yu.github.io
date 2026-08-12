# 글 작성 가이드

GitHub 블로그가 처음이어도 이 문서만 보고 글 하나를 끝까지 올릴 수 있도록 정리했다.
위에서부터 순서대로 따라 하면 된다.

> 이 문서는 사이트에 게시되지 않는다. 저장소에서만 보이는 참고 문서다.

---

## 목차

1. [30초 요약](#1-30초-요약)
2. [글 하나 올리는 전체 과정](#2-글-하나-올리는-전체-과정)
3. [파일 이름 규칙](#3-파일-이름-규칙)
4. [Front Matter (글 맨 위 설정)](#4-front-matter-글-맨-위-설정)
5. [Notes 작성법](#5-notes-작성법)
6. [Projects 작성법](#6-projects-작성법)
7. [Troubleshooting 작성법](#7-troubleshooting-작성법)
8. [Retrospectives 작성법](#8-retrospectives-작성법)
9. [본문 문법 치트시트](#9-본문-문법-치트시트)
10. [이미지 넣기](#10-이미지-넣기)
11. [확인하고 올리기](#11-확인하고-올리기)
12. [글이 안 보일 때](#12-글이-안-보일-때)
13. [최종 체크리스트](#13-최종-체크리스트)

---

## 1. 30초 요약

```text
templates/ 에서 템플릿 복사
        ↓
_posts/2026-08-13-my-first-note.md 로 붙여넣기
        ↓
맨 위 4줄(title, date, categories, tags) 채우기
        ↓
본문 작성
        ↓
git add . → git commit → git push
        ↓
1~2분 뒤 https://ho-yu.github.io 에 자동 반영
```

기억할 것은 딱 두 가지다.

- **모든 글은 `_posts/` 폴더에 넣는다.** 다른 폴더는 만들지 않는다.
- **분류는 폴더가 아니라 글 맨 위의 `categories`로 한다.** 카테고리 페이지, 태그 페이지, 아카이브는 전부 자동으로 만들어진다.

---

## 2. 글 하나 올리는 전체 과정

터미널에서 이 폴더로 이동한 뒤, 예를 들어 Notes 글을 하나 쓴다면:

```bash
cp templates/note-template.md _posts/2026-08-13-logistic-regression.md
```

그다음 만들어진 파일을 편집기로 열어서

1. 맨 위 `---` 사이의 설정을 채우고
2. `<!-- -->` 로 감싸인 안내 주석은 지우고
3. 필요 없는 절(`## 4. 코드 / 실습` 같은)은 통째로 지우고
4. 본문을 쓴다

마지막으로 확인하고 올린다. 명령어는 [11번](#11-확인하고-올리기)에 있다.

---

## 3. 파일 이름 규칙

```text
_posts/YYYY-MM-DD-영문-제목.md
```

날짜로 시작하고, 그 뒤에 영문 소문자와 하이픈(`-`)으로 제목을 쓴다.

| 좋은 예 | 설명 |
| --- | --- |
| `2026-08-13-logistic-regression.md` | 표준 형태 |
| `2026-08-13-python-list-vs-tuple.md` | 하이픈으로 단어 구분 |
| `2026-08-13-fastapi-cors-error.md` | Troubleshooting 글도 형식은 같다 |

| 피해야 할 예 | 이유 |
| --- | --- |
| `로지스틱회귀.md` | 날짜가 없어서 글로 인식되지 않는다 |
| `2026-08-13-로지스틱 회귀.md` | 한글·띄어쓰기가 주소를 깨뜨린다 |
| `2026-8-13-note.md` | 월/일은 반드시 두 자리(`08`, `13`) |

> 파일 이름이 곧 글 주소가 된다.
> `2026-08-13-logistic-regression.md` → `https://ho-yu.github.io/posts/logistic-regression/`
>
> **제목(`title`)은 한글로 써도 전혀 문제없다.** 한글을 피해야 하는 건 파일 이름뿐이다.

---

## 4. Front Matter (글 맨 위 설정)

모든 글은 `---` 두 줄 사이에 들어가는 설정으로 시작한다. 이걸 Front Matter라고 부른다.
**파일의 맨 첫 줄부터 시작해야 한다.** 위에 빈 줄이 있으면 인식되지 않는다.

```yaml
---
title: "로지스틱 회귀 이해하기"
date: 2026-08-13 21:30:00 +0900
categories: [Notes, Machine Learning]
tags: [logistic-regression, classification, scikit-learn]
---
```

### 네 줄이 각각 하는 일

| 항목 | 설명 |
| --- | --- |
| `title` | 글 제목. 화면에 보이는 제목이다. 한글 OK. **콜론(`:`)이 들어가면 반드시 큰따옴표로 감싼다.** |
| `date` | 작성 시각. `+0900`은 한국 시간이라는 뜻이니 그대로 둔다. |
| `categories` | 대괄호 안에 **[큰 분류, 세부 주제]** 두 개. |
| `tags` | 세부 기술·개념. 개수 제한 없다. |

### categories 규칙

첫 번째 값은 **반드시 아래 네 개 중 하나**다. 새로 만들지 않는다.

```text
Notes            학습하고 이해한 내용
Projects         직접 만든 결과물
Troubleshooting  겪고 해결한 문제
Retrospectives   돌아본 회고
```

두 번째 값은 자유롭게 정하면 된다. `Machine Learning`, `Python`, `Deep Learning`, `LLM`, `AI Service` 등.

```yaml
categories: [Notes, Machine Learning]
categories: [Notes, Python]
categories: [Projects, AI Service]
categories: [Troubleshooting, Python]
categories: [Retrospectives, Learning]
```

> **대소문자와 띄어쓰기를 매번 똑같이 쓴다.**
> `Machine Learning`과 `machine learning`을 섞어 쓰면 카테고리 페이지에 서로 다른 두 개로 나뉜다.
> 한 번 정한 이름을 그대로 복사해서 쓰는 게 안전하다.

### tags 규칙

**영문 소문자 + 하이픈**으로 통일한다. 세부 기술, 라이브러리, 개념 이름을 쓴다.

```yaml
tags: [logistic-regression, scikit-learn, numpy]
```

카테고리와 태그의 역할 차이는 이렇게 기억하면 된다.

```text
Category = 큰 서랍   (Notes / Machine Learning)
Tag      = 내용물 라벨 (logistic-regression, sklearn)
```

세부 개념이 많아져도 카테고리를 3단계로 늘리지 말고 **태그를 늘린다.**

### 필요할 때만 추가하는 설정

| 항목 | 언제 쓰나 |
| --- | --- |
| `math: true` | 글에 수식($$...$$)이 들어갈 때. **이걸 안 쓰면 수식이 그냥 글자로 보인다.** |
| `mermaid: true` | 글에 다이어그램을 그릴 때 |
| `pin: true` | 그 글을 홈 맨 위에 고정하고 싶을 때 |
| `image:` | 글 목록에 썸네일을 띄우고 싶을 때 |

```yaml
---
title: "로지스틱 회귀 이해하기"
date: 2026-08-13 21:30:00 +0900
categories: [Notes, Machine Learning]
tags: [logistic-regression, scikit-learn]
math: true
image:
  path: /assets/img/posts/logistic-regression/sigmoid.png
  alt: 시그모이드 함수 그래프
---
```

### 자주 하는 실수

| 잘못된 예 | 문제 |
| --- | --- |
| `title:로지스틱 회귀` | 콜론 뒤에 **공백**이 있어야 한다 |
| `title: 회귀: 기초` | 콜론이 있으면 `"회귀: 기초"` 처럼 따옴표 필요 |
| `categories: Notes, Python` | **대괄호**가 빠졌다 → `[Notes, Python]` |
| `date: 2026-08-13` | 시각과 `+0900`까지 써야 안전하다 |
| `tags: [머신러닝]` | 태그는 영문 소문자 권장 |

---

## 5. Notes 작성법

> **쓰는 시점:** 개념을 공부하고 "이제 이해했다" 싶을 때.
> 강의를 그대로 옮겨 적는 게 아니라, **내 말로 다시 설명해보는** 글이다.

**템플릿:** `templates/note-template.md`
**카테고리:** `[Notes, 주제]` — 예: `[Notes, Machine Learning]`, `[Notes, Python]`

### 구성

글 성격에 따라 두 가지 흐름 중 하나를 고르면 된다.

**이론 위주일 때**

```text
개요 → 핵심 개념 → 직관적 이해 → 수식/예제 → 핵심 정리 → 배운 점
```

**코드 위주일 때**

```text
개요 → 핵심 개념 → 입력/출력 구조 → 코드 → 실행 결과 → 실험 → 핵심 정리 → 배운 점
```

### 완성 예시

````markdown
---
title: "로지스틱 회귀 이해하기"
date: 2026-08-13 21:30:00 +0900
categories: [Notes, Machine Learning]
tags: [logistic-regression, classification, scikit-learn]
math: true
---

## 1. 개요

분류 문제를 처음 접하면서 왜 선형 회귀를 그대로 쓸 수 없는지 궁금했다.
그 답이 로지스틱 회귀여서 정리한다.

## 2. 핵심 개념

### 시그모이드 함수

어떤 실수를 0과 1 사이 값으로 눌러주는 함수다.

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

## 3. 이해하기

선형 회귀는 출력이 1을 넘거나 음수가 될 수 있어서 확률로 해석할 수 없다.
시그모이드를 씌우면 항상 0~1 사이로 들어오니 확률처럼 읽을 수 있다.

## 4. 코드 / 실습

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

## 5. 핵심 정리

- 로지스틱 회귀는 이름은 회귀지만 분류 모델이다
- 시그모이드가 출력을 확률 범위로 만든다

## 6. 배운 점

"회귀"라는 이름 때문에 값을 예측하는 모델이라고 오해하고 있었다.
실제로는 확률을 계산해 분류하는 모델이었다.

## 7. 참고

- scikit-learn 공식 문서
````

### 팁

- **6번 "배운 점"이 이 블로그에서 가장 중요한 부분이다.** 공부 전과 후에 이해가 어떻게 달라졌는지, 뭘 잘못 알고 있었는지 한두 문장이라도 꼭 남긴다.
- 코드가 필요 없는 개념 글에 억지로 코드를 넣지 않는다. 해당 절을 지우면 된다.
- 짧아도 괜찮다. 세 줄짜리 개념 정리도 충분히 글이 된다.

---

## 6. Projects 작성법

> **쓰는 시점:** 실제로 만든 결과물이 있을 때.
> 아직 안 만든 계획은 Projects가 아니다.

**템플릿:** `templates/project-template.md`
**카테고리:** `[Projects, 분야]` — 예: `[Projects, AI Service]`

### 구성

```text
프로젝트 개요 → 문제 정의 → 목표 → 주요 기능 → 기술 스택
→ 설계 및 구현 → 주요 의사결정 → 문제와 해결 → 결과 → 배운 점 → 관련 링크
```

### 팁

면접에서 실제로 물어보는 건 기능 목록이 아니라 **"왜 그렇게 만들었는가"** 다.
그래서 이 두 절에 힘을 준다.

- **주요 의사결정** — 무엇과 무엇을 두고 고민했고, 왜 그걸 골랐는지. (예: "SQLite와 PostgreSQL 중 고민했고, 배포 환경이 단일 서버라 SQLite를 골랐다")
- **문제와 해결** — 만들면서 막혔던 지점과 해결 방법

그리고 **관련 링크에 GitHub 저장소 주소를 꼭 넣는다.** 코드를 볼 수 있는 것과 없는 것은 차이가 크다.

```yaml
categories: [Projects, AI Service]
tags: [fastapi, openai-api, docker]
```

---

## 7. Troubleshooting 작성법

> **쓰는 시점:** 에러나 문제를 직접 겪고 해결했을 때. 바로 그날 쓰는 게 가장 좋다.
> 아직 해결 못 했다면 그 사실을 그대로 적어두고 나중에 이어서 쓰면 된다.

**템플릿:** `templates/troubleshooting-template.md`
**카테고리:** `[Troubleshooting, 분야]` — 예: `[Troubleshooting, Python]`

### 구성

```text
문제 → 상황 → 원인 분석 → 시도한 방법 → 해결 → 왜 해결되었는가 → 배운 점
```

### 팁

- **에러 메시지를 그대로 복사해서 코드 블록에 붙여넣는다.** 나중에 검색으로 이 글을 다시 찾게 된다.
- 실패한 시도도 지우지 말고 적는다. "이건 안 통했다"도 정보다.
- **"왜 해결되었는가"를 비우지 않는다.** 이 절이 없으면 그냥 검색 결과를 붙여넣은 글과 구분되지 않는다. 이 절이 있으면 원인을 이해했다는 증거가 된다.

````markdown
## 1. 문제

FastAPI 서버에 브라우저에서 요청하면 CORS 에러가 났다.

```text
Access to fetch at 'http://localhost:8000/api' from origin
'http://localhost:3000' has been blocked by CORS policy
```

## 3. 원인 분석

서버가 응답에 Access-Control-Allow-Origin 헤더를 넣지 않아서
브라우저가 응답을 막고 있었다.
````

---

## 8. Retrospectives 작성법

> **쓰는 시점:** 한 주, 한 달, 또는 프로젝트 하나가 끝났을 때.

**템플릿:** `templates/retrospective-template.md`
**카테고리:** `[Retrospectives, 범위]` — 예: `[Retrospectives, Learning]`

### 구성

```text
기간/범위 → 무엇을 했는가 → 새롭게 배운 것 → 잘한 점
→ 어려웠던 부분 → 개선할 점 → 다음 목표
```

### 팁

- 잘한 점만 쓰지 않는다. **어려웠던 부분과 개선할 점이 성장의 근거**가 된다.
- 다음 목표는 구체적으로 쓴다. ("공부 열심히 하기" ❌ → "다음 2주 안에 CNN 정리 글 3개 쓰기" ⭕)
- 이전 회고의 "다음 목표"를 얼마나 지켰는지 확인하면서 쓰면 흐름이 이어진다.

---

## 9. 본문 문법 치트시트

### 제목

```markdown
## 큰 제목
### 작은 제목
```

**`#` 하나짜리 제목은 쓰지 않는다.** 글 제목은 `title`이 자동으로 만들어준다.
`##`과 `###`은 오른쪽 목차(TOC)에 자동으로 들어간다.

### 강조 · 목록

```markdown
**굵게**, *기울임*, `코드`

- 항목
- 항목
  - 하위 항목

1. 첫째
2. 둘째
```

### 코드 블록

백틱 세 개로 감싸고, **언어 이름을 꼭 붙인다.** 그래야 색이 입혀진다.

````markdown
```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```
````

자주 쓰는 언어 이름: `python` `bash` `javascript` `sql` `yaml` `json` `text`

### 표

```markdown
| 항목 | 설명 |
| --- | --- |
| 내용 | 내용 |
```

### 인용 · 강조 박스 (Chirpy 전용)

인용문 바로 아래에 `{: .prompt-종류 }`를 붙이면 색깔 박스가 된다.

```markdown
> 알아두면 좋은 팁입니다.
{: .prompt-tip }

> 참고 정보입니다.
{: .prompt-info }

> 주의해야 합니다.
{: .prompt-warning }

> 위험합니다.
{: .prompt-danger }
```

파일 경로를 표시할 때는 이렇게 쓰면 경로처럼 보인다.

```markdown
`_posts/2026-08-13-note.md`{: .filepath }
```

### 링크

```markdown
[화면에 보일 글자](https://example.com)

[내 다른 글](/posts/logistic-regression/)
```

블로그 안의 다른 글을 링크할 때는 `/posts/파일이름에서-날짜를-뺀-부분/` 형식이다.

### 수식

**Front Matter에 `math: true`를 먼저 넣어야 한다.** 안 넣으면 그냥 글자로 나온다.

```markdown
문장 안에 넣을 때는 $ \sigma(z) $ 처럼 쓴다.

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
```

---

## 10. 이미지 넣기

### 1단계 — 이미지 파일 넣기

글마다 폴더를 하나 만들어 두면 나중에 관리가 편하다.

```bash
mkdir -p assets/img/posts/logistic-regression
```

만든 폴더에 이미지 파일을 복사해 넣는다.

### 2단계 — 본문에서 부르기

```markdown
![시그모이드 함수 그래프](/assets/img/posts/logistic-regression/sigmoid.png)
```

- **경로는 반드시 `/assets`로 시작한다.** (`assets/...`처럼 슬래시를 빼면 안 보인다)
- 대괄호 안 설명글은 이미지가 안 뜰 때 대신 보이는 문구다. 비워두지 않는다.

### 크기와 정렬 조절 (선택)

```markdown
![그래프](/assets/img/posts/logistic-regression/sigmoid.png){: width="500" }

![아이콘](/assets/img/posts/note/icon.png){: .normal }
```

`.normal`은 그림자 효과를 없앤다. 도표나 스크린샷에 어울린다.

---

## 11. 확인하고 올리기

### 1단계 — 로컬에서 미리 보기 (권장)

```bash
export PATH="$(brew --prefix ruby@3.4)/bin:$PATH" && bundle exec jekyll serve
```

터미널에 `Server address: http://127.0.0.1:4000/` 이 뜨면 브라우저로 그 주소를 연다.
글을 고치고 저장하면 자동으로 다시 만들어지니, 새로고침만 하면 된다.
확인이 끝나면 터미널에서 `Ctrl + C`로 종료한다.

### 2단계 — 올리기

```bash
git add .
```

```bash
git commit -m "post: 로지스틱 회귀 이해하기"
```

```bash
git push origin main
```

### 3단계 — 배포 확인

push하고 1~2분 뒤 https://ho-yu.github.io 를 새로고침하면 반영되어 있다.

배포가 잘 됐는지 확인하려면:

```bash
gh run list --limit 3
```

`success`면 정상, `failure`면 아래 [12번](#12-글이-안-보일-때)을 본다.

> 커밋 메시지는 `post: 글 제목` 형식으로 통일하면 나중에 이력을 보기 좋다.
> **글 하나를 완성할 때마다 커밋한다.** 여러 글을 한 번에 몰아서 올리지 않는 게 관리하기 편하다.

---

## 12. 글이 안 보일 때

| 증상 | 원인과 해결 |
| --- | --- |
| 글이 아예 안 나온다 | **날짜가 미래로 되어 있다.** 오늘 이후 날짜의 글은 게시되지 않는다. `date`를 현재 시각으로 고친다. |
| 글이 아예 안 나온다 (2) | 파일이 `_posts/` 안에 없거나, 파일 이름이 `YYYY-MM-DD-` 로 시작하지 않는다. |
| 제목이 비어 있다 | Front Matter가 파일 **첫 줄**부터 시작하지 않았거나 `---`가 빠졌다. |
| 배포가 `failure` | 대부분 Front Matter의 YAML 오타다. 콜론 뒤 공백, 대괄호, 따옴표를 확인한다. |
| 수식이 글자로 보인다 | Front Matter에 `math: true`가 빠졌다. |
| 이미지가 안 보인다 | 경로가 `/assets`로 시작하는지, 파일 이름의 대소문자가 정확한지 확인한다. |
| 카테고리가 두 개로 갈라졌다 | `Machine Learning`과 `machine learning`처럼 표기가 섞였다. 하나로 통일한다. |

배포 실패 원인을 자세히 보려면:

```bash
gh run view --log-failed
```

---

## 13. 최종 체크리스트

올리기 전에 이것만 확인하면 된다.

- [ ] 파일이 `_posts/` 안에 있고, 이름이 `YYYY-MM-DD-영문-제목.md` 형식인가
- [ ] Front Matter가 파일 첫 줄부터 시작하고 `---`로 열고 닫혔는가
- [ ] `categories`의 첫 번째 값이 Notes / Projects / Troubleshooting / Retrospectives 중 하나인가
- [ ] `tags`가 영문 소문자·하이픈인가
- [ ] `date`가 오늘 또는 과거인가
- [ ] 수식을 썼다면 `math: true`를 넣었는가
- [ ] 템플릿의 안내 주석(`<!-- -->`)을 지웠는가
- [ ] 안 쓴 절을 통째로 지웠는가 (빈 제목만 남기지 않기)
- [ ] "배운 점"을 한 줄이라도 채웠는가
- [ ] 로컬에서 눈으로 확인했는가

---

## 참고

- 저장소 전반 규칙: [`README.md`](../README.md)
- 저장소 운영 원칙: [`CLAUDE.md`](../CLAUDE.md)
- 글 템플릿: [`templates/`](../templates)
