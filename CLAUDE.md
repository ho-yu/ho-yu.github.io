# CLAUDE.md

이 저장소에서 Claude Code가 작업할 때 따르는 규칙이다.

## Repository Purpose

Developer Learning Log / TIL Blog.

- 학습 기록을 장기간 축적하는 개인 기술 블로그
- 취업 / 면접 과정에서 공개하는 개발자 학습 포트폴리오

목표하는 흐름:

```text
Learn → Understand → Practice → Solve → Build → Reflect
```

## Tech Stack

GitHub Pages + Jekyll + Chirpy (Chirpy Starter 기반) + GitHub Actions + Markdown.

버전 정보는 `Gemfile`과 `.github/workflows/pages-deploy.yml`이 기준이다.

## Content Location

모든 공개 게시물의 단일 원본(Single Source of Truth):

```text
_posts/
```

- `notes/`, `projects/`, `troubleshooting/`, `retrospectives/` 같은 별도 콘텐츠 디렉터리를 만들지 않는다.
- 분류는 디렉터리가 아니라 Front Matter의 `categories`로 한다.
- 게시물 하나를 추가할 때 index 파일이나 category 파일을 함께 수정해야 하는 구조를 만들지 않는다.
  게시물 + Front Matter만 작성하면 Navigation / Category / Tag에 자동 반영된다.

## Top-Level Categories

```text
Notes
Projects
Troubleshooting
Retrospectives
```

이 네 개는 고정이다. 새로운 1차 Category를 임의로 추가하지 않는다.

## Category Rule

```yaml
categories: [콘텐츠 유형, 세부 주제]
```

예:

```yaml
categories: [Notes, Machine Learning]
categories: [Notes, Python]
categories: [Projects, AI Service]
categories: [Troubleshooting, Python]
categories: [Retrospectives, Learning]
```

- Category는 2단계까지만 사용한다 (Chirpy의 Categories 페이지가 2단계를 기준으로 렌더링한다).
- 2차 Category는 사용자가 자유롭게 확장한다. 설정 파일이나 코드에 하드코딩하지 않는다.
- 세부 개념을 표현하려고 Category를 더 깊게 만들지 않는다. 그건 Tag의 역할이다.

```text
Category = 큰 문맥
Tag      = 세부 기술 / 개념 / 라이브러리
```

## Tag Rule

Tag는 세부 기술 및 개념에 사용한다. 영문 lowercase / kebab-case를 사용한다.

```text
machine-learning
logistic-regression
scikit-learn
numpy
```

## Filename Rule

```text
_posts/YYYY-MM-DD-descriptive-title.md
```

- 파일명은 영문 소문자 kebab-case를 사용한다 (URL이 `/posts/:title/`로 생성된다).
- `date`는 `YYYY-MM-DD HH:MM:SS +0900` 형식으로 작성한다 (타임존 `Asia/Seoul`).

## Post Front Matter

필수:

```yaml
---
title: "글 제목"
date: 2026-08-12 21:00:00 +0900
categories: [Notes, Machine Learning]
tags: [logistic-regression, scikit-learn]
---
```

필요할 때만 추가:

| 키              | 용도                                  |
| --------------- | ------------------------------------- |
| `math: true`    | MathJax 수식 사용                     |
| `mermaid: true` | Mermaid 다이어그램 사용               |
| `pin: true`     | 홈 상단 고정                          |
| `image:`        | 대표 이미지 (`path`, `alt`)           |

## TIL 자동 작성 워크플로 (`작성완료`)

사용자가 학습 내용을 작성한 뒤 **`작성완료`** 라고 입력하면, 직전에 작성한 내용을 게시물로
정리하는 명령으로 인식한다. 사용자는 Markdown 문법 / Category / Tag / 파일명 / 저장 경로 /
Front Matter를 직접 결정하지 않는다. 이 저장소의 기존 구조와 규칙을 분석해 전부 자동으로 정한다.

```text
사용자 작성 내용 → 내용 분석 → 유형 판정 → Template 적용 → Markdown 정리
→ 제목 / Category / Tag / 파일명 결정 → 파일 생성 → 관련 글 연결 → Build 검증 → 보고
```

사소한 판단으로 사용자에게 되묻지 않는다. 기존 규칙을 기준으로 합리적으로 결정하고 진행한다.

### 1. 내용 보존 (최우선 원칙)

사용자가 작성한 내용의 **의미를 바꾸지 않는다.** 자유 형식, 무번호, 메모 조각 상태의
초고도 그대로 입력으로 받아들이며, 정리하는 것은 사용자가 쓴 내용의 형식과 표현뿐이다.

허용:

