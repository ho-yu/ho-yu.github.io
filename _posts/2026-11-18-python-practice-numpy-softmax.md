---
title: "Python Day 7 응용 3 — 오버플로 없는 softmax 구현하기"
date: 2026-11-18 12:25:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, softmax, numerical-stability]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `softmax` `numerical-stability`
{: .prompt-info }

---

## 1. 📝 문제

최댓값을 빼서 오버플로 없이 softmax 확률을 구하는 문제

## 2. 💻 풀이

```python
def softmax(z):
    z = np.asarray(z, dtype=float)
    z = z - z.max()
    e = np.exp(z)
    p = e / e.sum()

    return p
```

## 3. 🔍 풀이 설명

- 입력에서 최댓값을 빼 가장 큰 값을 0으로 맞춰, `np.exp`의 결과가 지나치게 커지지 않게 한다.
- `np.exp` 결과를 그 합으로 나눠 합이 1인 확률 배열을 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
import math

p = softmax([1.0, 2.0, 3.0])
assert np.isclose(p.sum(), 1) and np.all(p > 0) and p.argmax() == 2
assert np.isclose(p[2], math.exp(3) / (math.exp(1) + math.exp(2) + math.exp(3)))
assert np.allclose(softmax([1000.0, 1000.0, 1000.0]), [1 / 3] * 3)          # 오버플로 없이
assert np.allclose(softmax([1.0, 2.0, 3.0]), softmax([101.0, 102.0, 103.0]))   # 같은 수를 더해도 같다
print("응용 3 통과")
```
