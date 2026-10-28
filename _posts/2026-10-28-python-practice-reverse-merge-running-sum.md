---
title: "Python Day 2 응용 1 — 리스트 뒤집기, 합치기, 누적합"
date: 2026-10-28 18:03:00 +0900
categories: [Notes, Python Practice]
tags: [python, list, sorted, for-loop]
---

> 🗂️ **Notes · Python Practice** — `python` `list` `sorted` `for-loop`
{: .prompt-info }

---

## 1. 📝 문제

리스트 뒤집기, 두 정렬 리스트 합치기, 누적합 리스트를 만드는 문제

## 2. 💻 풀이

```python
def reverse_list(items) -> list:
    result = []
    if items == []:
        return []

    for i in range(len(items), 0, -1):
        result.append(i)

    return result


def interleave(a, b) -> list:
    # 더하고, 정렬
    return sorted(a + b)


def running_sum(numbers) -> list[int]:
    # 순회하면서 각 인덱스별 전 값과 해당 값을 더함.
    result = []
    total = 0

    for i in range(len(numbers)):
        total += numbers[i]
        result.append(total)

    return result
```

## 3. ✅ 테스트

```python
assert reverse_list([1, 2, 3, 4]) == [4, 3, 2, 1] and reverse_list([]) == []
assert interleave([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
assert interleave([1, 3, 5, 7, 9], [2, 4]) == [1, 2, 3, 4, 5, 7, 9]
assert interleave([], [1, 2]) == [1, 2]
assert running_sum([1, 2, 3, 4, 5]) == [1, 3, 6, 10, 15] and running_sum([3, -1, 4]) == [3, 2, 6] and running_sum([]) == []
print("응용 1 통과")
```
