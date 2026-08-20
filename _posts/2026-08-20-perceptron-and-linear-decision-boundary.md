---
title: "퍼셉트론과 선형 결정 경계"
date: 2026-08-20 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [perceptron, linear-model, decision-boundary, weight, bias]
---

> 🗂️ **Notes · Deep Learning** — `perceptron` `linear-model` `decision-boundary` `weight` `bias`
{: .prompt-info }

---

## 1. 💡 핵심 개념

**퍼셉트론**은 입력을 받아 하나의 점수를 계산하고, 그 점수로 판단하는 가장 단순한
신경망 단위다. 입력값에 가중치를 곱하고 모두 더한 뒤 편향을 더한다:

`z = x₁w₁ + x₂w₂ + ... + xₙwₙ + b`

모델은 각 특성을 똑같이 보지 않는다. 어떤 특성은 더 중요하게, 어떤 특성은 덜 중요하게
본다. 이 중요도를 숫자로 표현한 것이 **가중치(weight)**다.

| 구성 요소 | 기호 | 역할 |
| --- | --- | --- |
| 입력 | `x` | 모델이 보고 판단할 데이터 |
| 가중치 | `w` | 각 입력을 얼마나 중요하게 볼지 정함 |
| 편향 | `b` | 전체 판단 기준을 조정 |

---

## 2. 🔍 이해하기 — 선형 결정 경계

2차원 입력에서 퍼셉트론의 판단 기준은 다음 식으로 표현된다:

`x₁w₁ + x₂w₂ + b = 0`

이 식은 2차원 평면에서 하나의 직선이다 — 한쪽은 class 0, 다른 한쪽은 class 1이 된다.

> 💡 **결정 경계(decision boundary)** · 모델이 두 클래스를 나누는 기준선이다. 퍼셉트론
> 하나는 2차원에서 직선, 3차원에서 평면, 더 높은 차원에서는 초평면으로 데이터를 나눈다.
{: .prompt-info }

아래 그림처럼 하나의 직선이 평면을 두 영역으로 나누고, 어느 쪽에 있는지로 class가 갈린다.

![선형 결정 경계 x₁w₁+x₂w₂+b=0이 평면을 class 0과 class 1 두 영역으로 나누는 모습](/assets/img/posts/perceptron-and-linear-decision-boundary/linear-decision-boundary.svg){: w="420" h="320" }

---

## 3. 🧪 코드 / 실습

### 여러 샘플 한 번에 계산하기

```python
import torch

# 데이터 4개, 특성이 2개인 2차원 텐서 생성.
X = torch.tensor([
    [1.0, 1.0],
    [2.0, 1.0],
    [1.0, 3.0],
    [4.0, 2.0]
])

# 가중치
w = torch.tensor([1.0, 0.7])

# 편향
b = torch.tensor(-0.2)

# X @ w는 각 샘플과 가중치의 내적을 한 번에 계산.
logits = X @ w + b

# .long()은 True/False 예측 결과를 분류에 사용할 정수 라벨 1/0으로 바꾸기 위해 사용.
preds = (logits > 0).long()

print("X shape     :", X.shape)
print("w shape     :", w.shape)
print("logits shape:", logits.shape)
print("logits      :", logits)
print("preds       :", preds)
```

---

## 4. ✅ 핵심 정리

- **퍼셉트론** : 입력·가중치·편향으로 점수 하나를 계산 (`z = x₁w₁+...+b`)
- **선형 결정 경계** : 2차원에서 직선, 3차원에서 평면, N차원에서 초평면
- **한계** : 퍼셉트론 하나로는 선형으로 나뉘지 않는 문제를 풀 수 없음 → MLP로 확장

---

## 5. 🔗 관련 글

- [선형모델 — Linear Regression과 Logistic Regression](/posts/linear-regression-and-logistic-regression/)
- [MLP의 입력층/은닉층/출력층](/posts/mlp-input-hidden-output-layers/)
