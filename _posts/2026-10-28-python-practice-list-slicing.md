---
title: "Python Day 2 기초 2 — 슬라이싱으로 앞·뒤·건너뛰기·양끝 제외"
date: 2026-10-28 18:01:00 +0900
categories: [Notes, Python Practice]
tags: [python, slicing, list, string]
---

> 🗂️ **Notes · Python Practice** — `python` `slicing` `list` `string`
{: .prompt-info }

---

## 1. 📝 문제

슬라이싱으로 앞·뒤 n개, 한 칸씩 건너뛰기, 양끝 제외를 구하는 문제

## 2. 💻 풀이

```python
def head(items, n):
    if n >= len(items):
        return items
    elif n <= 0:
        return []
    else:
        return items[:n]


def tail(items, n):
    if n == 0:
        return []
    else:
        return items[3::]


def every_other(data):
    return data[::2]


def drop_edges(data):
    if len(data) <= 2:
        return []

    return data[1:-1]
```

## 3. ✅ 테스트

```python
data = [88, 92, 75, 60, 99]
assert head(data, 2) == [88, 92] and head(data, 10) == data and head(data, 0) == []
assert tail(data, 2) == [60, 99] and tail(data, 0) == []
assert every_other(data) == [88, 75, 99] and every_other([]) == []
assert drop_edges(data) == [92, 75, 60] and drop_edges([1]) == [] and drop_edges([1, 2]) == []
assert head("python", 3) == "pyt" and every_other("abcdef") == "ace"
print("기초 2 통과")
```
