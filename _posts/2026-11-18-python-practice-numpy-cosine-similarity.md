---
title: "Python Day 8 응용 1 — 코사인 유사도 구하기"
date: 2026-11-18 12:29:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, cosine-similarity]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `cosine-similarity`
{: .prompt-info }

---

## 1. 📝 문제

내적을 두 벡터 길이의 곱으로 나눠 코사인 유사도를 구하는 문제

## 2. 💻 풀이

```python
def cosine_similarity(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    dot_ab = a @ b
    len_a, len_b = np.sqrt(a @ a), np.sqrt(b @ b)

    return dot_ab / (len_a * len_b)
```

## 3. 🔍 풀이 설명

- `a @ b`로 두 벡터의 내적을 구한다.
- `np.sqrt(a @ a)`와 `np.sqrt(b @ b)`로 각 벡터의 길이를 구한다.
- 내적을 두 길이의 곱으로 나눠 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
import math
assert np.isclose(cosine_similarity([1, 2], [2, 4]), 1)
assert np.isclose(cosine_similarity([1, 0], [0, 1]), 0)
assert np.isclose(cosine_similarity([1, 2], [-1, -2]), -1)
assert np.isclose(cosine_similarity([1, 0], [1, 1]), 1 / math.sqrt(2))
assert np.isclose(cosine_similarity([2, 1, 0], [0, 3, 4]), 3 / (math.sqrt(5) * 5))
print("응용 1 통과")
```