- Markdown 문법, Heading 구조, 문단, 목록, 번호, 코드 블록 정리
- 글의 문맥에 맞는 Template 적용, 절 재배치, 빈 절 삭제, 절 번호 다시 매기기
- 굵은 글씨, 인라인 코드, 인용문, 표, Chirpy prompt 박스를 이용한 가독성 개선
- 사용자 원문 안에 흩어진 내용을 모아 요약하거나 핵심 문장을 추출해 강조
- 사용자 원문에 이미 있는 항목을 새로운 사실 추가 없이 표나 목록으로 변환
- 중복 문장 최소 정리, 명백한 오탈자 수정

위 작업으로 만든 요약이나 강조 문장도 반드시 사용자 원문의 문장과 의미만으로 근거를
설명할 수 있어야 한다. 원문에 `같다`, `듯하다`, `추정한다`처럼 불확실성이 있으면 이를
확정된 사실로 바꾸지 않고 같은 수준의 표현을 유지한다.

금지:

- 사용자가 작성하지 않은 학습 내용을 추가하는 것
- 원문에 없는 사실, 정의, 원리, 수치, 인과관계, 장단점, 결론을 추론해 추가하는 것
- 원문에 없는 코드, 실행 결과, 수식, 예시를 만들어 넣는 것
- 사용자의 결론을 다른 의미로 바꾸는 것
- 이해 수준을 과장하는 것
- 존재하지 않는 실습 / 프로젝트 경험을 넣는 것
- AI가 새로 쓴 문장을 사용자의 경험처럼 표현하는 것
- 불필요하게 장문으로 늘리는 것

내용이 없는 Template 절은 억지로 채우지 말고 **통째로 삭제**하고 번호를 다시 매긴다.
어느 절에 넣을지 모호하면 임의로 해석하지 말고 원문 순서를 유지한다. 설명에 필요한
내용이 부족하거나 서로 모순되면 게시물 본문을 임의로 보완하지 않는다. 대신 완료 보고에
`추가로 작성하면 좋은 부분`으로 분리해 알리고, 사용자가 직접 작성한 뒤 다시 정리한다.

### 2. 이 저장소 구조에 맞춘 적용

일반적인 TIL 저장소 관례와 이 저장소의 규칙이 다른 부분은 **이 저장소 규칙을 따른다.**

| 일반 관례 | 이 저장소에서의 적용 | 이유 |
| --- | --- | --- |
| `notes/<Category>/파일.md` | **`_posts/` 하나** | Jekyll이 `_posts/`만 게시물로 인식 |
| `vector-norm.md` | **`YYYY-MM-DD-vector-norm.md`** | 날짜 접두사가 없으면 게시되지 않음 |
| `category: Machine Learning` | **`categories: [Notes, Machine Learning]`** | Chirpy는 2단계 배열 |
| `Machine Learning / Evaluation` | 2차는 `Machine Learning`, `evaluation`은 Tag | Category는 2단계까지 |
| `date: 2026-08-12` | **`2026-08-12 21:00:00 +0900`** | 시각·타임존 필요 |
| 외부 출처와 내부 관련 글을 한 절에 혼합 | **`## 참고`와 `## 관련 글` 분리** | 출처와 사이트 탐색 경로의 역할이 다름 |
| README에 목록 추가 | **하지 않는다** | Chirpy가 Category/Tag/Archive를 자동 생성 |

### 3. 유형 판정과 Template

| 내용 | 1차 Category | Template |
| --- | --- | --- |
| 개념 학습 · 정리 · 실습 | `Notes` | `templates/note-template.md` |
| 직접 만든 결과물 | `Projects` | `templates/project-template.md` |
| 실제로 겪고 해결한 오류 | `Troubleshooting` | `templates/troubleshooting-template.md` |
| 기간 · 프로젝트 회고 | `Retrospectives` | `templates/retrospective-template.md` |

사용자가 유형을 지정했으면 그것을 따르고, 없으면 위 표로 판정한다. 기본값은 `Notes`다.
내용에 맞춰 절을 생략하거나 순서를 조정한다 (이론 중심 / 코드 중심 구성은 아래 Templates 절 참고).

### 4. 제목 자동 생성

사용자가 제목을 명확히 지정했으면 그것을 우선한다. 없으면 핵심 개념을 중심으로 생성한다.

```text
좋음: 벡터의 Norm과 단위 벡터 이해하기 / Precision과 Recall의 차이
     Train / Validation / Test를 분리하는 이유
나쁨: 오늘 공부한 내용 / TIL 8월 12일 / 머신러닝 공부 / 3장 2강
```

