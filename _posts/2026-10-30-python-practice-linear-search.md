---
title: "Python Day 3 기초 1 — 선형 탐색으로 첫 위치 찾기"
date: 2026-10-30 12:10:00 +0900
categories: [Notes, Python Practice]
tags: [python, linear-search, for-loop]
---

> 🗂️ **Notes · Python Practice** — `python` `linear-search` `for-loop`
{: .prompt-info }

---

## 1. 📝 문제

리스트를 앞에서부터 훑어 target의 첫 인덱스(없으면 -1)를 찾는 문제

## 2. 💻 풀이

```python
def linear_search(items, target):
    # 돌다가 찾으면 해당 숫자 인덱스 뽑기.

    idx = 0
    result = 0
    count = 0

    for i in items:
        if i == target:
            result = idx
            count += 1
        else:
            idx += 1

    if count == 0:
        return -1

    return result
```

## 3. 🔍 풀이 설명

- `for`로 값을 하나씩 보면서, target과 다르면 `idx`를 1 늘리고 같으면 그때의 `idx`를 `result`에 저장하고 `count`를 센다.
- 끝까지 돈 뒤 `count`가 0이면 찾지 못한 것이므로 -1, 아니면 `result`를 반환한다.

## 4. ✅ 테스트

```python
assert linear_search([5, 2, 9, 1, 7], 9) == 2
assert linear_search([5, 2, 9, 1, 7], 5) == 0 and linear_search([5, 2, 9, 1, 7], 7) == 4
assert linear_search([5, 2, 9, 1, 7], 4) == -1 and linear_search([], 1) == -1
assert linear_search([3, 3, 3], 3) == 0                       # 여러 개면 맨 앞
print("기초 1 통과")
```
