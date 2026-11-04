---
title: "Python Day 5 기초 2 — 정수 변환 실패를 None으로 처리하기"
date: 2026-11-04 12:31:00 +0900
categories: [Notes, Python Practice]
tags: [python, try-except, value-error]
---

> 🗂️ **Notes · Python Practice** — `python` `try-except` `value-error`
{: .prompt-info }

---

## 1. 📝 문제

문자열을 정수로 바꾸고, 실패하면 None을 반환하는 문제

## 2. 💻 풀이

```python
def safe_int(s):
    try:
        return int(s)
    except ValueError:
        return None
```
{: file="safe.py" }

## 3. 🔍 풀이 설명

- `try`에서 `int(s)`로 변환한 값을 반환한다.
- 변환에 실패해 `ValueError`가 나면 `except`에서 `None`을 반환한다.

## 4. ✅ 테스트

```python
from safe import safe_int
assert safe_int("42") == 42 and safe_int("abc") is None and safe_int("  7 ") == 7 and safe_int("3.5") is None
print("기초 2 통과")
```
{: file="q2.py" }
