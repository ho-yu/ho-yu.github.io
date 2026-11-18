---
title: "Python Day 1 심화 1 — 소수 판별과 소수 목록 만들기"
date: 2026-11-18 14:40:00 +0900
categories: [Notes, Python Practice]
tags: [python, prime-number, list-comprehension]
---

> 🗂️ **Notes · Python Practice** — `python` `prime-number` `list-comprehension`
{: .prompt-info }

---

## 1. 📝 문제

제곱근까지만 나눠 소수를 판별하고 limit 이하 소수 목록을 만드는 문제

## 2. 💻 풀이

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, math.isqrt(n)+1, 2):
        if n % i == 0:
            return False

    return True


def primes_up_to(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_prime(n)]
```

## 3. 🔍 풀이 설명

- `is_prime`: 2 미만이면 `False`, 2는 `True`, 2가 아닌 짝수는 `False`를 바로 반환한다.
- 나머지는 3부터 `math.isqrt(n)`까지 홀수로만 나눠 보고, 나누어떨어지면 `False`, 끝까지 없으면 `True`를 반환한다.
- `primes_up_to`: 리스트 컴프리헨션으로 2부터 limit까지의 수 중 `is_prime`이 `True`인 수만 모은다.

## 4. ✅ 테스트

```python
import math
assert [n for n in range(1, 30) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
assert is_prime(49) is False and is_prime(97) is True and is_prime(1) is False
assert len(primes_up_to(100)) == 25 and primes_up_to(100)[-1] == 97
assert primes_up_to(10) == [2, 3, 5, 7] and primes_up_to(1) == []
assert primes_up_to(1000) == [n for n in range(1001) if is_prime(n)]
print("심화 1 통과")
```