날짜나 강의 순서가 아니라 **기술 개념**을 제목에 담는다.

### 5. Category 결정

새 Category를 무분별하게 만들지 않는다. 결정 우선순위:

```text
1. 기존 게시물이 이미 쓰고 있는 Category
2. 유사 주제 게시물의 Category
3. 위 기준으로 분류 불가능할 때만 신규
```

2차 Category는 **넓은 기술 영역**을 나타낸다. `Precision`, `Recall`, `F1 Score`를 각각
Category로 만들지 않는다. 이 경우 2차는 `Machine Learning`이고 세부는 Tag로 표현한다.

### 6. Tag 결정

본문에 **실제로 등장하는** 기술 키워드에서 2~5개를 뽑는다. 영문 lowercase / kebab-case.
같은 의미의 기존 Tag가 있으면 새로 만들지 않고 **기존 표기를 글자 그대로 재사용한다.**

```text
금지: machine-learning / machinelearning / ML / Machine Learning / machine_learning 혼용
```

본문에서 근거를 찾을 수 없는 Tag는 넣지 않는다.

### 7. 작성 전 필수 조사

파일을 만들기 전에 **반드시** 기존 표기와 중복 문서를 확인한다.

```bash
grep -h "^categories:" _posts/*.md | sort | uniq -c | sort -rn
grep -h "^tags:" _posts/*.md | sort -u
ls _posts/
```

같은 주제의 글이 이미 있으면 새로 만들기 전에 내용을 확인한다.
완전히 같은 주제면 **새 파일을 만들지 말고**, 기존 문서 보강과 별도 개념 분리 중 어느 쪽이
적절한지 판단해 사용자에게 알린다. 기존 문서를 고칠 때 새 학습 기록과 기존 내용을
임의로 섞어 의미를 바꾸지 않는다.

### 8. Front Matter 자동 생성

```yaml
---
title: "Precision과 Recall의 차이"
date: 2026-08-12 21:00:00 +0900
categories: [Notes, Machine Learning]
tags: [classification, precision, recall]
---
```

- `date`는 실제 작성 시각(`date "+%Y-%m-%d %H:%M:%S +0900"`). **미래 날짜 금지.**
- 사용자가 날짜를 지정하면 그것을 우선한다.
- `workspace/` 초고의 Front Matter에 `date: YYYY-MM-DD`가 적혀 있으면 그 값이
  "사용자가 지정한 날짜"다 — 시각은 `09:00:00 +0900`을 붙여 발행일로 확정한다.
  초고에 `date`가 비어 있으면 작성완료를 요청한 당일 실제 시각을 쓴다.
- 기존 글을 단순 수정할 때 원래 `date`를 바꾸지 않는다.
- `math: true`는 `$$` 수식이 있을 때만, `mermaid: true`는 다이어그램이 있을 때만 넣는다.
- `pin`, `image`는 사용자가 요청할 때만 넣는다.

### 9. Markdown 자동 정리

사용자가 Markdown 문법을 몰라도 되도록 아래를 자동 처리한다.

Heading 레벨, 목록 / 번호 목록, 굵은 글씨, 인라인 코드, 코드 블록과 언어별 Syntax Highlight,
인용문, 링크, 이미지, 표, 수식, 문단 간격.

초고에 Category, Tag, Heading, 번호가 전혀 없어도 내용의 문맥을 기준으로 구조화한다.
노션 스타일은 장식이 아니라 가독성을 위해 사용한다. 글의 목적이나 핵심 요약처럼 원문에서
명확히 확인되는 내용만 `.prompt-tip`, `.prompt-info`, `.prompt-warning` 등으로 강조하며,
강조 박스를 채우기 위해 새로운 설명을 만들지 않는다.

- 문서 최상단에 `#` 제목을 넣지 않는다 (`title`이 제목을 만든다). 절은 `##`, 하위는 `###`.
- 코드 블록에는 **반드시 언어 태그**를 붙인다. 에러 메시지 · 로그 · 터미널 출력은 ` ```text `.
- **사용자가 code fence(` ``` `)로 감싸지 않고 그냥 붙여 넣은 코드도 자동으로 감지해
  코드 블록으로 감싼다.** 들여쓰기된 함수 정의, `import`/API 호출 한 줄, 터미널 명령,
  변수 대입식처럼 코드로 읽히는 줄은 산문으로 두지 않고 언어를 판단해 ` ```python ` 등으로
  감싼다 — 애매하면 원문의 문맥(코드 앞뒤 설명, 사용된 문법)으로 판단하고, 그래도
  불확실하면 ` ```text `로 감싼다. 코드의 내용 자체(변수명, 값, 로직)는 바꾸지 않는다.
