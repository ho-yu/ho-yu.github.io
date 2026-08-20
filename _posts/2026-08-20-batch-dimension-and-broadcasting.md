---
title: "Batch dimension과 broadcasting"
date: 2026-08-20 08:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, tensor, broadcasting, unsqueeze, squeeze]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `tensor` `broadcasting` `unsqueeze` `squeeze`
{: .prompt-info }

---

## 1. 💡 핵심 개념

**Batch dimension**은 여러 개의 데이터를 한 번에 묶어서 모델에 넣을 때, 몇 개의
샘플이 들어있는지를 나타내는 차원이다 — 데이터를 덩어리로 묶어서 한 번에
처리하는 방식이다.

> 💡 **중요** · 딥러닝에서 2차원 입력 tensor는 보통 `(batch_size, features)` 형태다.
{: .prompt-info }

아래 그림처럼 feature 4개짜리 샘플 여러 개를 쌓으면, 그 개수가 곧 batch dimension이 된다.

![feature 4개짜리 샘플 3개가 각각 shape (4,)인 상태에서 쌓여서 shape (3, 4)의 batch tensor가 되는 과정, batch dimension은 샘플 개수를 나타낸다](/assets/img/posts/batch-dimension-and-broadcasting/batch-stacking.svg){: w="440" h="200" }

---

## 2. 🔍 이해하기

### unsqueeze — 차원 추가

`unsqueeze()`의 인자는 새 차원을 삽입할 위치(index)다. 기존이 N차원 tensor라면
`unsqueeze()`의 양수 index는 0~N까지 사용할 수 있다.

```python
import torch

# feature 4개를 가진 샘플 하나입니다.
sample = torch.tensor([170.0, 65.0, 5.0, 7.0])

print("before:", sample.shape)

# 0번째 위치에 차원을 하나 추가합니다.
# (4,) -> (1, 4)
sample_batch = sample.unsqueeze(0)

print("after :", sample_batch.shape)
```

### squeeze — 차원 제거

크기가 1인 차원을 제거한다. 주로 모델에 넣기 전 shape을 맞추거나, 모델 출력
shape을 후처리에 맞출 때 사용한다.

```python
import torch

x = torch.randn(1, 4)

print("before:", x.shape)

# 크기가 1인 차원을 제거합니다.
y = x.squeeze(0)

print("after :", y.shape)
```

### Broadcasting

서로 다른 shape의 Tensor를 연산할 때, PyTorch가 가능한 경우 자동으로 크기를
맞춰주는 규칙이다. shape을 오른쪽부터 비교한다.

```text
x shape:    (2, 3, 4)
y shape:       (3, 1)

# 차원 수가 다르면 짧은 쪽 앞에 1이 있다고 생각한다.

x shape:    (2, 3, 4)
y shape:    (1, 3, 1)
```

오른쪽부터 비교하면:

| 차원 | x | y | 가능 여부 |
| --- | --- | --- | --- |
| 마지막 차원 | 4 | 1 | 가능, 1은 확장 가능 |
| 가운데 차원 | 3 | 3 | 가능, 같음 |
| 첫 번째 차원 | 2 | 1 | 가능, 1은 확장 가능 |

---

## 3. 🧪 코드 / 실습

항상 검증하는 습관을 들이자.

```python
import torch

pred = torch.randn(4, 1)
target = torch.randn(4, 1)

# 두 Tensor의 shape가 같은지 확인합니다.
# 다르면 여기서 바로 멈추고 오류를 냅니다.
assert pred.shape == target.shape, f"shape mismatch: pred={pred.shape}, target={target.shape}"

loss = ((pred - target) ** 2).mean()

print(loss)
```

---

## 4. ✅ 핵심 정리

1. batch dimension은 여러 샘플을 한 번에 처리하기 위한 차원이다
2. 표 데이터는 보통 `(batch_size, features)` 형태다
3. 이미지 데이터는 보통 `(batch_size, channels, height, width)` 형태다
4. broadcasting은 뒤쪽 차원부터 shape를 비교한다
5. `(batch_size, 1)`과 `(batch_size,)`는 broadcasting 결과가 달라질 수 있다

---

## 5. 🔗 관련 글

- [Tensor 기본 개념 - tensor 생성과 dtype/shape 확인](/posts/pytorch-tensor-basics/)
