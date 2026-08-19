---
title: "선형모델 — Linear Regression과 Logistic Regression"
date: 2026-08-13 09:00:00 +0900
categories: [Notes, Machine Learning]
tags: [linear-model, linear-regression, logistic-regression, regression, classification]
---

> 🗂️ **Notes · Machine Learning** — `linear-model` `linear-regression` `logistic-regression` `regression` `classification`
{: .prompt-info }

---

## 1. 🔍 이해하기

여러 재료의 양을 재서 요리의 맛 점수를 예측한다고 하자. "소금 1g마다 맛 점수가 0.3점씩 오른다"처럼
각 재료(특성)의 기여를 더하는 단순한 저울질이 선형모델이다. 이 저울질의 결과를 그대로 쓰면
(Linear Regression) 연속적인 점수를 예측하고, 그 결과를 "합격/불합격" 확률로 눌러 짜내면
(Logistic Regression) 분류가 된다.

---

## 2. 💡 핵심 개념

**선형모델**은 입력을 가중합하고 절편을 더하는 구조(아핀변환, affine transformation)로 예측한다:
`예측값 = w₁x₁ + w₂x₂ + … + wₙxₙ + b`.

**Linear Regression**은 이 값을 그대로 연속값 예측(회귀)에 쓰고, **Logistic Regression**은
이 선형결합으로 양성의 **로그 오즈(log-odds)**를 모델링한 뒤 로지스틱 함수로 0~1 사이의
확률로 바꿔 분류에 쓴다.

---

## 3. ✅ 핵심 정리

- **선형모델** : 여러 입력(특성)의 가중합 + 절편으로 예측하는 구조 (아핀변환)
- **Linear Regression** : 가중합 결과를 그대로 사용해 연속값(회귀)을 예측한다
- **Logistic Regression** : 가중합 결과(로그 오즈)를 로지스틱 함수로 0~1 확률로 바꿔 분류에 쓴다

---

## 4. 🔗 관련 글

- [지도·비지도 5개 모델 비교와 선택 기준](/posts/model-selection-linear-knn-tree-kmeans-pca/)
