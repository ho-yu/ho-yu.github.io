---
title: "Python 기초 2 — 1부터 n까지의 합과 배수 개수"
date: 2026-10-27 14:01:00 +0900
categories: [Notes, Python Practice]
tags: [python, for-loop, range, floor-division]
---

> 🗂️ **Notes · Python Practice** — `python` `for-loop` `range` `floor-division`
{: .prompt-info }

---

## 1. 📝 문제

1부터 n까지의 합과 n 이하 k의 배수 개수를 구하는 문제

## 2. 💻 풀이

```python
def count_multiples(n: int, k: int) -> int:
    result = n // k
    return result


def sum_to(n: int) -> int:
    result = 0
    for i in range(1, n+1, 1):
        result += i
    return result
```

## 3. ✅ 테스트

```python
assert sum_to(100) == 5050 and sum_to(1) == 1 and sum_to(0) == 0
assert count_multiples(100, 3) == 33 and count_multiples(10, 5) == 2 and count_multiples(5, 7) == 0
print("기초 2 통과")
```
