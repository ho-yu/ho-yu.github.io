---
title: "Python Day 8 응용 3 — 선형 모델 예측값 계산하기"
date: 2026-11-18 12:31:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, linear-model]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `linear-model`
{: .prompt-info }

---

## 1. 📝 문제

입력 X와 가중치 w, 편향 b로 X·w+b 예측값을 구하는 문제

## 2. 💻 풀이

```python
def linear_predict(X, w, b):
    return np.dot(X, w) + b
```

## 3. 🔍 풀이 설명

- `np.dot(X, w)`로 각 행(샘플)과 가중치를 내적하고 `b`를 더해, 샘플마다 예측값 하나를 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
X = np.array([[1, 2], [3, 4]])
assert np.allclose(linear_predict(X, [10, 1], 5), [17, 39])
assert np.allclose(linear_predict(X, [0, 0], 7), [7, 7])
assert linear_predict(np.ones((5, 3)), [1, 2, 3], 0).shape == (5,)
print("응용 3 통과")
```
