---
title: "비선형성과 활성화 함수 / ReLU의 역할"
date: 2026-08-21 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [nonlinearity, activation-function, relu, xor, pytorch]
---

> 🗂️ **Notes · Deep Learning** — `nonlinearity` `activation-function` `relu` `xor` `pytorch`
{: .prompt-info }

---

## 1. 📖 개요

> 📌 **왜 필요한가** · Linear를 아무리 여러 겹 쌓아도 활성화 함수가 없으면 결국 하나의 큰
> 선형 변환과 같아져서 복잡한 비선형 관계를 학습하지 못한다. 활성화 함수는 모델에
> 비선형성을 넣어주는 장치다.
{: .prompt-tip }

---

## 2. 💡 핵심 개념

### 비선형성이 필요한 이유

XOR처럼 직선 하나로 나누기 어려운 패턴을 표현하려면 비선형성이 필요하다.

아래 그림처럼 XOR은 class 0에 해당하는 두 점 `(0,0)`, `(1,1)`과 class 1에 해당하는 두 점
`(0,1)`, `(1,0)`이 대각선으로 놓여 있어서, 어떤 직선을 그어도 두 class를 한 번에 나눌 수 없다.

![XOR 데이터의 class 0 두 점과 class 1 두 점은 대각선으로 배치되어 있어 하나의 직선으로 분리할 수 없다](/assets/img/posts/activation-function-and-relu/xor-not-linearly-separable.svg){: w="420" h="350" }
_직선 하나로는 XOR의 두 class를 분리할 수 없다_

> 💡 **핵심** · Linear만 연속으로 쌓으면 하나의 Linear로 압축할 수 있지만, ReLU처럼 입력에
> 따라 동작이 달라지는 함수가 들어가면 전체를 하나의 Linear로 압축할 수 없다.
{: .prompt-info }

### Linear를 여러 겹 쌓아도 하나로 합쳐지는 이유

`nn.Linear`는 선형 변환에 bias를 더한 아핀 변환(affine transformation)이다.

```python
output = input @ weight.T + bias
```

Linear 두 개를 연속으로 통과시키면 다음과 같다.

```text
h   = x @ W1.T + b1
out = h @ W2.T + b2
```

이는 아래처럼 풀어 쓸 수 있다.

```text
out = (x @ W1.T + b1) @ W2.T + b2
    = x @ W1.T @ W2.T + b1 @ W2.T + b2
```

결국 아래와 동일한 형태가 된다.

```text
out = x @ W_new.T + b_new
```

즉, 선형층을 여러 개 쌓아도 중간에 활성화 함수가 없으면 다시 하나의 선형층으로 합쳐질 수
있다. Linear → Linear를 여러 번 해도 ReLU 같은 비선형 함수가 없으면, 결국 하나의 Linear
계산으로 합칠 수 있다는 뜻이다. 이것이 중간에 ReLU를 굳이 넣는 이유다.

> 💡 **한 줄 정리** · 활성화 함수는 주로 tensor의 값을 비선형적으로 바꾸는 역할을 한다.
{: .prompt-info }

### XOR 문제로 보는 비선형성

XOR 데이터는 선형모델 하나만으로 표현하기 어렵다. MLP에 활성화 함수를 넣으면 여러 개의
선형 경계를 조합해, 비선형 경계를 만들 수 있다. 일반적인 MLP에서는 활성화 함수를 은닉층
뒤에 넣는다.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(2, 8),  # 입력 feature 2개 -> hidden feature 8개
    nn.ReLU(),        # 첫 번째 은닉층 뒤의 활성화 함수
    nn.Linear(8, 8),  # hidden feature 8개 -> hidden feature 8개
    nn.ReLU(),        # 두 번째 은닉층 뒤의 활성화 함수
    nn.Linear(8, 2)   # class 2개에 대한 logits 출력
)
```

---

## 3. 🧪 ReLU

### ReLU란

ReLU는 음수는 0으로 바꾸고, 양수는 그대로 통과시킨다.

```python
ReLU(x) = max(0, x)
```

![ReLU 함수 그래프 — x가 0보다 작으면 0, 0보다 크면 입력값을 그대로 출력한다](/assets/img/posts/activation-function-and-relu/relu-function.png){: w="460" h="340" }
_ReLU(x) = max(0, x)_

> 💡 **핵심** · ReLU는 tensor의 shape을 바꾸는 층이 아니라 값을 바꾸는 층이다. 입력값이
> 0보다 작으면 0을 출력하고, 0보다 크면 입력값을 그대로 출력한다.
{: .prompt-info }

### MLP에서 ReLU의 위치

MLP에서 ReLU는 은닉층 뒤에 넣는다.

```text
입력 -> Linear -> ReLU -> Linear -> ReLU -> Linear -> 출력 logits
```

```text
1. Linear가 feature를 새로운 공간으로 변환합니다.
2. ReLU가 그 변환 결과를 비선형적으로 꺾습니다.
3. 다음 Linear가 꺾인 표현을 다시 조합합니다.

Linear와 ReLU가 번갈아 나오면서 모델은 더 복잡한 패턴을 표현할 수 있습니다.
```

### gradient 흐름과 dead ReLU

ReLU는 양수 영역에서는 기울기가 1이고, 음수 영역에서는 기울기가 0이다. x > 0이면
gradient가 흐르고, x < 0이면 gradient가 0이 된다.

![ReLU의 gradient 그래프 — x가 0보다 작은 구간은 gradient가 0, 0보다 큰 구간은 gradient가 1이다](/assets/img/posts/activation-function-and-relu/relu-gradient.png){: w="460" h="340" }
_ReLU의 gradient는 음수 구간에서 0, 양수 구간에서 1이다_

> ⚠️ **dead ReLU** · 어떤 뉴런이 계속 음수 값만 출력해서 ReLU 뒤에 항상 0이 된다면, 그
> 뉴런은 학습 신호를 거의 받지 못할 수 있다. 이런 상황을 직관적으로 dead ReLU라고 부른다.
{: .prompt-warning }

---

## 4. ✅ 핵심 정리

- **선형층만 쌓으면** : 활성화 함수 없이 Linear만 여러 개 쌓으면 전체적으로 하나의 선형 변환처럼 동작함
- **활성화 함수** : 모델에 비선형성을 넣어주는 장치
- **XOR** : 직선 하나로 정확히 분리할 수 없는 문제로, 비선형성의 필요성을 보여줌
- **ReLU 위치** : 일반적인 MLP에서는 은닉층의 `Linear` 뒤에 `ReLU`를 넣음
- **ReLU 계산** : `ReLU(x) = max(0, x)`, 음수는 0으로 만들고 양수는 그대로 통과시킴
- **ReLU의 역할** : Tensor의 shape가 아니라 값을 바꿈
- **ReLU의 gradient** : 양수 구간은 1, 음수 구간은 0
- **dead ReLU** : 뉴런이 계속 음수만 출력해 gradient가 0이 되어 학습 신호를 거의 받지 못하는 상태
- **출력층** : 문제 유형과 loss 함수에 맞게 별도로 설계해야 하며, 출력층 뒤에 ReLU를 무조건 붙이면 안 됨

---

## 5. 🔗 관련 글

- [가중치/편향과 nn.Linear](/posts/nn-linear-weight-bias/)
- [MLP의 입력층/은닉층/출력층](/posts/mlp-input-hidden-output-layers/)
