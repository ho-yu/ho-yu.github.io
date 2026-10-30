---
title: "Python Day 3 심화 1 — 이진 탐색 구현하기"
date: 2026-10-30 12:12:00 +0900
categories: [Notes, Python Practice]
tags: [python, binary-search, while-loop]
---

> 🗂️ **Notes · Python Practice** — `python` `binary-search` `while-loop`
{: .prompt-info }

---

## 1. 📝 문제

정렬된 리스트에서 이진 탐색으로 target 인덱스(없으면 -1) 찾기

## 2. 💻 풀이

```python
def binary_search(items, target):
    low, high = 0, len(items) - 1

    while low <= high:
        mid = (low + high) // 2

        if items[mid] < target:
            low = mid + 1
        elif items[mid] > target:
            high = mid - 1
        else:
            return mid

    return -1
```

## 3. 🔍 풀이 설명

- `low`, `high`를 리스트 양 끝 인덱스로 두고 `low <= high`인 동안 반복한다.
- 가운데 `mid`의 값이 target보다 작으면 오른쪽 절반(`low = mid + 1`), 크면 왼쪽 절반(`high = mid - 1`)만 남긴다.
- 값이 같으면 `mid`를 반환하고, 범위가 비어 반복이 끝나면 -1을 반환한다.

## 4. ✅ 테스트

```python
import random
s = [1, 3, 5, 7, 9, 11, 13]
assert binary_search(s, 11) == 5 and binary_search(s, 1) == 0 and binary_search(s, 13) == 6
assert binary_search(s, 4) == -1 and binary_search([], 1) == -1 and binary_search([5], 5) == 0
big = list(range(0, 2_000_000, 2))
assert binary_search(big, 1_999_998) == 999_999 and binary_search(big, 7) == -1
random.seed(0)
for _ in range(100):                                          # 무작위로 내 답을 index와 비교
    arr = sorted(random.sample(range(100), random.randint(0, 20)))
    x = random.randint(0, 100)
    assert binary_search(arr, x) == (arr.index(x) if x in arr else -1)
print("심화 1 통과")
```
