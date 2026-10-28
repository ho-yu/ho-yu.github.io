---
title: "Python Day 1 기초 3 — 리스트 최댓값과 위치 찾기"
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

## 3. 🔍 풀이 설명

- 첫 번째 값과 인덱스 0을 최댓값 후보로 잡는다.
- 인덱스로 리스트를 돌며 현재 최댓값보다 큰 값이 나올 때만 값과 인덱스를 바꾼다.
- `>`로 비교하므로 같은 값이 다시 나와도 처음 위치가 유지된다.

## 4. ✅ 테스트

```python
assert max_with_index([12, 7, 25, 3, 19]) == (25, 2)
assert max_with_index([-5, -2, -9]) == (-2, 1)
assert max_with_index([4, 9, 9, 1]) == (9, 1)
assert max_with_index([7]) == (7, 0)
print("기초 3 통과")
```
