---
title: "Python Day 2 기초 1 — 평균 구하기와 범위 제한"
date: 2026-10-28 18:00:00 +0900
categories: [Notes, Python Practice]
tags: [python, default-parameter, if-elif]
---

> 🗂️ **Notes · Python Practice** — `python` `default-parameter` `if-elif`
{: .prompt-info }

---

## 1. 📝 문제

리스트 평균을 구하고, 값을 low~high 범위로 제한하는 문제

## 2. 💻 풀이

```python
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


def clamp(x, low=0, high=100):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x
```

## 3. 🔍 풀이 설명

- `average`: `sum()`으로 합을 구해 `len()`으로 나눈다.
- `clamp`: `low=0`, `high=100`을 기본값으로 두고, x가 low보다 작으면 low, high보다 크면 high, 그 사이면 x를 그대로 반환한다.

## 4. ✅ 테스트

```python
assert average([88, 92, 75]) == 85.0 and average([10]) == 10.0
assert clamp(150) == 100 and clamp(-5) == 0 and clamp(50) == 50
assert clamp(150, high=200) == 150 and clamp(5, 10, 20) == 10
print("기초 1 통과")
```