- 코드의 의미나 동작을 요청 없이 바꾸지 않는다. 복사 과정에서 깨진 formatting만 고친다.
- 수식은 LaTeX로 정리하되, 사용자가 쓰지 않은 수식을 추가하지 않는다.
- 본문에서 파일 경로를 언급하면 `` `경로`{: .filepath } `` 를 쓴다.
- 나열식 내용은 내용 추가 없이 표로만 바꿀 수 있다.
- **설명 산문은 놓치지 않고 노션 문법으로 가독성을 높인다.** "왜 필요한가"처럼 원문에서
  확인되는 동기·이유는 `.prompt-tip`, 핵심 정의·한 줄 요약은 `.prompt-info`, 주의·함정은
  `.prompt-warning`, 위험한 실수는 `.prompt-danger`로 감싸고, 나열된 용어 대응·비교는
  표로 정리한다. 강조 상자 안 문장은 원문 문장을 그대로 쓰거나 다듬기만 하지, 새 내용을
  만들어 채우지 않는다.
- Template의 `<!-- -->` 안내 주석은 반드시 제거한다.

### 10. 관련 글 연결

관련 글은 사용자가 플래그나 링크를 직접 작성하지 않아도 자동 처리한다.

#### 하단 자동 추천 카드

- 공통 Tag가 많은 글을 우선해 최대 3개 표시한다.
- 공통 Tag가 없으면 동일한 2차 Category의 글로 보완한다.
- `Notes` 같은 1차 Category만 같다는 이유로 연결하지 않는다.
- 관련성이 없으면 카드 영역을 표시하지 않는다.
- 새 글이 추가되면 기존 글의 카드도 빌드 시 자동 갱신된다.

#### 본문 최하단 관련 글

Tag는 2~5개로 제한되므로 Tag가 겹치지 않아도 본문의 개념 관계가 명확할 수 있다.
작성 전 필수 조사에서 기존 게시물의 제목과 본문을 확인하고, 내용상 직접 연결되는 글이 있으면
게시물 **본문 최하단**에 `## 관련 글` 절을 만들고 게시물 제목을 링크로 삽입한다.

```markdown
## 관련 글

- [벡터 기초 — 정의부터 정규화까지](/posts/vector-basics/)
```

- 링크 형식은 `/posts/<날짜를-뺀-파일명>/`.
- 링크 텍스트는 해당 게시물의 `title`을 글자 그대로 사용한다.
- Tag 일치 여부가 아니라 **본문의 개념 관계**를 기준으로 1~3개만 선택한다.
- 관련성이 약한 글, 같은 1차 Category일 뿐인 글, 단순히 작성 시기가 가까운 글은 넣지 않는다.
- 관련 글이 없으면 빈 절을 만들지 않는다.
- `## 참고`가 있더라도 `## 관련 글`은 그보다 뒤, 본문의 마지막 절에 둔다.
- `## 참고`는 외부 문서·강의·출처, `## 관련 글`은 이 블로그의 내부 게시물에 사용한다.

### 11. 검증

파일 생성 후 빌드를 확인한다. 통과 전에는 완료 보고를 하지 않는다.

```bash
export PATH="$(brew --prefix ruby@3.4)/bin:$PATH" && LANG=en_US.UTF-8 bash tools/test.sh
```

확인 항목: Front Matter 오류, Markdown 오류, broken link, 이미지 경로, build error,
잘못된 Category / Tag / URL. 오류는 안전한 범위에서 직접 고친다.

### 12. 보고

길게 설명하지 않는다. 자동으로 결정한 값을 짧게 보여준다.

```text
TIL 정리 완료

제목:      Precision과 Recall의 차이
Category:  [Notes, Machine Learning]
Tags:      classification, precision, recall
파일:      _posts/2026-08-12-precision-recall.md
관련 글:   1개 연결
Build:     정상
```

내용의 의미를 건드리지 않았음을 밝히고, 내용이 없어 삭제한 절이 있으면 반드시 알린다.
원문만으로 설명이 부족한 지점이 있으면 게시물에 내용을 만들어 넣지 않고
`추가로 작성하면 좋은 부분` 항목에 질문 또는 주제만 간단히 나열한다.

### 13. Commit / Push

파일 생성과 검증까지만 자동으로 한다. **사용자의 명시적 요청 없이 `git commit` / `git push`를
실행하지 않는다.** 사용자가 "커밋해줘" / "푸시까지 해줘"라고 하면 그때 수행한다.
커밋 메시지 형식은 `post: 글 제목`이다.

