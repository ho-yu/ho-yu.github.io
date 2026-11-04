---
title: "Python Day 5 기초 1 — 모듈로 넓이 함수 분리하기"
date: 2026-11-04 12:30:00 +0900
categories: [Notes, Python Practice]
tags: [python, module, import]
---

> 🗂️ **Notes · Python Practice** — `python` `module` `import`
{: .prompt-info }

---

## 1. 📝 문제

shapes 모듈에 사각형 넓이 함수를 만들어 import로 쓰는 문제

## 2. 💻 풀이

```python
def rect_area(a, b):
    return a * b
```
{: file="shapes.py" }

## 3. 🔍 풀이 설명

- `shapes.py`: `rect_area`는 두 변의 길이를 곱해 반환한다.
- `q1.py`: `from shapes import rect_area`로 다른 파일의 함수를 가져와 테스트한다.

## 4. ✅ 테스트

```python
from shapes import rect_area
assert rect_area(3, 4) == 12 and rect_area(0, 5) == 0 and rect_area(2.5, 2) == 5.0
print("기초 1 통과")
```
{: file="q1.py" }
