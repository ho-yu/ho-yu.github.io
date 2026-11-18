---
title: "Python Day 8 기초 1 — 두 벡터의 내적 구하기"
date: 2026-11-18 12:26:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, vector, dot-product]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `vector` `dot-product`
{: .prompt-info }

---

## 1. 📝 문제

같은 위치끼리 곱해 더하는 방식으로 두 벡터의 내적을 구하는 문제

## 2. 💻 풀이

```python
def dot(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return (a * b).sum()
```

## 3. 🔍 풀이 설명

- 두 입력을 배열로 바꾼 뒤 `a * b`로 같은 위치끼리 곱하고 `.sum()`으로 더한다.

## 4. ✅ 테스트

```python
import numpy as np
assert np.isclose(dot([1, 2, 3], [4, 5, 6]), 32)
assert np.isclose(dot([1, 0], [0, 1]), 0)
assert np.isclose(dot([2, 3], [2, 3]), 13)
assert np.isclose(dot(np.array([0.5, 2]), [4, -1]), 0)
print("기초 1 통과")
```
