---
title: "Python Day 2 응용 3 — 짝수 거르기와 2차원 격자 만들기"
date: 2026-11-19 15:50:00 +0900
categories: [Notes, Python Practice]
tags: [python, list-comprehension, list]
---

> 🗂️ **Notes · Python Practice** — `python` `list-comprehension` `list`
{: .prompt-info }

---

## 1. 📝 문제

리스트에서 짝수를 거르고, 행마다 따로인 2차원 격자를 만드는 문제

## 2. 💻 풀이

```python
def remove_evens(nums) -> list[int]:
    return [num for num in nums if num % 2 != 0]


def make_grid(rows, cols, fill=0) -> list[list]:
    grid = []
    for row in range(rows):
        grid.append([fill] * cols)
    return grid
```

## 3. 🔍 풀이 설명

- `remove_evens`: 리스트 컴프리헨션으로 홀수만 모은 새 리스트를 반환해서 원본 리스트는 바뀌지 않는다.
- `make_grid`: 행마다 `[fill] * cols`로 리스트를 새로 만들어 `grid`에 추가한다. 행을 매번 새로 만들기 때문에 한 칸을 바꿔도 다른 행은 그대로다.

## 4. ✅ 테스트

```python
original = [1, 2, 4, 6, 7]
result = remove_evens(original)
assert result == [1, 7] and original == [1, 2, 4, 6, 7]
assert remove_evens([2, 4]) == [] and remove_evens([]) == []
grid = make_grid(3, 3)
grid[0][0] = 99
assert grid == [[99, 0, 0], [0, 0, 0], [0, 0, 0]]
assert make_grid(2, 3, fill="-") == [["-", "-", "-"], ["-", "-", "-"]]
print("응용 3 통과")
```
