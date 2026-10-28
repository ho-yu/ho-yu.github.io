---
title: "Python Day 1 기초 1 — 점수 구간별 학점 구하기"
date: 2026-10-27 14:00:00 +0900
categories: [Notes, Python Practice]
tags: [python, if-elif, assert]
---

> 🗂️ **Notes · Python Practice** — `python` `if-elif` `assert`
{: .prompt-info }

---

## 1. 📝 문제

점수 구간에 따라 A·B·C·F 학점을 반환하는 문제

## 2. 💻 풀이

```python
def grade(score: int) -> str:
    if score >= 90 and score <= 95:
        grade = "A"
    elif score >= 80 and score <= 89:
        grade = "B"
    elif score >= 70 and score <= 79:
        grade = "C"
    else:
        grade = "F"
    return grade
```

## 3. ✅ 테스트

```python
assert grade(95) == "A" and grade(90) == "A"
assert grade(89) == "B" and grade(80) == "B"
assert grade(79) == "C" and grade(70) == "C"
assert grade(69) == "F" and grade(0) == "F"
print("기초 1 통과")
```
