---
title: "난수 생성기와 Seed — 왜 Seed를 여러 개 설정할까"
date: 2026-08-26 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, numpy, seed, reproducibility, random]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `numpy` `seed` `reproducibility` `random`
{: .prompt-info }

---

## 1. ❓ 왜 Seed를 여러 개 설정할까?

Python 언어는 하나지만, `random`, NumPy, PyTorch는 각각 **자기만의 난수 생성기와 난수
상태를 따로 관리**한다.

![Python 프로그램 안에서 random, NumPy, PyTorch가 각각 별도의 난수 생성기를 가지고 random.seed(123), np.random.seed(123), torch.manual_seed(123)으로 따로 고정되며, 같은 123을 써도 만들어지는 숫자는 서로 다를 수 있고 같은 라이브러리에서 같은 Seed를 다시 설정하면 같은 결과를 재현할 수 있다](/assets/img/posts/random-seed/separate-rngs.svg){: w="700" h="310" }

따라서 하나의 Seed만 고정한다고 다른 라이브러리의 랜덤값까지 자동으로 고정되지는 않는다.

```python
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
```

이렇게 각각 설정하는 이유가 여기에 있다.

---

## 2. 💡 Seed란?

Seed는 **난수 생성기의 시작 상태를 고정하는 값**이다.

```python
torch.manual_seed(123)
print(torch.randn(3))

torch.manual_seed(123)
print(torch.randn(3))
```

같은 Seed로 다시 시작했기 때문에 같은 랜덤값이 나온다.

```text
seed = 123 → 같은 시작 상태 → 같은 난수 순서
```

---

## 3. ⚠️ 같은 Seed면 모든 라이브러리가 같은 숫자를 만들까?

아니다.

```python
random.seed(123)
np.random.seed(123)
torch.manual_seed(123)
```

모두 `123`을 사용해도 각 라이브러리는 난수 생성 방식과 상태를 따로 관리하므로 **생성되는
숫자 자체는 서로 다를 수 있다.**

> 💡 중요한 것은 **같은 라이브러리에서 같은 Seed를 다시 설정하면 같은 랜덤 결과를 재현할 수
> 있다**는 점이다.
{: .prompt-info }

---

## 4. 🔍 딥러닝에서 왜 중요한가?

딥러닝에서는 랜덤 요소가 많이 사용된다.

- 모델 Weight 초기화
- 데이터 Shuffle
- 랜덤 Tensor 생성
- Train / Validation 분할

Seed를 고정하면 실험을 다시 실행했을 때 결과가 크게 달라지는 것을 줄일 수 있다. 즉 **실험
재현성(Reproducibility)**을 높이기 위해 사용한다.

---

## 5. ✅ 핵심 정리

| 항목 | 의미 |
| --- | --- |
| `random` / NumPy / PyTorch | 각각 난수 상태를 따로 관리 |
| Seed | 난수 생성기의 시작 상태 고정 |
| 여러 Seed 설정 | 사용하는 라이브러리들의 랜덤 결과를 각각 고정 |
| 목적 | 실험 결과를 최대한 재현 |

> 💡 **한 줄 요약** · **지금 단계에서는 "라이브러리마다 난수 생성기를 따로 관리하므로,
> 재현성을 위해 각각 Seed를 고정한다" 정도로 이해하면 충분하다.**
{: .prompt-info }

---

## 6. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **왜 여러 개** : `random` / NumPy / PyTorch가 각각 자기만의 난수 생성기와 상태를 관리
- **Seed** : 난수 생성기의 시작 상태를 고정하는 값
- **설정 방법** : `random.seed()` / `np.random.seed()` / `torch.manual_seed()`
- **같은 Seed, 다른 라이브러리** : 생성되는 숫자 자체는 서로 다를 수 있다
- **재현되는 것** : 같은 라이브러리에서 같은 Seed를 다시 설정했을 때의 결과
- **딥러닝의 랜덤 요소** : Weight 초기화, 데이터 Shuffle, 랜덤 Tensor 생성, Train/Validation 분할
- **목적** : 실험 재현성(Reproducibility)

</details>

---

## 7. 🔗 관련 글

- [PyTorch 코드 기본 구조](/posts/pytorch-training-script-structure/)
- [데이터 분리와 평가지표 — train/valid/test](/posts/train-valid-test-split-and-metrics/)
- [MLP의 입력층/은닉층/출력층](/posts/mlp-input-hidden-output-layers/)
