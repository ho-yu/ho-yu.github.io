---
title: "Python Day 3 심화 1 다시 풀기 — 주석으로 정리한 이진 탐색"
date: 2026-11-20 15:45:00 +0900
categories: [Notes, Python Practice]
tags: [python, binary-search, while-loop]
---

> 🗂️ **Notes · Python Practice** — `python` `binary-search` `while-loop`
{: .prompt-info }

---

## 1. 📝 문제

주석으로 단계별로 정리한 이진 탐색으로 target 인덱스 찾기

## 2. 💻 풀이

```python
# 이진 탐색
# 정렬되어 있으면 반씩 버림.

def binary_search(items, target):
    n = len(items)                                  # 리스트의 길이.
    low, high = 0, n - 1                            # 탐색 범위의 양 끝 인덱스.

    while low <= high:                              # 탐색 범위가 남아 있는 동안 반복.
        mid = (low + high) // 2                     # 범위의 가운데 인덱스.

        if items[mid] < target:                     # 가운데 값이 목표보다 작으면
            low = mid + 1                           # 왼쪽 절반은 버리고 오른쪽만 탐색.
        elif items[mid] > target:                   # 가운데 값이 목표보다 크면
            high = mid - 1                          # 오른쪽 절반은 버리고 왼쪽만 탐색.
        else:
            return mid                              # 찾았다 : 그 인덱스를 반환.

    return -1                                       # 범위가 비도록 못 찾았으면 -1.
```

## 3. 🔍 풀이 설명

- `low`, `high`로 탐색 범위의 양 끝을 잡고, 범위가 남아 있는 동안 가운데 인덱스 `mid`의 값을 본다.
- 가운데 값이 target보다 작으면 왼쪽 절반을, 크면 오른쪽 절반을 버리고, 같으면 `mid`를 반환한다.
- 범위가 비어 반복이 끝나면 -1을 반환한다.

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
