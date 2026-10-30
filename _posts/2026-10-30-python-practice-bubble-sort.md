---
title: "Python Day 3 응용 1 — 버블 정렬 구현하기"
date: 2026-10-30 12:11:00 +0900
categories: [Notes, Python Practice]
tags: [python, bubble-sort, nested-loop, sorting]
---

> 🗂️ **Notes · Python Practice** — `python` `bubble-sort` `nested-loop` `sorting`
{: .prompt-info }

---

## 1. 📝 문제

원본은 그대로 두고 버블 정렬로 정렬한 새 리스트를 반환하는 문제

## 2. 💻 풀이

```python
def bubble_sort(items):
    # 1,2 / 2,3 / 3,4 이렇게 한 칸씩 진행하면서 크기를 비교하고, 성립하면 바로 위치를 변경.
    # 변경 후, 그 다음 숫자와 크기를 비교.
    n = len(items)
    items = items[:]

    for i in range(n):
        for j in range(0, n-i-1):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
    return items
```

## 3. 🔍 풀이 설명

- `items[:]`로 복사본을 만들어서 원본 리스트는 바꾸지 않는다.
- 바깥 `for`를 n번 돌고, 안쪽 `for`에서 이웃한 두 값 `items[j]`와 `items[j+1]`을 비교해 앞이 더 크면 자리를 바꾼다.
- 한 바퀴가 끝날 때마다 가장 큰 값이 맨 뒤로 가므로, 안쪽 반복 범위를 `n-i-1`까지 줄인다.

## 4. ✅ 테스트

```python
import random

data = [5, 2, 9, 1, 7]
assert bubble_sort(data) == [1, 2, 5, 7, 9]
assert data == [5, 2, 9, 1, 7]                                # 원본은 그대로
assert bubble_sort([]) == [] and bubble_sort([7]) == [7] and bubble_sort([3, 3, 1]) == [1, 3, 3]
random.seed(0)
for _ in range(100):                                          # 무작위로 내 답을 sorted와 비교
    arr = [random.randint(0, 50) for _ in range(random.randint(0, 10))]
    assert bubble_sort(arr) == sorted(arr)
print("응용 1 통과")
```
