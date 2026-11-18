---
title: "Python Day 8 심화 1 — 행렬 곱 구현하기"
date: 2026-11-18 12:32:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, matrix]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `matrix`
{: .prompt-info }

---

## 1. 📝 문제

두 행렬을 곱해 (앞 행렬 행 수, 뒤 행렬 열 수) 행렬을 만드는 문제

## 2. 💻 풀이

```python
def mat_mul(A, B):
    a, b = np.asarray(A), np.asarray(B)
    return a @ b
```

## 3. 🔍 풀이 설명

- 두 입력을 배열로 바꾼 뒤 `@` 연산자로 행렬 곱을 계산해 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6, 7], [8, 9, 10]])
assert np.allclose(mat_mul(A, B), [[21, 24, 27], [47, 54, 61]])
assert mat_mul(A, B).shape == (2, 3)
rng = np.random.default_rng(0)
P, Q = rng.normal(size=(4, 3)), rng.normal(size=(3, 5))
assert np.allclose(mat_mul(P, Q), P @ Q)
assert mat_mul(np.ones((1, 4)), np.ones((4, 1))).shape == (1, 1)
print("심화 1 통과")
```
