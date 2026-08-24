---
title: "Loss의 reduction — mean, sum, none"
date: 2026-08-24 12:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, loss-function, reduction, mse-loss, batch]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `loss-function` `reduction` `mse-loss` `batch`
{: .prompt-info }

---

## 1. 💡 `reduction`이란?

`reduction`은 **여러 데이터에서 계산된 개별 Loss를 최종적으로 어떻게 처리할지 결정하는
옵션**이다.

예를 들어 Batch에 데이터 3개가 있고 각각의 Loss가:

```text
[4, 1, 9]
```

라고 하자.

Reduction 설정에 따라 최종 결과가 달라진다. 아래 그림처럼 같은 개별 Loss에서 세 가지
다른 결과가 나온다.

![개별 Loss [4, 1, 9]가 reduction 설정에 따라 mean이면 4.67, sum이면 14, none이면 [4, 1, 9] 그대로가 되는 비교](/assets/img/posts/loss-reduction-mean-sum-none/reduction-mean-sum-none.svg){: w="600" h="290" }

---

## 2. 📖 `mean`

```python
nn.MSELoss(reduction="mean")
```

모든 Loss의 **평균**을 계산한다.

```text
[4, 1, 9]

↓ 평균

(4 + 1 + 9) / 3

= 4.67
```

일반적인 딥러닝 학습에서 가장 많이 사용한다.

이유는 Batch Size가 바뀌어도 Loss 크기를 비교하기 쉽기 때문이다.

```text
Batch 32개  → 평균 Loss 2.1
Batch 128개 → 평균 Loss 2.0
```

> 💡 특별한 목적이 없다면 보통 `mean`을 사용한다.
{: .prompt-info }

---

## 3. 📖 `sum`

```python
nn.MSELoss(reduction="sum")
```

모든 Loss를 **합산**한다.

```text
[4, 1, 9]

↓ 합계

4 + 1 + 9

= 14
```

전체 오차량 자체가 중요한 경우 사용할 수 있다.

> ⚠️ 다만 Batch Size가 커지면 데이터 개수가 많다는 이유로 Loss도 커진다.
>
> ```text
> 데이터 10개
> → Loss 합계가 상대적으로 작음
>
> 데이터 100개
> → Loss 합계가 상대적으로 커짐
> ```
>
> 따라서 일반적인 모델 학습에서는 `mean`보다 덜 사용한다.
{: .prompt-warning }

---

## 4. 📖 `none`

```python
nn.MSELoss(reduction="none")
```

Loss를 합치지 않고 **개별 Loss를 그대로 유지**한다.

```text
[4, 1, 9]
```

다음과 같은 상황에서 유용하다.

- 어떤 데이터에서 모델이 크게 틀렸는지 확인
- 데이터마다 다른 가중치 적용
- Custom Loss 구현

예:

```python
loss_fn = nn.MSELoss(reduction="none")

losses = loss_fn(preds, y)

weighted_loss = losses * weights
loss = weighted_loss.mean()
```

즉 개별 Loss를 직접 조작한 뒤 최종적으로 평균이나 합계를 계산할 수 있다.

---

## 5. ✅ 선택 기준

| Reduction | 의미         | 주 사용 상황                 |
| --------- | ---------- | ----------------------- |
| `mean`    | Loss 평균    | 일반적인 모델 학습              |
| `sum`     | Loss 총합    | 전체 오차량이 중요할 때           |
| `none`    | 개별 Loss 유지 | 분석, 가중치 적용, Custom Loss |

PyTorch의 많은 손실 함수는 기본적으로:

```python
reduction="mean"
```

을 사용한다.

> 💡 **한 줄 요약** · `reduction`은 **여러 개의 개별 Loss를 평균낼지(`mean`), 모두
> 더할지(`sum`), 그대로 유지할지(`none`) 결정하는 옵션**이다.
{: .prompt-info }

---

## 6. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **reduction** : 개별 Loss를 최종적으로 어떻게 처리할지 결정하는 옵션
- **`mean`** : 평균 → `[4, 1, 9]` = 4.67, 일반적인 학습에서 가장 많이 사용
- **`mean`을 쓰는 이유** : Batch Size가 바뀌어도 Loss 크기를 비교하기 쉬움
- **`sum`** : 합계 → `[4, 1, 9]` = 14, 전체 오차량이 중요할 때
- **`sum`의 주의점** : 데이터 개수가 많다는 이유만으로 Loss가 커진다
- **`none`** : 개별 Loss 유지 → 분석, 데이터별 가중치, Custom Loss
- **기본값** : PyTorch의 많은 손실 함수는 `reduction="mean"`

</details>

---

## 7. 🔗 관련 글

- [Loss Function과 Epoch 이해하기](/posts/loss-function-and-epoch/)
- [MSELoss 이해하기 — 차이, 제곱, 평균](/posts/mse-loss/)
