---
title: "지도 학습과 비지도 학습 모델 비교"
date: 2026-08-17 16:39:53 +0900
categories: [Notes, Machine Learning]
tags: [supervised-learning, unsupervised-learning, knn, decision-tree, k-means]
---

> 🗂️ **Notes · Machine Learning** — `supervised-learning` `unsupervised-learning` `knn` `decision-tree` `k-means`
{: .prompt-info }

---

## 1. 📖 개요

> 📌 **왜 필요한가** · 지도/비지도 학습 모델 5개를 비교하고, 모델 선택 기준의 핵심 개념과 필요성을 파악한다.
{: .prompt-tip }

---

## 2. 💡 핵심 개념

처음에는 해석이 쉬운 단순한 모델을 선정하고, 필요에 따라 복잡한 모델로 넘어간다. 데이터 크기, 특성 스케일, 해석 필요성 등 여러 기준으로 후보를 좁혀 간다.

| 모델 | 핵심 질문 | 특징 |
| --- | --- | --- |
| Linear / Logistic | 선형적인 관계로 설명이 가능한가? | 해석이 쉽다 |
| KNN | 가까운 데이터들은 무엇인가? | 거리 기반, 스케일링 중요 |
| Decision Tree | 어떤 조건으로 나눌까? | 규칙 기반, 비선형 가능 |
| K-means | 비슷한 것끼리 어떻게 그룹화? | 비지도 군집화 |
| PCA | 특성을 어떻게 얼마나 줄이지? | 비지도 차원축소 |

> 💡 **한 줄 정리** · 설명이 중요하다면 선형 모델이나 결정 트리를 우선 검토한다.
{: .prompt-info }

---

## 3. 🔍 모델 선택 기준

- 설명이 중요하다 → Linear / Decision Tree
- 비선형 관계가 강하다 → Decision Tree / KNN
- 거리 기반으로 모델을 쓴다 → KNN
- 정답 없이 그룹을 찾는다 → K-means
- 특성이 너무 많아 줄이고 싶다 → PCA

---

## 4. ✅ 핵심 정리

- **모델 선택은 해석이 쉬운 단순한 모델에서 시작해 필요할 때 복잡한 모델로 넘어간다**
- **데이터 크기, 특성 스케일, 해석 필요성이 모델을 좁히는 기준이 된다**

---

## 5. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

**필수 암기 내용**

```text
설명 중요
→ 선형모델 / Decision Tree

비선형 강함
→ Decision Tree / KNN

거리 기반
→ 스케일링 확인

정답 없이 그룹화
→ K-means

특성 수 축소
→ PCA
```

**하이퍼파라미터 정리**

```text
n_neighbors  → KNN의 이웃 수
max_depth    → Decision Tree 깊이
n_clusters   → K-means 군집 수
n_components → PCA 축소 차원 수
```

</details>
