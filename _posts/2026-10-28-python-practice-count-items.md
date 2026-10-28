---
title: "Python Day 2 기초 3 — 딕셔너리로 개수 세기와 최빈 항목"
date: 2026-10-28 18:02:00 +0900
categories: [Notes, Python Practice]
tags: [python, dictionary, list]
---

> 🗂️ **Notes · Python Practice** — `python` `dictionary` `list`
{: .prompt-info }

---

## 1. 📝 문제

리스트 항목별 개수를 딕셔너리로 세고 가장 많은 항목 찾기

## 2. 💻 풀이

```python
def count_items(items: list[str]) -> dict[str, int]:
    counts = {}
    for i in items:
        counts[i] = counts.get(i, 0) + 1

    return counts


def most_common_item(items: list[str]) -> str:
    counts = count_items(items)
    result = max(counts, key=counts.get)
    return result
```

## 3. ✅ 테스트

```python
fruits = ["사과", "배", "사과", "감", "배", "사과"]
assert count_items(fruits) == {"사과": 3, "배": 2, "감": 1}
assert count_items([]) == {}
assert list(count_items(fruits).keys()) == ["사과", "배", "감"]
assert most_common_item(fruits) == "사과" and most_common_item(["a", "b", "b"]) == "b"
print("기초 3 통과")
```
