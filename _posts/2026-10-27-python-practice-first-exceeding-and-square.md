---
title: "Python 응용 3 — 누적합이 처음 넘는 지점과 최대 제곱수"
date: 2026-10-27 14:05:00 +0900
categories: [Notes, Python Practice]
tags: [python, while-loop, square-number]
---

> 🗂️ **Notes · Python Practice** — `python` `while-loop` `square-number`
{: .prompt-info }

---

## 1. 📝 문제

1부터 더한 합이 limit를 처음 넘는 지점과 n 이하 최대 제곱수 찾기

## 2. 💻 풀이

```python
def first_exceeding(limit: int) -> tuple[int, int]:
    # limit 까지 더함.
    count = 0
    sum = 0
    while True:
        if sum <= limit:
            count += 1
            sum += count
        else:
            break
    return count, sum


def largest_square_below(n: int) -> int:
    i = 0
    while (i + 1) * (i + 1) <= n:
        i += 1

    return i * i
```

## 3. ✅ 테스트

```python
assert first_exceeding(1000) == (45, 1035)
assert first_exceeding(0) == (1, 1)
assert first_exceeding(10) == (5, 15)
assert largest_square_below(2026) == 2025 and largest_square_below(16) == 16 and largest_square_below(1) == 1
print("응용 3 통과")
```
