---
title: "Python Day 7 기초 3 — 기준보다 큰 값 개수 세기"
date: 2026-11-18 12:22:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, boolean-mask]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `boolean-mask`
{: .prompt-info }

---

## 1. 📝 문제

배열에서 기준값 t보다 큰 원소가 몇 개인지 세는 문제

## 2. 💻 풀이

```python
def count_above(a, t):
    a = np.asarray(a)
    return int((a > t).sum())
```

## 3. 🔍 풀이 설명

- `a > t`로 원소마다 True / False인 배열을 만든다.
- `.sum()`으로 True의 개수를 세고 `int`로 바꿔 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
a = np.array([3, -1, 7, 0, 5, -4])
assert count_above(a, 2) == 3 and count_above(a, 100) == 0 and count_above(a, -10) == 6
assert count_above([1, 2, 3], 1) == 2
print("기초 3 통과")
```
