---
title: "Python 기초 3 — 리스트 최댓값과 위치 찾기"
date: 2026-10-27 14:02:00 +0900
categories: [Notes, Python Practice]
tags: [python, list, tuple, for-loop]
---

> 🗂️ **Notes · Python Practice** — `python` `list` `tuple` `for-loop`
{: .prompt-info }

---

## 1. 📝 문제

리스트의 최댓값과 그 값이 처음 나온 위치를 함께 반환하는 문제

## 2. 💻 풀이

```python
def max_with_index(numbers: list[int]) -> tuple[int, int]:
    max, index = numbers[0], 0

    for i in range(len(numbers)):
        if numbers[i] > max:
            max = numbers[i]
            index = i
    return max, index
```

## 3. ✅ 테스트

```python
assert max_with_index([12, 7, 25, 3, 19]) == (25, 2)
assert max_with_index([-5, -2, -9]) == (-2, 1)
assert max_with_index([4, 9, 9, 1]) == (9, 1)
assert max_with_index([7]) == (7, 0)
print("기초 3 통과")
```