`workspace/` 안의 초고 파일은 `작성완료` 처리 이후에도 **절대 자동으로 수정·초기화하지
않는다.** 발행한 슬롯을 비우거나 공통 템플릿으로 되돌리는 등 초고 내용에 손대는 작업과
그 commit / push는 사용자가 그때그때 별도로 명시할 때만 한다.

## TIL Final Review & Enhancement Workflow

이미 존재하는 `_posts/*.md` 게시물 한 편을 기술적으로 검토·보완하는 별도 워크플로다.
초고를 새 게시물로 만드는 위 `작성완료`(공백 없음) 워크플로와는 **다른 트리거, 다른
대상**이다 — 혼동하지 않는다.

### 트리거

다음처럼 말하면 이 워크플로를 실행한다: `작성 완료`(공백 있음), `TIL 작성 완료`,
`글 작성 완료`, `정리 완료`, `최종 검토해줘`.

### 원칙: Rewrite가 아니라 Review + Enhance

```text
사용자가 작성한 내용 → 전체 흐름 이해 → 기술적 검토 → 부족한 연결고리 발견
→ 현재 학습 범위 내에서 보완 → 오개념 수정 → 필요한 시각자료 추가 → 사용자의 글로 유지
```

TIL은 사용자의 실제 학습 기록이자 향후 기술 면접 포트폴리오다. 글 전체를 AI 문체로
새로 쓰지 않는다. 다음은 절대 하지 않는다: 학습하지 않은 고급 개념 대량 추가, 범위를
크게 넘는 새 강의 작성, 불필요한 대학원 수준 이론·수식 추가, 사용하지 않은
라이브러리·기술 추가, 하지 않은 실험·실행·오류 경험을 했다고 서술, 느끼지 않은
"배운 점"을 창작, 과장된 이해 수준 표현, 전문 용어를 면접용으로 불필요하게 늘리기,
원문 전체를 AI 문체로 교체, 분량만 억지로 늘리기, 장식용 이미지 추가.
정확성 > 분량, 이해 > 전문 용어, 사용자 목소리 > AI 목소리, 맥락에 맞는 보완 > 과잉
지식, 근거 > 과장, 유용한 그림 > 장식 이미지 — 이 우선순위가 항상 이긴다.

### Current Learning Scope 판단

보완 전 게시물 전체를 읽고 다음을 파악한다: 실제로 배운 주제, 핵심 개념, 도달한 수준,
다룬 코드/수식/예제, 설명하려는 범위. 모든 보완은 **이 범위 바로 주변의 인접 개념까지만**
허용한다. 예를 들어 `nn.Linear`의 weight/bias/shape를 다룬 글이라면 입출력 feature
관계·weight shape 의미·forward 계산 흐름까지는 보완 대상이지만, attention·CNN·역전파
전체 유도·optimizer 내부 알고리즘은 대상이 아니다.

### 검토 절차

1. **대상 확인** — 저장소 전체를 다시 읽지 않는다. `git status` / `git diff`로 현재
   작업 중인 `_posts/*.md`와 직접 관련된 파일만 확인한다.
2. **전체 흐름 파악** — 부분 문장부터 고치지 않는다. 먼저 전체를 읽고
   `왜 배우는가 → 무엇인가 → 어떻게 이해하는가 → 코드로 어떻게 표현되는가 → 결과 →
   무엇을 배웠는가` 흐름을 파악한 뒤 수정한다.
3. **기술 정확성 검토** — 개념 정의, 용어, 수식, shape 설명, 입출력 관계, 코드-설명
   일치, 함수/클래스/메서드 설명, 인과관계, 예제 적합성, 오해하기 쉬운 표현을 확인한다.
   틀린 내용은 반드시 고치고, 단순 표현 차이는 사용자 표현을 우선한다.
4. **외부 검증** — 불확실하거나 버전에 영향받는 내용만 공식 자료로 확인한다(공식
   Documentation → 공식 API Reference → 공식 Tutorial → 원 논문). 블로그·Stack
   Overflow는 1차 근거로 쓰지 않는다. 매 문장을 검색하지 않는다.
5. **부족한 내용 탐지** — 정의(처음 보는 사람이 "이게 뭔지" 알 수 있는가), 필요성(왜
   필요한지 설명됐는가), 관계(앞뒤 개념과의 관계), 직관(정의·수식뿐이고 의미가
   빠지지 않았는가), 데이터 구조(shape/dimension/input/output/type이 필요한 곳에
   명확한가), 코드(왜 쓰는지·입력·결과가 설명됐는가), 결과 해석(실행 결과의 의미가
   설명됐는가)을 기준으로 검토한다.
