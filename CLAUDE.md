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

사용자가 작성한 내용의 **의미를 바꾸지 않는다.** 정리하는 것은 형식뿐이다.

허용: Markdown 문법 정리, 제목 구조 정리, 문단 분리, 목록 정리, 코드 블록 처리,
강조 표현, 가독성 개선, 중복 문장 최소 정리, Template 구조 적용, 명백한 오탈자 수정.

금지:

- 사용자가 작성하지 않은 학습 내용을 추가하는 것
- 사용자의 결론을 다른 의미로 바꾸는 것
- 이해 수준을 과장하는 것
- 존재하지 않는 실습 / 프로젝트 경험을 넣는 것
- AI가 새로 쓴 문장을 사용자의 경험처럼 표현하는 것
- 불필요하게 장문으로 늘리는 것

내용이 없는 Template 절은 억지로 채우지 말고 **통째로 삭제**하고 번호를 다시 매긴다.
어느 절에 넣을지 모호하면 임의로 해석하지 말고 원문 순서를 유지한다.

### 2. 이 저장소 구조에 맞춘 적용

일반적인 TIL 저장소 관례와 이 저장소의 규칙이 다른 부분은 **이 저장소 규칙을 따른다.**

| 일반 관례 | 이 저장소에서의 적용 | 이유 |
| --- | --- | --- |
| `notes/<Category>/파일.md` | **`_posts/` 하나** | Jekyll이 `_posts/`만 게시물로 인식 |
| `vector-norm.md` | **`YYYY-MM-DD-vector-norm.md`** | 날짜 접두사가 없으면 게시되지 않음 |
| `category: Machine Learning` | **`categories: [Notes, Machine Learning]`** | Chirpy는 2단계 배열 |
| `Machine Learning / Evaluation` | 2차는 `Machine Learning`, `evaluation`은 Tag | Category는 2단계까지 |
| `date: 2026-08-12` | **`2026-08-12 21:00:00 +0900`** | 시각·타임존 필요 |
| 별도 `## Related` 절 | Template의 **`## 참고`** 절에 통합 | 절 구조를 템플릿과 일치시킴 |
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
- 기존 글을 단순 수정할 때 원래 `date`를 바꾸지 않는다.
- `math: true`는 `$$` 수식이 있을 때만, `mermaid: true`는 다이어그램이 있을 때만 넣는다.
- `pin`, `image`는 사용자가 요청할 때만 넣는다.

### 9. Markdown 자동 정리

사용자가 Markdown 문법을 몰라도 되도록 아래를 자동 처리한다.

Heading 레벨, 목록 / 번호 목록, 굵은 글씨, 인라인 코드, 코드 블록과 언어별 Syntax Highlight,
인용문, 링크, 이미지, 표, 수식, 문단 간격.

- 문서 최상단에 `#` 제목을 넣지 않는다 (`title`이 제목을 만든다). 절은 `##`, 하위는 `###`.
- 코드 블록에는 **반드시 언어 태그**를 붙인다. 에러 메시지 · 로그 · 터미널 출력은 ` ```text `.
- 코드의 의미나 동작을 요청 없이 바꾸지 않는다. 복사 과정에서 깨진 formatting만 고친다.
- 수식은 LaTeX로 정리하되, 사용자가 쓰지 않은 수식을 추가하지 않는다.
- 본문에서 파일 경로를 언급하면 `` `경로`{: .filepath } `` 를 쓴다.
- 나열식 내용은 내용 추가 없이 표로만 바꿀 수 있다.
- Template의 `<!-- -->` 안내 주석은 반드시 제거한다.

### 10. 관련 글 연결

내용과 밀접한 기존 게시물이 있으면 `## 참고` 절에 링크한다.

```markdown
## 참고

- [벡터의 Norm](/posts/vector-norm/)
```

- 링크 형식은 `/posts/<날짜를-뺀-파일명>/`.
- 관련성이 약한 글을 억지로 연결하지 않는다.
- 작성 날짜가 아니라 **개념 관계**를 기준으로 판단한다.
- Chirpy가 Tag 기반 관련 글을 자동 표시하므로, 개념적으로 명확한 선수 / 후속 관계만 수동 연결한다.

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

### 13. Commit / Push

파일 생성과 검증까지만 자동으로 한다. **사용자의 명시적 요청 없이 `git commit` / `git push`를
실행하지 않는다.** 사용자가 "커밋해줘" / "푸시까지 해줘"라고 하면 그때 수행한다.
커밋 메시지 형식은 `post: 글 제목`이다.

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
- Chirpy가 기본 제공하는 기능(Categories, Tags, Archives, 검색, TOC, Dark/Light 모드, 관련 글, 이전/다음 글)을 다시 구현하지 않는다.
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
