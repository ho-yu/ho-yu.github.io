---
title: "Python Day 7 기초 2 — axis로 과목별 평균 구하기"
date: 2026-11-18 12:21:00 +0900
categories: [Notes, Python Practice]
tags: [python, numpy, axis]
---

> 🗂️ **Notes · Python Practice** — `python` `numpy` `axis`
{: .prompt-info }

---

## 1. 📝 문제

학생×과목 점수 배열에서 axis=0으로 과목별 평균을 구하는 문제

## 2. 💻 풀이

```python
def subject_means(scores):
    return np.array(scores).mean(axis=0)
```

## 3. 🔍 풀이 설명

- `np.array(scores)`로 배열로 만든 뒤 `mean(axis=0)`으로 행(학생) 방향을 따라 평균을 내어, 과목마다 값 하나씩 얻는다.

## 4. ✅ 테스트

```python
import numpy as np
r = subject_means(np.array([[80, 90, 70], [60, 70, 100]]))
assert np.shape(r) == (3,) and np.allclose(r, [70, 80, 85])
assert np.allclose(subject_means(np.ones((4, 2))), [1, 1])
print("기초 2 통과")
```