6. **보완 우선순위** — Priority 1(반드시): 잘못된 개념, 오개념 소지, 핵심 정의 누락,
   코드-설명 불일치, 수식/shape 오류, 인과관계 전도. Priority 2(적극): 개념 간 연결,
   필요성, 직관, 실행 결과 해석, 중요한 입출력 관계, 초보자가 헷갈리는 지점.
   Priority 3(필요할 때만): 추가 예제·수식·참고·관련 개념 — 이것 때문에 글을
   억지로 늘리지 않는다.

### 문체 · 분량 · 구조

사용자의 성장 기록을 논문처럼 바꾸지 않는다.

```text
좋음: "처음에는 weight가 단순히 하나의 값이라고 생각했다. 하지만 nn.Linear(4, 2)를
확인하면서 출력 뉴런마다 입력 4개에 대응하는 weight가 필요하기 때문에 weight가
(2, 4) 구조를 가진다는 것을 이해했다."
나쁨: "가중치 행렬 W∈R^{m×n}는 아핀 변환을 구성하는 선형 연산자로서..."
```

현재 학습 수준에 필요 없는 전문 표현은 쓰지 않는다. "현재 내용을 제대로 이해하기 위해
필요한가?"가 기준이다 — YES면 추가, NO면 추가하지 않는다. 기존 분량을 크게 늘리지
않으면서 정보 밀도와 이해도를 높인다. 중복 문장은 제거할 수 있다. 순서가 이해를
방해할 때만 최소한으로 재배치한다(예: 코드→정의→왜→결과 순서를 왜→정의→직관→코드→
결과 해석 순서로) — 작성자의 원래 의도를 무시하는 전면 구조 변경은 하지 않는다.
본문은 `## H2` / `### H3`만 쓴다. `title`이 H1 역할을 하므로 `# 제목`을 중복
생성하지 않는다. TOC가 보기 좋도록 지나치게 깊은 heading은 피한다.

### "배운 점" 처리

사용자가 이미 썼다면 문맥 정리·표현 명확화·앞 내용과의 연결만 한다. 사용자가 쓰지
않았다면 AI가 경험을 임의로 만들지 않고, 대신 TODO 주석을 남길 수 있다:

```markdown
<!-- TODO: 학습 전 생각과 학습 후 달라진 점을 직접 한두 문장으로 정리 -->
```

### 코드 검토

syntax, API 사용, 변수 의미, shape, input/output, 실행 흐름을 확인한다. 단순 예제가
불필요하게 복잡하면 현재 개념 수준에 맞게 정리할 수 있다. 사용자가 직접 작성한 중요한
실습 코드는 임의로 통째로 교체하지 않는다 — 변경이 필요하면 이유가 명확해야 한다.

### 시각자료 추가 판단

**개념을 설명하는 부분에는 되도록이면 정확한 그림을 넣는다.** 흐름·구조·관계·비교로
표현되는 핵심 개념이면 우선 그림으로 옮길 수 있는지 검토한다 — 굳이 "그림 없이는
이해가 안 될 정도"까지는 아니어도, 정확하게 그릴 수 있고 이해를 도우면 넣는다.
다만 정확성은 여전히 최우선이다: 확신할 수 없는 그림, 개념과 무관한 장식용 이미지는
넣지 않는다. 표로 이미 충분히 정리되는 나열형 정보(비교표 등)까지 억지로 그림으로
바꾸지 않는다. 분량 상한은 두지 않되, 같은 내용을 표·그림으로 중복 표현하지 않는다.

특히 유용한 경우: 데이터 흐름(Input→Model→Output), Tensor/Matrix shape 변환,
신경망 구조(Input/Hidden/Output Layer), ML 파이프라인(Data→Split→Train→Evaluate),
개념 비교(Training vs Validation vs Test 등), 알고리즘 흐름(Forward→Loss→Backward→
Optimizer Step).

생성 방식 우선순위:

1. **Mermaid** — 흐름·구조·관계 표현에 우선 사용. Markdown 관리, diff 확인, Light/Dark
   대응이 쉽다. 사용 시 Front Matter에 `mermaid: true`를 추가한다.
2. **SVG** — Tensor/Matrix/신경망 구조처럼 Mermaid보다 명확한 경우 직접 제작한다.
   `assets/img/posts/<post-slug>/`에 저장한다. 단순·정확·고가독성·Light/Dark 대응·
   충분한 텍스트 크기·모바일 가독성을 지킨다.
3. **Python 그래프** — sigmoid, loss curve, activation function처럼 실제 수식/데이터
   기반 정확한 표현이 중요할 때만 matplotlib 등을 쓴다. 그럴듯한 임의의 그래프를
   만들지 않는다.

