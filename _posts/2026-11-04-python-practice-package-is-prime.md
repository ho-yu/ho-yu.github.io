---
title: "Python Day 5 응용 1 — 패키지에서 소수 판별 함수 가져오기"
date: 2026-11-04 12:33:00 +0900
categories: [Notes, Python Practice]
tags: [python, package, import]
---

> 🗂️ **Notes · Python Practice** — `python` `package` `import`
{: .prompt-info }

---

## 1. 📝 문제

tools 패키지의 is_prime을 from tools import로 가져오게 하는 문제

## 2. 💻 풀이

```python
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True
```
{: file="tools/numbers.py" }

```python
from .numbers import is_prime    # 끌어올리기: from tools import is_prime 이 되게
```
{: file="tools/__init__.py" }

## 3. 🔍 풀이 설명

- `is_prime`: 2 미만이면 `False`, 2부터 n-1까지 나누어떨어지는 수가 있으면 `False`, 없으면 `True`를 반환한다.
- `__init__.py`: `from .numbers import is_prime`으로 함수를 패키지 최상위로 끌어올린다.
- 그래서 `from tools import is_prime`과 `from tools.numbers import is_prime`이 같은 함수 객체를 가리킨다.

## 4. ✅ 테스트

```python
from tools import is_prime
from tools.numbers import is_prime as is_prime2
assert is_prime(97) and not is_prime(1) and not is_prime(91)
assert is_prime is is_prime2                       # 같은 함수 객체
print("응용 1 통과")
```
{: file="q4.py" }
