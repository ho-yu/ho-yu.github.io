---
title: "위험한 Broadcasting — 에러 없이 틀리는 Shape 불일치"
date: 2026-08-27 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, broadcasting, tensor-shape, view, mse-loss]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `broadcasting` `tensor-shape` `view` `mse-loss`
{: .prompt-info }

---

## 1. 💡 위험한 Broadcasting이란?

Broadcasting은 **서로 다른 Shape의 Tensor를 연산할 때 PyTorch가 자동으로 크기를 맞춰주는
기능**이다.

> ⚠️ 편리하지만, Shape이 의도와 다르면 **에러 없이 잘못된 계산이 진행될 수 있다.**
{: .prompt-warning }

---

## 2. 🧪 예시

```python
pred = torch.randn(4, 1)
target = torch.randn(4)
```

Shape은 다음과 같다.

```text
pred.shape   = [4, 1]
target.shape = [4]
```

사람 눈에는 둘 다 데이터가 4개라서 맞아 보이지만, Tensor 구조는 다르다.

| Tensor | 차원 | Shape |
| --- | --- | --- |
| `pred` | 2차원 | `[4, 1]` |
| `target` | 1차원 | `[4]` |

---

## 3. ⚠️ 왜 위험할까?

예를 들어 `pred - target`을 계산하면 Broadcasting이 발생할 수 있다. PyTorch는 `target`을
계산 가능하도록 확장해서 결과적으로 `[4, 4]` 형태의 계산이 만들어질 수 있다.

우리가 원한 것과 실제로 일어나는 일을 나란히 보면 아래 그림과 같다.

![의도한 계산과 Broadcasting이 만든 계산의 비교 — pred [4, 1]과 target [4, 1]이면 pred1↔target1처럼 샘플끼리 1:1로 4쌍을 비교하지만, target이 [4]이면 각 예측값이 target 4개 모두와 계산되어 4×4 = 16칸의 결과 [4, 4]가 만들어진다](/assets/img/posts/dangerous-broadcasting/intended-vs-broadcast.svg){: w="700" h="372" }

우리가 원한 것은 다음처럼 **샘플끼리 1:1 비교**하는 것이다.

```text
pred1 ↔ target1
pred2 ↔ target2
pred3 ↔ target3
pred4 ↔ target4
```

하지만 Broadcasting이 발생하면 각 예측값이 여러 Target과 계산될 수 있다.

---

## 4. 🔧 해결 방법

Target의 Shape을 예측값과 맞춘다.

```python
fixed_target = target.view(4, 1)
```

Shape 변화는 다음과 같다.

```text
target
[4]

 ↓ view(4, 1)

fixed_target
[4, 1]
```

이제 `pred`와 `fixed_target`이 둘 다 `[4, 1]`로 Shape이 같아진다. 따라서 의도한 1:1 계산이
가능하다.

---

## 5. 📖 Loss 계산에서 특히 중요

예를 들어 `MSELoss`를 사용할 때:

```python
loss = nn.MSELoss()(pred, fixed_target)
```

처럼 **Prediction과 Target의 Shape을 맞춰주는 것이 중요하다.**

| `pred` | `target` | 결과 |
| --- | --- | --- |
| `[4, 1]` | `[4]` | ⚠️ Broadcasting 위험 |
| `[4, 1]` | `[4, 1]` | ✅ 의도한 계산 |

---

## 6. ✅ 핵심 정리

> 💡 **한 줄 요약** · **위험한 Broadcasting은 Shape이 다른 Tensor가 자동 확장되면서 에러
> 없이 의도하지 않은 계산이 발생하는 경우이다.**
{: .prompt-info }

따라서 Loss 계산 전에는 항상 다음처럼 **Prediction과 Target의 Shape을 확인하는 습관**이
중요하다.

```python
print(pred.shape)
print(target.shape)
```

---

## 7. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **Broadcasting** : Shape이 다른 Tensor를 연산할 때 PyTorch가 자동으로 크기를 맞춰주는 기능
- **위험한 이유** : Shape이 의도와 달라도 **에러 없이** 잘못된 계산이 진행된다
- **대표 사례** : `pred [4, 1]`와 `target [4]` — 사람 눈엔 둘 다 4개지만 차원이 다르다
- **일어나는 일** : `target`이 확장되어 결과가 `[4, 4]` 형태가 될 수 있다
- **의도했던 것** : `pred1 ↔ target1`처럼 샘플끼리 1:1 비교
- **해결** : `target.view(4, 1)`로 Shape을 예측값과 맞춘다
- **Loss에서 특히** : `pred`와 `target`의 Shape이 같아야 의도한 계산이 된다
- **습관** : Loss 계산 전에 `print(pred.shape)` / `print(target.shape)`

</details>

---

## 8. 🔗 관련 글

- [Batch dimension과 broadcasting](/posts/batch-dimension-and-broadcasting/)
- [PyTorch shape·device 오류 디버깅 체크리스트](/posts/pytorch-shape-device-debugging/)
- [MSELoss 이해하기 — 차이, 제곱, 평균](/posts/mse-loss/)
