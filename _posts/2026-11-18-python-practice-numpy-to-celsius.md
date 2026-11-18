---
title: "Python Day 7 기초 1 — NumPy로 화씨를 섭씨로 바꾸기"
date: 2026-11-18 12:20:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, dtype]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `dtype`
{: .prompt-info }

---

## 1. 📝 문제

화씨 값(리스트·배열)을 NumPy로 한 번에 섭씨 배열로 바꾸는 문제

## 2. 💻 풀이

```python
def to_celsius(f):
    f = np.asarray(f, dtype=float)
    return np.array((f - 32) * 5 / 9)
```

## 3. 🔍 풀이 설명

- `np.asarray(f, dtype=float)`로 리스트든 배열이든 실수 배열로 바꾼다.
- `(f - 32) * 5 / 9`를 배열 전체에 한 번에 계산하고 `np.array`로 감싸 반환한다. 2차원 입력도 모양 그대로 계산된다.

## 4. ✅ 테스트

```python
import numpy as np

c = to_celsius([32, 212, 98.6])
assert isinstance(c, np.ndarray) and c.shape == (3,)
assert np.allclose(c, [0, 100, 37])
assert np.allclose(to_celsius(np.array([[50, 14]])), [[10, -10]])
print("기초 1 통과")
```
