---
title: "Python Day 8 기초 3 — 행렬 곱 결과 shape 판단하기"
date: 2026-11-18 12:28:00 +0900
categories: [Notes, Python Practice]
tags: [python, matrix, shape]
---

> 🗂️ **Notes · Python Practice** — `python` `matrix` `shape`
{: .prompt-info }

---

## 1. 📝 문제

두 행렬 shape로 곱셈 가능 여부와 결과 shape를 구하는 문제

## 2. 💻 풀이

```python
def result_shape(s1, s2):
    print(s1)
    print(s2)

    if s1[1] != s2[0]:
        return None
    return (s1[0], s2[1])
```

## 3. 🔍 풀이 설명

- 입력받은 두 shape를 `print`로 출력한다.
- 앞 행렬의 열 수 `s1[1]`과 뒤 행렬의 행 수 `s2[0]`이 다르면 `None`, 같으면 `(s1[0], s2[1])`을 반환한다.

## 4. ✅ 테스트

```python
import numpy as np
assert result_shape((2, 3), (3, 4)) == (2, 4)
assert result_shape((5, 2), (2, 1)) == (5, 1)
assert result_shape((1, 1), (1, 1)) == (1, 1)
assert result_shape((2, 3), (2, 3)) is None
print("기초 3 통과")
```