**정확도는 100%에 가깝게 맞춘다.** 시각적으로 이해가 더 빠른 정리 부분(흐름·구조·
shape 변환·비교)을 찾으면 만들기 전에 반드시 본문·코드의 관련 수치(shape, 개수,
순서, 화살표 방향)를 다시 한번 원문과 대조한 뒤 그린다. 그림은 텍스트보다 오해를
크게 만들 수 있으므로 화살표 방향, shape, dimension, 용어, 레이블, 수학 관계가
본문·코드와 정확히 일치하는지 그린 후에도 재검증한다. 확신할 수 없는 그림은
만들지 않는다. SVG로 `<img>` 삽입 시 루트 `<svg>`에 `width`/`height`를 `viewBox`와
함께 명시하고 마크다운에도 `{: w=".." h=".." }`를 붙인다 — 없으면 Chirpy의 lazy-load
스크립트가 컨테이너 크기를 못 잡아 이미지가 0px로 접힌다. `alt`는 항상 의미 있게
쓴다(`![nn.Linear에서 입력 4개와 출력 2개에 대응하는 weight 행렬 구조](...)`이지
`![image](...)`가 아니다). 그림만 던져두지
않는다 — 본문에서 "아래 그림처럼..."으로 무엇을 보여주는지 먼저 설명하고, 그림 아래에서
핵심 의미를 한두 문장으로 해석한다.

### 최종 점검

수정 후 처음부터 다시 읽으며 확인한다: 처음 보는 사람이 흐름을 따라갈 수 있는가 /
핵심 정의가 빠지지 않았는가 / 필요성이 설명됐는가 / 개념 간 연결이 자연스러운가 /
수식·shape·코드가 정확한가 / 설명과 코드가 일치하는가 / 불필요하게 어려운 내용이
추가되지 않았는가 / 학습 범위를 벗어나지 않았는가 / AI가 쓴 교과서처럼 바뀌지
않았는가 / 사용자가 직접 공부한 흔적이 유지되는가 / 면접관에게 공개해도 부끄러운
기술 오류가 없는가 / 추가한 그림이 실제 이해에 도움이 되는가.

### 로컬 검증

기존 `### 11. 검증`의 빌드 명령을 그대로 사용한다. 시각자료를 추가했다면 로컬에서
Mermaid·이미지·수식·코드 블록·Table·TOC가 깨지지 않는지 반드시 확인한다.

### Commit / Push 금지

이 워크플로는 `git commit` / `git push`를 **절대 자동으로 하지 않는다.** Claude의
역할은 Review → Enhance → Validate → Report까지다. 사용자가 최종 결과를 직접 읽고
검토한 뒤 수동으로 commit/push한다.

### 보고 형식

```markdown
## TIL 최종 검토 완료

### 기술 검토
- 수정한 기술적 오류
- 오해 가능성이 있어 명확히 한 부분

### 내용 보완
- 추가한 핵심 설명
- 추가한 개념 연결

### 시각자료
- 추가한 그림
- 그림을 추가한 이유

### 유지한 범위
- 현재 글의 학습 범위
- 의도적으로 확장하지 않은 부분

### 직접 작성이 필요한 부분
- 사용자의 실제 경험이나 배운 점 등 AI가 대신 작성하지 않은 부분

### 검증
- Build
- Markdown
- Image / Mermaid
- Category / Tag

### Git
- Commit하지 않음
- Push하지 않음
```

수정할 것이 거의 없다면 억지로 바꾸지 말고 "현재 학습 범위에서 기술적 오류와 의미
있는 누락이 없어 최소한의 표현 수정만 수행"이라고 짧게 보고한다.

## Writing Guide

사용자용 글 작성 가이드는 `docs/WRITING-GUIDE.md`에 있다 (사이트 빌드에서 제외됨).
Front Matter 규칙이나 영역별 작성법을 바꿀 때는 이 문서도 함께 갱신한다.

## Templates

문서 형식은 `templates/`의 템플릿을 기준으로 한다.

```text
templates/note-template.md
templates/project-template.md
templates/troubleshooting-template.md
templates/retrospective-template.md
```

- `templates/`는 게시물이 아니다. `_config.yml`의 `exclude`에 포함되어 사이트 빌드에서 제외된다.
- 저장소에서는 그대로 열람할 수 있어야 하므로 삭제하거나 이동하지 않는다.
- 템플릿의 모든 항목을 억지로 채우지 않는다. 글 성격에 맞춰 절을 빼거나 순서를 조정한다.
  - 이론 중심: 개요 → 핵심 개념 → 직관적 이해 → 수식 / 예제 → 핵심 정리 → 핵심 기억 카드
  - 코드 중심: 개요 → 핵심 개념 → 입력 / 출력 구조 → 코드 → 실행 결과 → 실험 → 핵심 정리 → 핵심 기억 카드

