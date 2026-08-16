# ho-yu Devlog

Developer Learning Log

개인적으로 학습한 내용을 단순히 기록하는 것을 넘어
이해한 개념, 코드 실습, 문제 해결, 프로젝트 경험과 회고를 정리합니다.

## Blog

<https://ho-yu.github.io>

## Content

### Notes

개념 및 학습 기록 — <https://ho-yu.github.io/notes/>

### Projects

프로젝트 설계 및 구현 기록 — <https://ho-yu.github.io/projects/>

### Troubleshooting

문제 분석과 해결 과정 — <https://ho-yu.github.io/troubleshooting/>

### Retrospectives

학습 및 프로젝트 회고 — <https://ho-yu.github.io/retrospectives/>

## Content Structure

```text
Learn
→ Understand
→ Practice
→ Solve
→ Build
→ Reflect
```

## Writing Guide

글을 처음 쓴다면 **[docs/WRITING-GUIDE.md](docs/WRITING-GUIDE.md)** 를 먼저 본다.
파일 이름 규칙부터 Front Matter, 4개 영역별 작성법, 이미지, 배포, 문제 해결까지 순서대로 정리되어 있다.

아래는 요약이다.

## Writing Convention

모든 공개 게시물의 단일 원본은 `_posts/` 하나다.
별도의 `notes/`, `projects/` 같은 콘텐츠 디렉터리를 만들지 않는다.

파일명:

```text
_posts/YYYY-MM-DD-descriptive-title.md
```

Front Matter:

```yaml
---
title: "글 제목"
date: 2026-08-12 21:00:00 +0900
categories: [Notes, Machine Learning]
tags: [classification, logistic-regression, scikit-learn]
---
```

Category (2단계 고정):

```text
[Notes | Projects | Troubleshooting | Retrospectives, 세부 주제]
```

- 1차 Category는 위 네 가지 중 하나로 고정한다.
- 2차 Category는 학습 주제 / 프로젝트 분야에 따라 자유롭게 확장한다.
- Category는 큰 문맥, Tag는 세부 기술 / 개념이다. 세부 개념은 Category를 더 깊게 만들지 말고 Tag로 표현한다.

Tag:

- 영문 lowercase, kebab-case를 사용한다. 예: `machine-learning`, `logistic-regression`, `scikit-learn`, `numpy`

선택 Front Matter:

| 키              | 용도                                     |
| --------------- | ---------------------------------------- |
| `math: true`    | 해당 글에서 MathJax 수식 활성화          |
| `mermaid: true` | 해당 글에서 Mermaid 다이어그램 활성화    |
| `pin: true`     | 홈 상단 고정                             |
| `image:`        | 대표 이미지 (`path`, `alt`)              |

문서 형식은 `templates/`의 템플릿을 복사해서 사용한다. 모든 항목을 억지로 채울 필요는 없다.

직접 초고를 작성할 때는 `workspace/draft-01.md`부터 `draft-05.md`까지 제공되는
5개 작업 슬롯 중 하나에서 작업한다. 이 폴더는 Git으로 동기화되지만 사이트 빌드에서는
제외된다. 작성이 끝나면 `작성완료 workspace/draft-번호.md`라고 요청한다.
발행일은 요청한 당일로 확정하고, 발행한 슬롯은 공통 템플릿으로 다시 초기화한다.

## Images

```text
assets/img/posts/                          # 공통
assets/img/posts/<post-slug>/              # 글이 이미지를 여러 개 쓸 때
```

본문에서는 절대 경로로 참조한다.

```markdown
![설명](/assets/img/posts/<post-slug>/example.png)
```

## Repository Structure

```text
ho-yu.github.io/
├── .github/workflows/pages-deploy.yml   # GitHub Actions 배포 워크플로
├── docs/WRITING-GUIDE.md                # 글 작성 가이드 (사이트 빌드에서 제외)
├── _data/
│   ├── contact.yml                      # 사이드바 연락처 / 링크
│   ├── share.yml                        # 게시물 공유 버튼
│   └── locales/ko-KR.yml                # 커스텀 탭 이름만 추가 (테마 locale에 병합)
├── _includes/
│   └── section-post-list.html           # 카테고리별 목록 (테마 override 아님)
├── _plugins/
│   └── posts-lastmod-hook.rb            # git 이력 기반 최종 수정일
├── _posts/                              # 모든 게시물의 단일 원본
├── _tabs/                               # 사이드바 메뉴
│   ├── notes.md
│   ├── projects.md
│   ├── troubleshooting.md
│   ├── retrospectives.md
│   ├── categories.md
│   ├── tags.md
│   ├── archives.md
│   └── about.md
├── assets/img/posts/                    # 게시물 이미지
├── templates/                           # 글쓰기 템플릿 (사이트 빌드에서 제외)
│   ├── note-template.md
│   ├── project-template.md
│   ├── troubleshooting-template.md
│   └── retrospective-template.md
├── workspace/                           # 여러 PC에서 동기화하는 초고 (사이트 빌드에서 제외)
│   ├── common-template.md               # 형식에 얽매이지 않는 공통 초고 템플릿
│   └── draft-01.md ... draft-05.md       # 동시에 사용할 수 있는 기본 작업 슬롯 5개
├── _config.yml
├── Gemfile
├── index.html
├── CLAUDE.md
└── README.md
```

## Local Development

Ruby 3.x가 필요하다 (GitHub Actions는 Ruby 3.4 사용).
이 저장소는 macOS에서 Homebrew의 keg-only Ruby 3.4로 검증했다.

```bash
export PATH="$(brew --prefix ruby@3.4)/bin:$PATH"
```

의존성 설치:

```bash
bundle install
```

로컬 서버 실행 (<http://127.0.0.1:4000>):

```bash
bundle exec jekyll serve
```

프로덕션 빌드 + 링크 검사 (GitHub Actions와 동일):

```bash
LANG=en_US.UTF-8 bash tools/test.sh
```

`LANG`이 비어 있으면 html-proofer가 한글이 포함된 HTML을 US-ASCII로 읽다가
모든 파일을 건너뛰고 "0 internal links"로 통과해버린다. 반드시 UTF-8 locale에서 실행한다.
(GitHub Actions 러너는 UTF-8이라 이 설정이 필요 없다.)

## Deployment

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/pages-deploy.yml`)가
Jekyll 빌드 → html-proofer 검사 → GitHub Pages 배포를 수행한다.

```text
git push origin main
→ GitHub Actions (Build and Deploy)
→ GitHub Pages
→ https://ho-yu.github.io
```

## Tech Stack

GitHub Pages · Jekyll · [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) (Chirpy Starter 기반) · GitHub Actions · Markdown

## Author

GitHub: <https://github.com/ho-yu>

## License

저장소 구조 및 설정은 [Chirpy Starter](https://github.com/cotes2020/chirpy-starter)(MIT)를 기반으로 하며, 해당 라이선스는 `LICENSE`에 포함되어 있다.
게시물 본문의 저작권은 작성자에게 있다.
