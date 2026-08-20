---
title: "MLP의 입력층/은닉층/출력층"
date: 2026-08-20 11:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, mlp, hidden-layer, neural-network, relu]
mermaid: true
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `mlp` `hidden-layer` `neural-network` `relu`
{: .prompt-info }

---

## 1. 📖 개요

> 📌 **학습 목표**
> - MLP를 구성하는 입력층, 은닉층, 출력층의 역할을 구분할 수 있다.
> - 은닉층이 입력 feature를 새로운 표현으로 바꾼다는 의미를 설명할 수 있다.
> - `depth`, `width`, `hidden size`를 구분할 수 있다.
> - 각 층을 통과할 때 Tensor shape가 어떻게 바뀌는지 계산할 수 있다.
{: .prompt-tip }

---

## 2. 💡 핵심 개념

퍼셉트론을 여러 개 묶어 층(layer)을 만들고, 그 층을 여러 개 쌓아 MLP를 만든다.

```text
입력 데이터 → 은닉층 → 출력층 → 예측 점수
```

**MLP**(Multi-Layer Perceptron)는 여러 층을 가진 퍼셉트론 구조다.

```text
Perceptron 하나    → 선형 경계 하나
Perceptron 여러 개 → 여러 방향의 신호 계산
Layer 여러 개      → 표현을 단계적으로 변환
MLP                → 입력을 여러 단계로 변환해 출력 생성
```

> 💡 **핵심** · 입력 데이터를 바로 정답으로 바꾸는 게 아니라, 중간에 은닉층(hidden layer)을
> 통해 더 유용한 표현으로 바꾸는 것이다.
{: .prompt-info }

### 입력층 / 은닉층 / 출력층 역할

| 층 | 역할 | 예시 shape |
| --- | --- | --- |
| 입력층 | 원본 데이터를 받는다 | `(batch_size, input_dim)` |
| 은닉층 | 입력을 새로운 표현으로 변환한다 | `(batch_size, hidden_dim)` |
| 출력층 | 최종 예측 점수 또는 logits를 만든다 | `(batch_size, num_classes)` |

### MLP에서 흐름 읽기

`input_dim=3`, `hidden_dim=5`, `num_classes=2`일 때, 입력 Tensor가 `(4, 3)`이면
shape 흐름은 다음과 같다.

```mermaid
flowchart LR
    A["입력층<br/>X: (4, 3)"] --> B["Linear(3, 5)"] --> C["은닉층<br/>(4, 5)"]
    C --> D["ReLU"] --> E["(4, 5)"]
    E --> F["Linear(5, 2)"] --> G["출력층<br/>logits: (4, 2)"]
```

---

## 3. 🧪 코드 / 실습

### 중간 출력 직접 확인하기

```python
import torch
import torch.nn as nn

torch.manual_seed(42)

X = torch.randn(4, 3)

# 각 층을 변수로 분리해서 정의함.
fc1 = nn.Linear(3, 5)
relu = nn.ReLU()
fc2 = nn.Linear(5, 2)

# 1번째 linear
hidden_linear = fc1(X)

# relu
hidden_relu = relu(hidden_linear)

# 마지막 linear
logits = fc2(hidden_relu)

print("X               :", X.shape)
print("hidden_linear   :", hidden_linear.shape)
print("hidden_activated:", hidden_relu.shape)
print("logits          :", logits.shape)
```

### PyTorch로 2층 MLP 만들기

```python
import torch
import torch.nn as nn

torch.manual_seed(42)

X = torch.randn(4, 3)

# MLP 구조를 정의.
# Linear(3, 5): 입력 feature 3개를 hidden feature 5개로 변환.
# ReLU(): 은닉층 결과에 비선형성을 추가합니다.
# Linear(5, 2): hidden feature 5개를 class 2개에 대한 점수로 변환.
model = nn.Sequential(
    nn.Linear(3, 5),
    nn.ReLU(),
    nn.Linear(5, 2)
)

logits = model(X)

print("X shape     :", X.shape)
print("logits shape:", logits.shape)
print(logits)
```

### depth와 width

| 용어 | 의미 |
| --- | --- |
| depth | 층을 얼마나 깊게 쌓았는지 |
| width | 한 은닉층에 뉴런이 얼마나 많은지 |
| hidden size | 은닉층 출력 feature 수 |

```python
import torch.nn as nn

input_dim = 3
num_classes = 2

for hidden_dim in [2, 5, 10, 20]:
    model = nn.Sequential(
        nn.Linear(input_dim, hidden_dim),
        nn.ReLU(),
        nn.Linear(hidden_dim, num_classes)
    )

    total_params = sum(p.numel() for p in model.parameters())

    print(f"hidden_dim={hidden_dim:2d} -> total_params={total_params}")
```

> 💡 **hidden size** · 모델의 표현력과 parameter 수를 함께 바꾼다. 그래서 실험할 때
> hidden size는 중요한 하이퍼파라미터다.
{: .prompt-info }

---

## 4. ✅ 핵심 정리

- **MLP** : 여러 층으로 구성된 퍼셉트론 구조
- **입력층** : 원본 데이터를 받음
- **은닉층** : feature를 새로운 표현으로 변환
- **출력층** : 문제 유형에 맞는 최종 점수(logits) 생성
- **층 통과 시** : batch size는 유지되고 feature 차원만 바뀜

---

## 5. 🔗 관련 글

- [퍼셉트론과 선형 결정 경계](/posts/perceptron-and-linear-decision-boundary/)
- [가중치/편향과 nn.Linear](/posts/nn-linear-weight-bias/)
- [PyTorch 코드 기본 구조](/posts/pytorch-training-script-structure/)
