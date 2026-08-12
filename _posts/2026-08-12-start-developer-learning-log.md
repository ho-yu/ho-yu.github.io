---
title: "Developer Learning Log 시작"
date: 2026-08-12 21:00:00 +0900
categories: [Notes, Meta]
tags: [til, github-pages]
pin: true
math: true
---

> 이 글은 블로그 초기 구축 후 Category / Tag / Post 렌더링을 확인하기 위한 테스트 게시물입니다.
> 확인이 끝나면 `_posts/2026-08-12-start-developer-learning-log.md`{: .filepath } 파일을 삭제해도 됩니다.
{: .prompt-info }

## Developer Learning Log

이론을 이해하고,
코드로 확인하고,
문제를 해결하며,
프로젝트로 확장하는 과정을 기록합니다.

## 기록하는 영역

| 영역                                 | 기록하는 내용                             |
| ------------------------------------ | ----------------------------------------- |
| [Notes](/notes/)                     | 개념을 이해하고 코드와 예제로 확인한 기록 |
| [Projects](/projects/)               | 문제 정의부터 결과물 구현까지의 과정      |
| [Troubleshooting](/troubleshooting/) | 오류의 원인 분석과 해결 과정              |
| [Retrospectives](/retrospectives/)   | 학습과 프로젝트를 돌아본 회고             |

전체 흐름은 다음을 목표로 합니다.

```text
Learn → Understand → Practice → Solve → Build → Reflect
```

## 렌더링 확인

코드 블록:

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"


print(hello("world"))
```

수식 (`math: true`를 Front Matter에 넣은 경우에만 활성화됩니다):

$$
\hat{y} = \sigma(w^\top x + b)
$$

## 다음 단계

앞으로 학습한 내용을 `_posts/` 아래에 하나씩 추가합니다.
작성 규칙은 저장소의 `README.md`{: .filepath }와 `CLAUDE.md`{: .filepath }, 문서 형식은 `templates/`{: .filepath }를 따릅니다.
