---
title: "PyTorch shape·device 오류 디버깅 체크리스트"
date: 2026-08-20 13:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, tensor, shape, device, debugging]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `tensor` `shape` `device` `debugging`
{: .prompt-info }

---

## 1. 💡 핵심 개념

### nn.Linear 입력 차원 오류

수정 방법은 입력 데이터를 모델에 맞추거나, 모델을 데이터에 맞추는 것이다.

```python
import torch
import torch.nn as nn

model = nn.Linear(in_features=4, out_features=2)
# model = nn.Linear(in_features=5, out_features=2)

# 모델은 feature 4개를 기대합니다.
# 그런데 실제 입력은 feature가 5개입니다.
# x_wrong = torch.randn(8, 5)
x_wrong = torch.randn(8, 4)  # 특성 수를 모델의 특성 수와 일치시킨다.

try:
    output = model(x_wrong)
except RuntimeError as e:
    print("오류 발생!")
    print(e)
```

입력을 바꿀지, 모델을 바꿀지는 문제 상황에 따라 다르다. 데이터의 특성 수가 원래
5개가 맞다면 모델을 바꾸고, 모델이 특성 4개만 쓰도록 설계됐다면 데이터 전처리에서
특성 수를 맞춰야 한다.

### batch 차원 누락

데이터 1개를 모델에 넣을 때, `unsqueeze(0)`로 batch 차원을 명시적으로 추가하는
것이 더 안전하다. 기존 데이터의 값이나 구조를 건드리지 않고 원하는 위치에 크기
1짜리 차원만 추가하기 때문이다.

> ⚠️ **주의** · `reshape()`을 잘못 사용하면, 데이터의 의미가 전혀 다른 shape으로
> 바뀔 수도 있다.
{: .prompt-warning }

### device mismatch

device 오류는 아래 3가지 값을 비교하면 된다.

```python
print(next(model.parameters()).device)
print(x.device)
print(y.device)
```

---

## 2. ✅ 핵심 정리

- **Tensor 점검 3요소** : shape · dtype · device
- **batch dimension** : 여러 샘플을 한 번에 처리하기 위한 차원
- **broadcasting 주의** : 의도치 않은 shape 확장 가능
- **GPU 사용** : 모델과 Tensor를 같은 device로 이동
- **오류 발생 시** : 먼저 shape·dtype·device를 출력

---

## 3. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>tensor 디버깅 체크리스트 — 펼쳐서 확인</strong></summary>

1. `print(x.shape)`를 찍었나?
2. `print(x.dtype)`을 찍었나?
3. `print(x.device)`를 찍었나?
4. 모델의 입력 차원과 Tensor의 마지막 차원이 같은가?
5. 예측값과 정답값의 shape가 의도대로 맞나?
6. 분류 target이 class index라면 dtype이 `torch.long`인가?
7. 모델, 입력, 정답이 같은 device에 있나?
8. broadcasting 때문에 결과 shape가 커지지 않았나?

</details>

---

## 4. 🔗 관련 글

- [Tensor 기본 개념 - tensor 생성과 dtype/shape 확인](/posts/pytorch-tensor-basics/)
- [Batch dimension과 broadcasting](/posts/batch-dimension-and-broadcasting/)
- [CPU/GPU device와 .to(device)](/posts/pytorch-device-cpu-gpu/)
