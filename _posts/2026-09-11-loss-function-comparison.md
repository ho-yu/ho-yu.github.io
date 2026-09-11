---
title: "MSE·BCE·CrossEntropy — 문제 유형별 Loss 고르기"
date: 2026-09-11 09:03:00 +0900
categories: [Notes, Deep Learning]
tags: [loss-function, mse-loss, bce-with-logits-loss, cross-entropy-loss, reduction]
---

> 🗂️ **Notes · Deep Learning** — `loss-function` `mse-loss` `bce-with-logits-loss` `cross-entropy-loss` `reduction`
{: .prompt-info }

---

## 1. 📖 문제 유형별로 Loss가 갈린다

가장 먼저 문제 유형에 따라 손실함수를 구분합니다.

![회귀는 정답이 실수값이라 MSE, 이진 분류는 정답이 0 또는 1이라 BCE, 다중 클래스 분류는 정답이 class index라 CrossEntropy로 이어지는 선택 흐름](/assets/img/posts/loss-function-comparison/loss-selection.svg){: w="720" h="256" }

각각의 자세한 내용은 [Loss Function과 Epoch 이해하기](/posts/loss-function-and-epoch/)부터
이어지는 개별 글에 있고, 이 글은 셋을 한자리에서 비교하는 복습 정리입니다.

---

## 2. 📉 MSE — 회귀

MSE는 주로 **회귀 문제**에서 사용합니다.

```text
예측값 - 정답
↓
제곱
↓
평균
```

```text
MSE = 평균((예측 - 정답)²)
```

### 오차를 제곱하는 이유

1. 양수 오차와 음수 오차가 서로 상쇄되는 것을 막기 위해
2. 큰 오차에 더 큰 패널티를 주기 위해

| 오차 | 제곱 |
| --- | --- |
| 1 | 1 |
| 3 | 9 |

즉 큰 오차가 더 강하게 반영됩니다. → [MSELoss 이해하기 — 차이, 제곱, 평균](/posts/mse-loss/)

---

## 3. 🔵 BCE — 이진 분류와 `log(0)` 문제

BCE는 **이진 분류(Binary Classification)** 에 사용합니다. 정답은 보통 `0 또는 1`입니다.

```text
스팸 아님 → 0
스팸      → 1
```

> ⚠️ BCE에서는 확률에 `log()`를 적용하기 때문에 `log(0)` 문제가 발생할 수 있습니다.
{: .prompt-warning }

### `clip`으로 범위를 제한한다

`clip`은 값을 **지정한 범위 안으로 강제로 제한하는 기능**입니다.

![np.clip(x, 0, 1)에서 -0.5는 0으로, 0.3은 그대로, 1.7은 1로 밀려 들어가는 수직선 그림과 BCE에서는 epsilon부터 1-epsilon 범위를 쓴다는 설명](/assets/img/posts/loss-function-comparison/clip.svg){: w="720" h="250" }

BCE에서는 주로 `[epsilon, 1 - epsilon]` 범위로 확률을 제한합니다.

```python
p = np.clip(p, epsilon, 1 - epsilon)
```

이렇게 하면 정확한 `0`이나 `1`을 피해서 `log(0)` 문제를 방지할 수 있습니다. 또는 실무에서는
`BCEWithLogitsLoss`처럼 **logits를 직접 받는 안정적인 전용 함수**를 사용하기도 합니다.
→ [BCEWithLogitsLoss와 Logit 이해하기](/posts/bce-with-logits-loss/)

---

## 4. 🎯 CrossEntropy — 다중 클래스 분류

CrossEntropy는 주로 **여러 클래스 중 하나를 선택하는 다중 클래스 분류**에 사용합니다.

```text
0 → 고양이
1 → 강아지
2 → 새
```

정답이 강아지라면 `정답 class index = 1`입니다. 즉 정답을 보통 확률 벡터가 아니라 **클래스 번호
하나**로 표현합니다.

### shape

| 이름 | shape | 의미 |
| --- | --- | --- |
| logits | `[B, C]` | `B` = Batch size(샘플 개수), `C` = Class 개수 |
| target | `[B]` | 샘플마다 정답 클래스 번호 하나 |

`logits shape = [4, 3]`이면 4개 샘플, 각 샘플마다 3개 클래스 점수라는 뜻이고, 정답은 다음처럼
샘플 수만큼만 있으면 됩니다.

```python
target = [0, 2, 1, 0]
```