## Images

```text
assets/img/posts/                # 공통
assets/img/posts/<post-slug>/    # 글이 이미지를 여러 개 쓸 때
```

본문에서는 절대 경로(`/assets/img/posts/...`)로 참조한다.
샘플 이미지를 임의로 대량 생성하지 않는다.

## Writing Principle

- AI가 사용자의 학습 경험을 임의로 만들어내지 않는다.
- 단순 강의 복사보다 사용자가 이해한 내용을 중심으로 한다.
- 기술적 정확성을 유지한다. 확인되지 않은 내용을 단정하지 않는다.
- 불필요하게 장황하게 쓰지 않는다.
- 코드가 필요하지 않은 이론 글에 코드를 억지로 넣지 않는다.
- 프로젝트가 아닌 학습 글에 프로젝트 형식을 강제하지 않는다.
- 문제 해결 경험이 실제로 있을 때만 Troubleshooting으로 기록한다.
- 실제로 만든 결과물이 있을 때만 Projects로 기록한다.
- 모든 기존 게시물을 대량 재작성하지 않는다.
- 게시물 하나의 작업이 끝나면 그 게시물 단위로 commit하기 쉽게 유지한다.
- 사용자의 개인정보(이메일, 실명, SNS 등)를 임의로 추가하지 않는다.

## Theme Rule

- Chirpy는 gem(theme) 으로 사용한다. 테마 core를 저장소로 복사해오지 않는다.
- 테마의 `_layouts` / `_includes` / `_sass` 파일을 같은 이름으로 덮어쓰지 않는다.
  기능을 추가할 때는 `_includes/section-post-list.html`처럼 이름이 겹치지 않는 파일을 새로 만든다.
- `_tabs/`에 새 탭을 추가하면 `_data/locales/ko-KR.yml`의 `tabs:`에도 한 줄 추가한다.
  Chirpy는 탭 페이지의 `<title>`을 locale에서만 가져오고 `page.title`로 fallback하지 않아서,
  이 줄이 없으면 해당 탭의 `<title>`이 비게 된다. 이 파일은 테마 locale에 병합되므로
  필요한 키만 적고 나머지는 테마 값을 그대로 쓴다.
- Chirpy가 기본 제공하는 기능(Categories, Tags, Archives, 검색, TOC, Dark/Light 모드, 이전/다음 글)을 다시 구현하지 않는다.
- 관련 글 UI는 Chirpy 카드를 유지하고, 추천 점수만 `_includes/related-posts.html`에서 보완한다.
- 새 기능보다 유지보수성과 테마 업데이트 가능성을 우선한다.
- 불필요한 dependency, 별도 프런트엔드 프레임워크, 과도한 CSS override, 과도한 자동화를 추가하지 않는다.

원칙: 단순성 > 자동화 > 화려함

## Local Development

Ruby 3.x가 필요하다. macOS에서는 Homebrew의 keg-only Ruby를 사용하고 system Ruby를 건드리지 않는다.

```bash
export PATH="$(brew --prefix ruby@3.4)/bin:$PATH"
bundle install
bundle exec jekyll serve                        # http://127.0.0.1:4000
LANG=en_US.UTF-8 bash tools/test.sh             # 프로덕션 빌드 + html-proofer (CI와 동일)
```

`tools/test.sh`는 반드시 UTF-8 locale에서 실행한다. `LANG`이 비어 있으면 html-proofer가
한글이 포함된 HTML을 US-ASCII로 읽다가 모든 파일을 건너뛰고 "0 internal links"로
통과해버린다 (검사한 것처럼 보이지만 실제로는 아무것도 검사하지 않은 상태).

## Deployment

`main` push → GitHub Actions(`Build and Deploy`) → GitHub Pages → <https://ho-yu.github.io>

- GitHub Pages의 배포 소스는 **GitHub Actions**이다. `gh-pages` 브랜치를 만들지 않는다.
- `_site/`, `.jekyll-cache/`, `Gemfile.lock`, `vendor/`는 commit하지 않는다 (`.gitignore` 참고).
- force push를 사용하지 않는다.

## Routine Workflow

```text
학습 / 복습
→ _posts/YYYY-MM-DD-title.md 작성
→ Front Matter 설정
→ 본문 작성
→ 로컬 확인 (bundle exec jekyll serve)
→ git add / commit / push
→ GitHub Pages 자동 배포
```
