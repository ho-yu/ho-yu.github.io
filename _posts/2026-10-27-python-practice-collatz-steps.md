---
title: "Python 응용 1 — 콜라츠 단계 수와 가장 긴 수"
date: 2026-10-27 14:03:00 +0900
categories: [Notes, Python Practice]
tags: [python, while-loop, collatz]
---

> 🗂️ **Notes · Python Practice** — `python` `while-loop` `collatz`
{: .prompt-info }

---

## 1. 📝 문제

콜라츠 규칙으로 1이 되는 단계 수와 limit 이하에서 가장 긴 수 찾기

## 2. 💻 풀이

```python
def collatz_steps(n: int) -> int:
    count = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1
        count += 1
    return count


def longest_collatz(limit: int) -> int:
    max_step, max_num = 0, 0

    for i in range(1, limit+1):
        steps = collatz_steps(i)

        if steps > max_step:
            max_step = steps
            max_num = i

    return max_num
```

## 3. ✅ 테스트

```python
assert collatz_steps(1) == 0 and collatz_steps(6) == 8 and collatz_steps(7) == 16 and collatz_steps(27) == 111
assert longest_collatz(100) == 97 and longest_collatz(10) == 9
print("응용 1 통과")
```
