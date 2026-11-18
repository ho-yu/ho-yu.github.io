---
title: "Python Day 8 기초 2 — 벡터의 길이(norm) 구하기"
date: 2026-11-18 12:27:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, vector, norm]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `vector` `norm`
{: .prompt-info }

---

## 1. 📝 문제

벡터 원소의 제곱합에 제곱근을 씌워 길이를 구하는 문제

## 2. 💻 풀이

```python
def norm(a):
    a = np.asarray(a, dtype=float)
    result = float(np.sqrt((a * a).sum()))
    return result
```

## 3. 🔍 풀이 설명

- 실수 배열로 바꾸고 `(a * a).sum()`으로 제곱합을 구한다.
- `np.sqrt`로 제곱근을 씌운 값을 `float`로 바꿔 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
assert np.isclose(norm([3, 4]), 5)
assert np.isclose(norm([0, 0]), 0)
assert np.isclose(norm([1, 2, 2]), 3)
assert np.isclose(norm([-3, -4]), 5)
print("기초 2 통과")
```
