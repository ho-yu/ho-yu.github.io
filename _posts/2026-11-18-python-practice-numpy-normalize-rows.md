---
title: "Python Day 7 응용 2 — 행마다 합이 1이 되게 정규화하기"
date: 2026-11-18 12:24:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, normalization, broadcasting]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `normalization` `broadcasting`
{: .prompt-info }

---

## 1. 📝 문제

각 행을 그 행의 합으로 나눠 행마다 합이 1이 되게 만드는 문제

## 2. 💻 풀이

```python
# 각 행을 그 행의 합으로 나눠서, 행마다 합이 1이 되게 바꾼 배열을 돌려주는 함수 작성.
def normalize_rows(m):
    n = np.asarray(m, dtype=float)
    sums = n.sum(axis=1, keepdims=True)
    return n / sums
```

## 3. 🔍 풀이 설명

- `sum(axis=1, keepdims=True)`로 행마다의 합을 (행 수, 1) 모양으로 구한다.
- `n / sums`에서 브로드캐스팅으로 각 행이 자기 행의 합으로 나뉜다.

## 4. ✅ 테스트

```python
import numpy as np
r = normalize_rows(np.array([[1, 1, 2], [0, 5, 5]], dtype=float))
assert r.shape == (2, 3)
assert np.allclose(r.sum(axis=1), 1) and np.allclose(r[0], [0.25, 0.25, 0.5])
assert np.allclose(normalize_rows([[2, 2], [1, 3], [5, 0]]), [[0.5, 0.5], [0.25, 0.75], [1, 0]])
print("응용 2 통과")
```
