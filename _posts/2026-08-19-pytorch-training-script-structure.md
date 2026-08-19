---
title: "PyTorch 코드 기본 구조"
date: 2026-08-19 13:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, neural-network, training-loop, dataloader, checkpoint]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `neural-network` `training-loop` `dataloader` `checkpoint`
{: .prompt-info }

---

## 1. 💡 핵심 개념

PyTorch 학습 스크립트는 보통 아래 10단계로 구성된다.

```text
1. import
2. config / hyperparameter
3. dataset / dataloader
4. model
5. loss function
6. optimizer
7. train loop
8. validation loop
9. metric
10. checkpoint / logging
```

---

## 2. 🧪 코드 / 실습

### 전체 코드 예시

```python
# 1. import
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split


# 2. config / hyperparameter
SEED = 42
BATCH_SIZE = 32
LR = 0.05
EPOCHS = 5

torch.manual_seed(SEED)


# 3. data
X = torch.randn(200, 4)
true_w = torch.tensor([[2.0], [-1.0], [0.5], [3.0]])
y = X @ true_w + 0.1 * torch.randn(200, 1)

dataset = TensorDataset(X, y)
train_dataset, valid_dataset = random_split(dataset, [160, 40])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=False)


# 4. device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 5. model
model = nn.Sequential(
    nn.Linear(4, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
).to(device)


# 6. loss / optimizer
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=LR)


# 7. train function
def train_one_epoch(model, dataloader, loss_fn, optimizer, device):
    model.train()
    total_loss = 0.0

    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()
        preds = model(batch_x)
        loss = loss_fn(preds, batch_y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * batch_x.size(0)

    return total_loss / len(dataloader.dataset)


# 8. validation function
@torch.no_grad()
def validate(model, dataloader, loss_fn, device):
    model.eval()
    total_loss = 0.0

    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        preds = model(batch_x)
        loss = loss_fn(preds, batch_y)

        total_loss += loss.item() * batch_x.size(0)

    return total_loss / len(dataloader.dataset)


# 9. epoch loop / logging
history = []

for epoch in range(1, EPOCHS + 1):
    train_loss = train_one_epoch(model, train_loader, loss_fn, optimizer, device)
    valid_loss = validate(model, valid_loader, loss_fn, device)

    log = {
        "epoch": epoch,
        "train_loss": train_loss,
        "valid_loss": valid_loss,
    }
    history.append(log)

    print(
        f"Epoch {epoch} | "
        f"train_loss={train_loss:.4f} | "
        f"valid_loss={valid_loss:.4f}"
    )


# 10. checkpoint
torch.save(model.state_dict(), "basic_mlp_regression.pt")
```

---

## 3. 🔍 이해하기

### 반드시 이해하고 작성해야 하는 코드

```python
model = nn.Sequential(
    nn.Linear(4, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
```

```python
for batch_x, batch_y in dataloader:
    optimizer.zero_grad()
    preds = model(batch_x)
    loss = loss_fn(preds, batch_y)
    loss.backward()
    optimizer.step()
```

```text
데이터를 batch 단위로 가져옴
  ↓
기울기 초기화 (이전 batch에서 계산된 gradient를 초기화)
  ↓
모델이 예측
  ↓
오차 계산 (예측과 정답의 차이)
  ↓
Gradient 계산 (Loss를 기준으로 각 Weight의 gradient를 계산)
  ↓
Weight 수정 (gradient를 이용해서 Weight를 실제로 수정)
```

### 구성 요소별 역할

```text
model     -> 신경망 정의
loss_fn   -> 틀린 정도 계산
optimizer -> weight 수정
train     -> 실제 학습
validate  -> 성능 확인
```

---

## 4. ✅ 핵심 정리

- **PyTorch 학습 스크립트** : import → config → data → model → loss/optimizer →
  train → validate → epoch 반복 → 로깅 → checkpoint의 10단계로 구성된다
- **한 batch 학습** : `zero_grad → 예측 → loss 계산 → backward → step` 순서로 진행된다
- **구성 요소** : `model`은 신경망 정의, `loss_fn`은 틀린 정도 계산,
  `optimizer`는 weight 수정을 담당한다

---

## 5. 🔗 관련 글

- [머신러닝과 딥러닝의 차이, 딥러닝의 기본 개념](/posts/machine-learning-vs-deep-learning-basics/)
- [딥러닝 문제 유형과 입출력 구조 설계](/posts/deep-learning-problem-types-and-io-shapes/)
