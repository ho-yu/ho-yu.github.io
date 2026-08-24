---
title: "PyTorch 학습 5단계와 비지도학습"
date: 2026-08-24 16:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, training-loop, backpropagation, optimizer, unsupervised-learning]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `training-loop` `backpropagation` `optimizer` `unsupervised-learning`
{: .prompt-info }

---

## 1. 💡 모델 학습 기본 5단계

PyTorch의 기본 학습 흐름은 다음 5단계로 이해하면 된다.

```python
optimizer.zero_grad()
outputs = model(inputs)
loss = criterion(outputs, targets)
loss.backward()
optimizer.step()
```

이 다섯 줄이 하는 일을 그림으로 보면 다음과 같다.

![한 Batch를 학습하는 5단계 — ① zero_grad로 이전 Gradient를 초기화하고, ② 입력이 Model을 지나 예측값이 되며, ③ 예측값과 정답값을 비교해 Loss를 만들고, ④ backward()가 각 Weight의 Gradient를 계산한 뒤, ⑤ optimizer.step()이 실제 Weight를 수정해 다음 Batch로 이어진다](/assets/img/posts/pytorch-training-5-steps/training-5-steps.svg){: w="700" h="350" }

이 과정을 Batch마다 반복하고, **전체 학습 데이터를 한 번 모두 처리하면 1 Epoch**이다.

---

## 2. 📖 각 단계가 하는 일

### ① `optimizer.zero_grad()`

이전 학습에서 계산된 **Gradient를 초기화**한다.

```text
이전 Gradient 제거
→ 새로운 Batch의 Gradient를 다시 계산할 준비
```

> ⚠️ PyTorch는 Gradient를 기본적으로 누적하기 때문에 일반적인 학습에서는 매번 초기화한다.
{: .prompt-warning }

### ② `outputs = model(inputs)`

현재 Weight를 이용해 **예측값을 계산**한다. 이 과정을 **순전파(Forward)**라고 한다.

### ③ `loss = criterion(outputs, targets)`

예측값과 실제 정답을 비교해 **Loss를 계산**한다.

예를 들어 `MSELoss`라면:

```text
예측값 - 실제값
      ↓
     제곱
      ↓
     평균
      ↓
     Loss
```

### ④ `loss.backward()`

Loss를 기준으로 **각 Weight의 Gradient를 계산**한다. 이 과정을
**역전파(Backpropagation)**라고 한다.

> ⚠️ `backward()`는 **Gradient 계산까지만** 한다. Weight 수정은 아직 하지 않는다.
{: .prompt-warning }

### ⑤ `optimizer.step()`

계산된 Gradient와 Learning Rate를 이용해 **실제 Weight를 수정**한다.

SGD의 기본 원리:

```text
새 Weight
= 기존 Weight - Learning Rate × Gradient
```

| 무엇이 | 무엇을 정하는가 |
| --- | --- |
| Gradient | 어느 방향으로 수정할지 |
| Learning Rate | 얼마나 크게 수정할지 |
| Optimizer | 실제 Weight 수정 |

---

## 3. 🔍 이 방식은 지도학습에서 가장 전형적이다

지도학습은 **정답(Target)이 있는 데이터로 학습**한다. 위 5단계는 그 전형적인 형태이다.

예:

- 집값 예측
- 판매량 예측
- 정상 / 불량 분류
- 이미지 분류

---

## 4. 🔍 비지도학습은 어떻게 다른가?

비지도학습(Unsupervised Learning)은 **정답 라벨 없이 데이터 안의 구조나 패턴을 찾는
방식**이다.

```text
고객 데이터
나이 / 구매금액 / 방문횟수
        ↓
비슷한 고객끼리 그룹화
```

대표적인 방법:

| 방법 | 하는 일 |
| --- | --- |
| `Clustering` | 비슷한 데이터끼리 묶기 |
| `PCA` | 중요한 특징만 남겨 차원 축소 |
| `Autoencoder` | 입력 데이터를 압축한 뒤 다시 복원 |

신경망 기반 비지도학습에서는 정답 라벨 대신 **데이터 자체에서 Loss를 계산하는 기준을
만든다.** 예를 들어 Autoencoder는 아래 그림처럼 **정답 대신 원래 입력과 비교**한다.

![지도학습과 비지도학습의 Loss 기준 비교 — 지도학습은 Model의 예측을 정답(Target)과 비교해 Loss를 만들고, Autoencoder는 Model이 복원한 데이터를 원래 입력과 비교해 Loss를 만든다](/assets/img/posts/pytorch-training-5-steps/supervised-vs-unsupervised-loss.svg){: w="680" h="330" }

> 💡 즉 비지도학습도 상황에 따라 `Loss → Gradient → Optimizer → Weight 수정` 구조를
> 사용할 수 있다.
{: .prompt-info }

---

## 5. ✅ 핵심 정리

| 단계 | 코드 | 하는 일 |
| --- | --- | --- |
| ① | `zero_grad()` | 이전 Gradient 초기화 |
| ② | `model(inputs)` | 예측 |
| ③ | `criterion()` | Loss 계산 |
| ④ | `backward()` | Gradient 계산 |
| ⑤ | `optimizer.step()` | Weight 수정 |

> 💡 **한 줄 요약** · **지도학습은 정답과 예측을 비교해 Loss를 만들고, 비지도학습은 정답
> 라벨 없이 데이터의 구조나 복원 결과 등을 이용해 학습 기준을 만든다.**
{: .prompt-info }

---

## 6. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **학습 5단계** : `zero_grad → model(inputs) → criterion → backward → step`
- **`zero_grad()`** : PyTorch는 Gradient를 누적하므로 매 Batch마다 초기화
- **순전파(Forward)** : 현재 Weight로 예측값을 계산
- **Loss 계산** : 예측값과 정답을 비교 — `MSELoss`는 `차이 → 제곱 → 평균`
- **역전파(Backpropagation)** : `backward()`가 각 Weight의 Gradient를 계산
- **핵심 구분** : `backward()`는 Gradient 계산까지, Weight 수정은 `optimizer.step()`
- **Weight 갱신** : `새 Weight = 기존 Weight - Learning Rate × Gradient`
- **1 Epoch** : 이 과정을 Batch마다 반복해 전체 학습 데이터를 한 번 모두 처리한 것
- **지도학습** : 정답(Target)이 있는 데이터로 학습 — 집값 예측, 이미지 분류 등
- **비지도학습** : 정답 라벨 없이 구조·패턴을 찾음 — Clustering, PCA, Autoencoder
- **비지도학습의 Loss 기준** : 정답 대신 데이터 자체에서 만든다 (Autoencoder는 원래 입력과 비교)

</details>

---

## 7. 🔗 관련 글

- [PyTorch 코드 기본 구조](/posts/pytorch-training-script-structure/)
- [Optimizer와 Learning Rate — SGD로 Weight 수정하기](/posts/optimizer-sgd-learning-rate/)
- [지도학습과 비지도학습](/posts/supervised-vs-unsupervised-learning/)
