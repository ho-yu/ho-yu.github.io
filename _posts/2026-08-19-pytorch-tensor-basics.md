---
title: "Tensor 기본 개념 - tensor 생성과 dtype/shape 확인"
date: 2026-08-19 11:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, tensor, vector, matrix, dtype]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `tensor` `vector` `matrix` `dtype`
{: .prompt-info }

---

## 1. 📖 개요

> 📌 **학습 목표**
> - `torch.tensor`, `torch.zeros`, `torch.ones`, `torch.randn`으로 Tensor를 만들 수 있다.
> - `shape`, `ndim`, `dtype`, `device`를 확인할 수 있다.
> - `shape`를 보고 데이터가 어떤 구조인지 설명할 수 있다.
> - dtype이 왜 모델 학습에서 중요한지 설명할 수 있다.
{: .prompt-tip }

---

## 2. 💡 핵심 개념

PyTorch에서 숫자 데이터를 담는 기본 그릇이 **Tensor**다.

딥러닝에서 tensor를 볼 때는 값 자체보다 먼저 `shape`, `dtype`, `device`를 확인해야
한다. Tensor의 값 자체보다 이 세 가지가 연산 가능 여부를 먼저 결정하기 때문이다.

> 💡 **한 줄 정리** · `shape`는 구조, `dtype`은 숫자 종류, `device`는 계산 위치이며,
> 이 3개가 맞아야 Tensor의 실제 값으로 계산을 시작할 수 있다.
{: .prompt-info }

---

## 3. 🧪 코드 / 실습

아래 그림처럼 Tensor는 0차원(scalar)에서 시작해 차원이 하나씩 늘어난다. 값 하나 →
값이 한 줄로 늘어선 vector → 행/열을 가진 matrix → matrix가 여러 개 쌓인 3차원
tensor 순이며, `shape`의 원소 개수가 곧 차원(ndim) 수다.

![Tensor가 scalar(0차원)에서 vector(1차원), matrix(2차원), 3차원 tensor로 차원이 하나씩 늘어나는 과정과 각 단계의 shape](/assets/img/posts/pytorch-tensor-basics/tensor-dimensions.svg){: w="960" h="300" }

### 0차원 Tensor: Scalar

```python
import torch

# 숫자 하나를 Tensor로 만듭니다.
# 이런 Tensor를 scalar라고 부릅니다.
scalar = torch.tensor(7)

print(scalar)
print(scalar.shape)
print(scalar.ndim)
```

### 1차원 Tensor: Vector

```python
# 숫자 3개가 한 줄로 들어 있는 Tensor입니다.
# 벡터(vector)라고 생각하면 됩니다.
vector = torch.tensor([1, 2, 3])

print(vector)
print(vector.shape)
print(vector.ndim)
```

### 2차원 Tensor: Matrix

```python
# 2행 3열짜리 Tensor입니다.
# 엑셀 표처럼 생각하면 이해하기 쉽습니다.
matrix = torch.tensor([
    [1, 2, 3],
    [4, 5, 6]
])

print(matrix)
print(matrix.shape)
print(matrix.ndim)
```

### 3차원 Tensor: 여러 개의 행렬 묶음

```python
# 2개의 행렬이 들어 있는 3차원 Tensor입니다.
tensor_3d = torch.tensor([
    [
        [1, 2, 3],
        [4, 5, 6]
    ],
    [
        [7, 8, 9],
        [10, 11, 12]
    ]
])

print(tensor_3d)
print(tensor_3d.shape)
print(tensor_3d.ndim)
```

### Tensor 속성 확인하기

```python
import torch

# 3행 4열짜리 무작위 Tensor를 만듭니다.
# torch.randn은 표준정규분포에서 무작위 값을 뽑습니다.
x = torch.randn(3, 4)

# shape: Tensor의 모양입니다.
print("shape:", x.shape)   # torch.Size([3, 4])

# ndim: Tensor가 몇 차원인지 알려줍니다.
print("ndim:", x.ndim)     # 2

# dtype: Tensor 안에 들어 있는 값의 자료형입니다.
print("dtype:", x.dtype)   # torch.float32 (dtype을 지정하지 않으면 기본값)

# device: Tensor가 CPU에 있는지 GPU에 있는지 알려줍니다.
print("device:", x.device) # cpu (device를 지정하지 않으면 기본값)
```

---

## 4. ✅ 핵심 정리

- **Tensor** : PyTorch에서 숫자 데이터를 담는 기본 자료구조
- **shape / dtype / device** : Tensor의 값보다 먼저 확인해야 하는 3가지 — 연산 가능 여부를 결정한다
- **차원** : 0차원(scalar) → 1차원(vector) → 2차원(matrix) → 3차원(행렬 여러 개의 묶음) 순으로 확장된다

---

## 5. 🔗 관련 글

- [벡터 기초 — 정의부터 정규화까지](/posts/vector-basics/)
