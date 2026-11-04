---
title: "Python Day 5 심화 1 — 이름과 점수 한 줄 파싱하기"
date: 2026-11-04 12:35:00 +0900
categories: [Notes, Python Practice]
tags: [python, value-error, try-except, string]
---

> 🗂️ **Notes · Python Practice** — `python` `value-error` `try-except` `string`
{: .prompt-info }

---

## 1. 📝 문제

"이름,점수" 한 줄을 파싱하고 형식이 틀리면 ValueError를 내는 문제

## 2. 💻 풀이

```python
def parse_records(line):
    str = line.strip().split(",")

    if len(str) != 2:
        raise ValueError("조각이 2개가 아닙니다.")

    name, score = str[0].strip(), str[1].strip()

    try:
        score = int(score)
    except ValueError:
        raise ValueError("점수가 정수가 아닙니다") from None

    return name, score
```
{: file="validate.py" }

## 3. 🔍 풀이 설명

- `strip()`으로 앞뒤 공백을 지운 뒤 `split(",")`으로 나누고, 조각이 2개가 아니면 `ValueError`를 일으킨다.
- 이름과 점수 조각의 공백을 각각 지운다.
- 점수를 `int()`로 바꾸다 실패하면 메시지를 바꾼 `ValueError`를 `from None`으로 다시 일으키고, 성공하면 `(이름, 점수)`를 반환한다.

## 4. ✅ 테스트

```python
from validate import parse_records
assert parse_records("영희,88") == ("영희", 88) and parse_records(" 철수 , 95 ") == ("철수", 95)
for bad in ["영희", "영희,abc", "a,b,c"]:
    try:
        parse_records(bad)
        assert False, bad
    except ValueError:
        pass
print("심화 1 통과")
```
{: file="q7.py" }
