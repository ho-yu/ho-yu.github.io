---
title: "Python Day 7 응용 1 — 표준편차 직접 계산하기"
date: 2026-11-18 12:23:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, standard-deviation]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `standard-deviation`
{: .prompt-info }

---

## 1. 📝 문제

평균·편차·분산을 차례로 구해 표준편차를 직접 계산하는 문제

## 2. 💻 풀이

```python
def std_dev(a):
    a = np.asarray(a, dtype=float)
    mean = a.sum() / len(a)
    dev = a - mean
    var = (dev ** 2).sum() / len(a)
    return var ** 0.5
```

## 3. 🔍 풀이 설명

- 실수 배열로 바꾼 뒤 `a.sum() / len(a)`로 평균을 구한다.
- 각 값에서 평균을 뺀 편차 `dev`를 제곱해 평균을 내면 분산 `var`가 된다.
- `var ** 0.5`로 분산의 제곱근을 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
assert np.isclose(std_dev([2, 4, 4, 4, 5, 5, 7, 9]), 2.0)
assert np.isclose(std_dev([5, 5, 5]), 0.0)
rng = np.random.default_rng(0)
x = rng.normal(10, 3, size=1000)
assert np.isclose(std_dev(x), x.std())
print("응용 1 통과")
```
