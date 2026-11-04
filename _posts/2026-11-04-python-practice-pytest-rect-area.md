---
title: "Python Day 5 기초 3 — pytest로 넓이 함수 테스트하기"
date: 2026-11-04 12:32:00 +0900
categories: [Notes, Python Practice]
tags: [python, pytest, assert]
---

> 🗂️ **Notes · Python Practice** — `python` `pytest` `assert`
{: .prompt-info }

---

## 1. 📝 문제

pytest 테스트 함수로 rect_area 결과를 검증하는 문제

## 2. 💻 풀이

```python
import pytest
from shapes import rect_area


def test_rect_area():
    assert rect_area(3, 4) == 12
```
{: file="test_shapes.py" }

## 3. 🔍 풀이 설명

- `shapes` 모듈에서 `rect_area`를 가져온다.
- `test_rect_area`에서 `rect_area(3, 4)`의 결과가 12인지 `assert`로 확인한다.
