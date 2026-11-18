---
title: "Python Day 8 응용 2 — 행렬과 벡터의 곱 계산하기"
date: 2026-11-18 12:30:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, matrix, vector]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `matrix` `vector`
{: .prompt-info }

---

## 1. 📝 문제

행렬의 각 행과 벡터를 내적해 행렬·벡터 곱을 만드는 문제

## 2. 💻 풀이

```python
def mat_vec(A, x):
    a, x = np.asarray(A), np.asarray(x)
    out = []

    for i in a:
        out.append(i @ x)

    return np.asarray(out)
```

## 3. 🔍 풀이 설명

- 행렬의 행을 하나씩 꺼내 `i @ x`로 벡터와 내적한 값을 `out`에 담는다.
- `out`을 배열로 바꿔 반환하므로 결과 길이는 행렬의 행 수와 같다.

## 4. ✅ 테스트

```python
import numpy as np
A = np.array([[1, 2], [3, 4], [5, 6]])
assert np.allclose(mat_vec(A, [1, 1]), [3, 7, 11])
assert mat_vec(A, [1, 1]).shape == (3,)
assert np.allclose(mat_vec(A, [2, -1]), A @ np.array([2, -1]))
assert np.allclose(mat_vec([[80, 90], [60, 100], [90, 70]], [0.4, 0.6]), [86, 84, 78])
print("응용 2 통과")
```
