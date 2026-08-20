---
title: "CPU/GPU device와 .to(device)"
date: 2026-08-20 12:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, tensor, device, cuda, training-loop]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `tensor` `device` `cuda` `training-loop`
{: .prompt-info }

---

## 1. 💡 핵심 개념

**device**는 Tensor가 어디에 저장되어 있는지를 나타낸다.

| device | 의미 |
| --- | --- |
| `cpu` | CPU 메모리에 Tensor가 있음 |
| `cuda` 또는 `cuda:0` | NVIDIA GPU 메모리에 Tensor가 있음 |

PyTorch Tensor는 기본적으로 CPU에 생성된다. GPU에서 연산하려면 Tensor를 명시적으로
이동해야 한다.

```python
import torch

x = torch.randn(2, 3)

print(x.device)
```

---

## 2. 🧪 코드 / 실습

### Tensor 이동하기

Tensor는 `.to(device)`로 이동한다.

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

x = torch.randn(2, 3)

print("before:", x.device)

# x를 device로 이동합니다.
# Tensor의 .to()는 이동된 Tensor를 반환하므로,
# 반환값을 다시 x에 저장해야 합니다.
x = x.to(device)

print("after :", x.device)
```

### 모델도 같은 device로 이동하기

```python
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(device)

model = nn.Linear(4, 2)

print(model)
# print(model.device)

print(next(model.parameters()).device)
# nn.Linear 모델 객체 자체에는 .device 속성이 없음.
# 모델 안의 파라미터가 어느 device에 올라가 있는지 확인해야 함.
# => next(model.parameters()).device
# 쉽게 표현하면:
# model -> parameters() => next() -> .device
# weight, bias 목록 -> 첫 번째 weight 선택 -> cpu인지 gpu인지 확인

model = model.to(device)

x = torch.randn(8, 4).to(device)

output = model(x)

print(output.shape)
print(output.device)
```

### 학습 루프에서 device 처리 패턴

모델, 입력, 정답을 같은 device에 두는 위치를 확인하는 것이 핵심이다.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model은 학습 시작 전에 한 번 device로 이동합니다.
model = model.to(device)

for inputs, labels in dataloader:
    # 입력과 정답을 모두 같은 device로 이동합니다.
    inputs = inputs.to(device)
    labels = labels.to(device)

    outputs = model(inputs)
    loss = criterion(outputs, labels)
```

### 새 tensor를 만들 때 device 맞추기

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 특성 3개를 가진 데이터 4개를 랜덤으로 만들고, 지정한 device에 올리는 코드.
x = torch.randn(4, 3).to(device)

# 새 Tensor를 만들 때 x와 같은 device에 만들고 싶다면 device=x.device를 사용합니다.
bias = torch.zeros(3, device=x.device)

result = x + bias

print(x.device)
print(bias.device)
print(result.device)
```

```python
x = torch.randn(4, 3).to(device)

# x와 같은 shape, dtype, device를 가진 0 Tensor를 만듭니다.
z = torch.zeros_like(x)
```

---

## 3. ✅ 핵심 정리

- **Tensor 기본 위치** : CPU
- **GPU 가능 여부 확인** : `torch.cuda.is_available()`
- **Tensor 이동** : `.to(device)`
- **모델 이동** : `.to(device)` (내부 파라미터가 실제로 이동)
- **학습 루프** : `model` · `inputs` · `labels`가 모두 같은 device에 있어야 함

---

## 4. 🔗 관련 글

- [Tensor 기본 개념 - tensor 생성과 dtype/shape 확인](/posts/pytorch-tensor-basics/)
- [PyTorch shape·device 오류 디버깅 체크리스트](/posts/pytorch-shape-device-debugging/)
- [PyTorch 코드 기본 구조](/posts/pytorch-training-script-structure/)
