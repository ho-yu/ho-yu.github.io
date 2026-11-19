---
title: "Python Day 2 심화 1 — 딕셔너리로 두 수의 합 찾기"
date: 2026-11-19 15:51:00 +0900
categories: [Notes, Python Practice]
tags: [python, dictionary, enumerate]
---

> 🗂️ **Notes · Python Practice** — `python` `dictionary` `enumerate`
{: .prompt-info }

---

## 1. 📝 문제

합이 target인 두 수의 인덱스를 딕셔너리로 한 번에 찾는 문제

## 2. 💻 풀이

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}

    for i, n in enumerate(nums):
        if target - n in seen:
            return (seen[target - n], i)
        seen[n] = i
```

## 3. 🔍 풀이 설명

- `enumerate`로 인덱스와 값을 함께 돌면서, `target - n`이 이미 `seen`에 있으면 그 인덱스와 현재 인덱스를 반환한다.
- 없으면 현재 값을 키로, 인덱스를 값으로 `seen`에 저장한다.
- 리스트를 한 번만 돌기 때문에 20만 개 입력도 빨리 끝나고, 끝까지 못 찾으면 반환문 없이 끝나 `None`이 된다.

## 4. ✅ 테스트

```python
import random, time
assert two_sum([2, 7, 11, 15, 3], 9) == (0, 1)
assert two_sum([2, 7, 11, 15, 3], 14) == (2, 4)
assert two_sum([2, 7, 11, 15, 3], 100) is None
assert two_sum([2, 5], 4) is None
assert two_sum([3, 3], 6) == (0, 1)
random.seed(1)
big = [random.randint(1, 10_000_000) for _ in range(200_000)]
t0 = time.perf_counter(); two_sum(big, -1); elapsed = time.perf_counter() - t0
assert elapsed < 1.0, f"20만 개에 {elapsed:.2f}초: 이중 루프를 쓴 것 같아요"
print(f"심화 1 통과 (20만 개 {elapsed * 1000:.0f} ms)")
```
