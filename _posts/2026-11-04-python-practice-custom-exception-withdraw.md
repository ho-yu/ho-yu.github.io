---
title: "Python Day 5 응용 2 — 잔액 부족을 직접 만든 예외로 처리하기"
date: 2026-11-04 12:34:00 +0900
categories: [Notes, Python Practice]
tags: [python, custom-exception, try-except]
---

> 🗂️ **Notes · Python Practice** — `python` `custom-exception` `try-except`
{: .prompt-info }

---

## 1. 📝 문제

잔액보다 많이 출금하면 직접 만든 예외를 일으키는 문제

## 2. 💻 풀이

```python
class InsufficientFunds(Exception):
    pass


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"잔액 {balance}원, 요청 {amount}원")

    return balance - amount
```
{: file="wallet.py" }

## 3. 🔍 풀이 설명

- `InsufficientFunds`: `Exception`을 상속해 직접 만든 예외 클래스다.
- `withdraw`: 출금액이 잔액보다 크면 잔액과 요청 금액을 담은 메시지로 예외를 일으키고, 아니면 `balance - amount`를 반환한다.

## 4. ✅ 테스트

```python
from wallet import InsufficientFunds, withdraw
assert withdraw(1000, 300) == 700
try:
    withdraw(100, 500)
    assert False, "예외가 나야 해요"
except InsufficientFunds as e:
    assert "500" in str(e)
print("응용 2 통과")
```
{: file="q5.py" }
