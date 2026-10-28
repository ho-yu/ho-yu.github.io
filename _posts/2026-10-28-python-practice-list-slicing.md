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

## 3. 🔍 풀이 설명

- `head`: n이 길이 이상이면 전체, 0 이하면 빈 리스트, 그 외에는 `items[:n]`으로 앞 n개를 자른다.
- `tail`: n이 0이면 빈 리스트, 아니면 `items[3::]`로 인덱스 3부터 끝까지 자른다.
- `every_other`: `data[::2]`로 한 칸씩 건너뛰며 가져온다.
- `drop_edges`: 길이가 2 이하면 빈 리스트, 아니면 `data[1:-1]`로 양 끝을 뺀다.

## 4. ✅ 테스트

```python
data = [88, 92, 75, 60, 99]
assert head(data, 2) == [88, 92] and head(data, 10) == data and head(data, 0) == []
assert tail(data, 2) == [60, 99] and tail(data, 0) == []
assert every_other(data) == [88, 75, 99] and every_other([]) == []
assert drop_edges(data) == [92, 75, 60] and drop_edges([1]) == [] and drop_edges([1, 2]) == []
assert head("python", 3) == "pyt" and every_other("abcdef") == "ace"
print("기초 2 통과")
```
