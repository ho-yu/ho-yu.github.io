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
  - 이론 중심: 개요 → 핵심 개념 → 직관적 이해 → 수식 / 예제 → 핵심 정리 → 배운 점
  - 코드 중심: 개요 → 핵심 개념 → 입력 / 출력 구조 → 코드 → 실행 결과 → 실험 → 핵심 정리 → 배운 점

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
