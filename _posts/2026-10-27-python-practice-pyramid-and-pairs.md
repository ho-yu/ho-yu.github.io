---
title: "Python Day 1 응용 2 — 별 피라미드와 두 수 쌍의 개수"
date: 2026-10-27 14:04:00 +0900
categories: [Notes, Python Practice]
tags: [python, nested-loop, string, list]
---

> 🗂️ **Notes · Python Practice** — `python` `nested-loop` `string` `list`
{: .prompt-info }

---

## 1. 📝 문제

높이 n의 별 피라미드를 만들고 1~n에서 고를 수 있는 두 수 쌍 세기

## 2. 💻 풀이

```python
def pyramid(height: int) -> list[str]:
    result = []
    for i in range(1, height+1):
        result.append(" " * (height-i) + "*" * (2*i-1))
    return result


def count_pairs(n: int) -> int:
    result = 0

    for i in range(1, n+1):
        for j in range(i+1, n+1):
            result += 1
    return result
```

## 3. 🔍 풀이 설명

- `pyramid`: i번째 줄(1부터)은 왼쪽 공백 `height-i`개와 별 `2*i-1`개를 이어 붙인 문자열로 만들어 리스트에 추가한다.
- `count_pairs`: 이중 `for`문에서 j를 i+1부터 시작해 (i, j) 쌍을 중복 없이 하나씩 센다.

## 4. ✅ 테스트

```python
assert pyramid(1) == ["*"]
assert pyramid(3) == ["  *", " ***", "*****"]
assert pyramid(4)[-1] == "*******" and len(pyramid(4)) == 4
assert count_pairs(6) == 15 and count_pairs(2) == 1 and count_pairs(1) == 0
print("응용 2 통과")
```