### 정답 확률과 loss의 관계

CrossEntropy의 핵심 관계는 다음과 같습니다.

```text
loss = -log(정답 클래스 확률)
```

![정답 클래스 확률이 0.1일 때 loss가 약 2.30, 0.9일 때 약 0.11로 떨어지는 -log(p) 곡선](/assets/img/posts/loss-function-comparison/neg-log-probability.svg){: w="720" h="280" }

```text
정답 확률 ↑
↓
CrossEntropy loss ↓
```

모델이 정답을 높은 확률로 예측할수록 손실이 작아집니다.
→ [CrossEntropyLoss 이해하기 — 다중 클래스 분류](/posts/cross-entropy-loss/)

---

## 5. 🧮 `reduction` — 여러 loss를 어떻게 정리할까

`reduction`은 **여러 샘플에서 나온 loss를 마지막에 어떻게 정리할지 결정하는 옵션**입니다.
`loss = [0.2, 0.5, 0.3]`이라면 다음과 같습니다.

| 설정 | 계산 | 결과 |
| --- | --- | --- |
| `"none"` | 샘플별 loss를 그대로 반환 | `[0.2, 0.5, 0.3]` |
| `"mean"` | `(0.2 + 0.5 + 0.3) / 3` | `0.333...` |
| `"sum"` | `0.2 + 0.5 + 0.3` | `1.0` |

> 💡 **한 줄 정리** · `none` → 개별 loss 유지 / `mean` → 평균 / `sum` → 합계
{: .prompt-info }

→ [Loss의 reduction — mean, sum, none](/posts/loss-reduction-mean-sum-none/)

---

## 6. ✅ 핵심 정리

| Loss | 문제 유형 | 정답의 형태 | 기억할 점 |
| --- | --- | --- | --- |
| **MSE** | 회귀 | 실수값 | 예측 − 정답 → 제곱 → 평균 · 오차 상쇄 방지 + 큰 오차 강조 |
| **BCE** | 이진 분류 | 0 또는 1 | `log(0)` 방지를 위해 `clip` 또는 logits 기반 함수 사용 |
| **CrossEntropy** | 다중 클래스 | class index | logits `[B, C]` / target `[B]` · `loss = -log(정답 확률)` |

```text
정답 클래스 확률 ↑
→ CrossEntropy loss ↓

clip
= 값을 특정 범위 안으로 제한

reduction
= 여러 loss를 마지막에 어떻게 정리할지 결정
```

---

## 7. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **선택 기준** : 회귀 → MSE / 이진 분류 → BCE / 다중 클래스 → CrossEntropy
- **MSE 계산** : 예측 − 정답 → 제곱 → 평균
- **제곱하는 이유 ①** : 양수 오차와 음수 오차가 서로 상쇄되는 것을 막기 위해
- **제곱하는 이유 ②** : 큰 오차에 더 큰 패널티 — 오차 1은 1, 오차 3은 9
- **BCE의 정답** : `0` 또는 `1` (스팸 아님 → 0, 스팸 → 1)
- **BCE의 위험** : 확률에 `log()`를 적용하므로 `log(0)` 문제가 생길 수 있다
- **`clip`** : 값을 지정한 범위 안으로 강제 제한 — `np.clip(x, 0, 1)`에서 `-0.5 → 0`, `1.7 → 1`
- **BCE에서의 clip** : `np.clip(p, epsilon, 1 - epsilon)` — 정확한 0과 1을 피한다
- **실무 대안** : logits를 직접 받는 `BCEWithLogitsLoss`
- **CrossEntropy의 정답** : 확률 벡터가 아니라 **클래스 번호 하나** (class index)
- **shape** : logits `[B, C]`, target `[B]` — `[4, 3]`이면 샘플 4개 × 클래스 3개
- **핵심 관계** : `loss = -log(정답 클래스 확률)` — 정답 확률 0.9면 약 0.11, 0.1이면 약 2.30
- **`reduction`** : `none` 개별 유지 / `mean` 평균 / `sum` 합계

</details>

---

## 8. 🔗 관련 글

- [MSELoss 이해하기 — 차이, 제곱, 평균](/posts/mse-loss/)
- [BCEWithLogitsLoss와 Logit 이해하기](/posts/bce-with-logits-loss/)
- [CrossEntropyLoss 이해하기 — 다중 클래스 분류](/posts/cross-entropy-loss/)
