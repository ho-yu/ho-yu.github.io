---
title: "PyTorch reshape() 이해하기"
date: 2026-08-29 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, reshape, view, tensor-shape, flatten]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `reshape` `view` `tensor-shape` `flatten`
{: .prompt-info }

---

## 1. 💡 `reshape()`란?

`reshape()`는 Tensor의 **값은 그대로 두고 Shape만 변경하는 함수**이다.

```python
import torch

x = torch.arange(12)

print(x.shape)
# torch.Size([12])

y = x.reshape(3, 4)

print(y.shape)
# torch.Size([3, 4])
```

변화:

```text
[12]
 ↓ reshape(3, 4)
[3, 4]
```

> 💡 **중요** · `reshape()`는 데이터 타입을 바꾸는 형변환이 아니라 **Tensor의 모양을 바꾸는
> Shape 변환**이다.
{: .prompt-info }

---

## 2. 📐 원소 개수는 반드시 같아야 한다

원래 Tensor가 `[12]`라면 총 원소는 12개이다.

따라서:

```python
x.reshape(3, 4)   # 3 × 4 = 12 → 가능
x.reshape(2, 6)   # 2 × 6 = 12 → 가능
x.reshape(4, 3)   # 4 × 3 = 12 → 가능
```

하지만:

```python
x.reshape(5, 3)   # 5 × 3 = 15 → 불가능
```

> 📌 **핵심**
>
> ```text
> reshape 전 원소 개수 = reshape 후 원소 개수
> ```
{: .prompt-tip }

---

## 3. 🔍 `-1`을 사용하면 자동 계산 가능

한 차원의 크기를 직접 계산하기 귀찮다면 `-1`을 사용할 수 있다.

```python
x = torch.randn(2, 3, 4)

print(x.shape)
# [2, 3, 4]
```

총 원소는 `2 × 3 × 4 = 24`이다.

다음과 같이 작성하면 PyTorch가 나머지 크기를 자동 계산한다.

```python
y = x.reshape(2, -1)
```

```text
[2, 3, 4]
 ↓
[2, 12]
```

즉 `x.reshape(2, -1)`은 `x.reshape(2, 12)`와 같은 의미이다.

---

## 4. 🧪 딥러닝에서는 언제 사용할까?

예를 들어 CNN의 출력이 다음과 같다고 하자.

```text
[Batch, Channel, Height, Width]

[32, 16, 8, 8]
```

Linear Layer에 넣기 위해 각 이미지의 Feature를 하나로 펼치고 싶다면:

```python
x = x.reshape(32, -1)
```

결과:

```text
[32, 16, 8, 8]
        ↓
[32, 1024]
```

| 차원 | 처리 |
| --- | --- |
| `32` | Batch는 유지 |
| `16 × 8 × 8` | 하나의 Feature 차원으로 합침 |

---

## 5. 🤔 `reshape()`는 안전한가?

일반적인 Shape 변경에서는 `reshape()`를 편하게 사용할 수 있다.

```python
y = x.reshape(3, 4)
```

PyTorch가 내부적으로 다음을 처리한다.

| 메모리 상태 | 처리 |
| --- | --- |
| 기존 메모리를 그대로 사용할 수 있음 | 그대로 활용 |
| 기존 메모리를 그대로 사용하기 어려움 | 필요한 경우 복사해서 새로운 Tensor 생성 |

그래서 일반적인 Shape 변경에서는 `view()`보다 사용하기 편하다.

---

## 6. ⚖️ `reshape()`와 `view()` 차이

둘 다 Shape을 변경한다.

```python
x.reshape(3, 4)

x.view(3, 4)
```

하지만 차이가 있다.

| 구분 | `reshape()` | `view()` |
| --- | --- | --- |
| 하는 일 | Shape 변경이 목적 | 기존 메모리를 다른 Shape으로 바라봄 |
| 메모리 | 메모리 상태에 따라 기존 메모리 사용 또는 복사 | Tensor의 메모리 배치가 조건에 맞아야 함 |

그래서 `reshape()`가 사용이 비교적 편하다.

예를 들어 다음처럼 차원 순서를 변경한 Tensor에서는

```python
x = torch.randn(2, 3, 4)

x = x.permute(0, 2, 1)
```

`x.view(2, 12)`가 실패할 수 있지만, `x.reshape(2, 12)`는 보통 정상적으로 처리된다.

> 💡 따라서 초반에는 **일반적인 Shape 변경 → `reshape()`** 라고 생각하면 충분하다.
{: .prompt-info }

---

## 7. 🧰 `reshape()` 말고 다른 방법

Shape을 변경한다고 해서 항상 `reshape()`를 사용하는 것은 아니다. 목적에 따라 다른 함수가
더 적합하다.

### `flatten()`

여러 차원을 하나로 펼칠 때 사용한다.

```python
x = torch.randn(32, 16, 8, 8)

y = torch.flatten(x, start_dim=1)
```

결과:

```text
[32, 16, 8, 8]
      ↓
[32, 1024]
```

CNN에서는 의미가 명확하기 때문에 자주 사용한다. 모델에서는 `nn.Flatten()`도 사용할 수 있다.

### `unsqueeze()`

크기가 `1`인 새로운 차원을 추가한다.

```python
x.shape
# [3]

y = x.unsqueeze(0)

y.shape
# [1, 3]
```

```text
[3]
 ↓
[1, 3]
```

예를 들어 Batch 차원을 추가할 때 사용할 수 있다.

### `squeeze()`

크기가 `1`인 차원을 제거한다.

```python
x.shape
# [1, 3]

y = x.squeeze(0)

y.shape
# [3]
```

```text
[1, 3]
 ↓
[3]
```

### `permute()`

Shape의 크기를 재구성하는 것이 아니라 **차원의 순서를 변경**한다.

```text
[B, H, W, C]

↓

[B, C, H, W]
```

```python
x = x.permute(0, 3, 1, 2)
```

이미지 Tensor의 차원 순서를 맞출 때 자주 사용한다.

---

## 8. 📋 함수별 역할 구분

| 함수 | 역할 |
| --- | --- |
| `reshape()` | Tensor의 전체적인 Shape 변경 |
| `flatten()` | 여러 차원을 하나로 펼침 |
| `unsqueeze()` | 크기 1인 차원 추가 |
| `squeeze()` | 크기 1인 차원 제거 |
| `permute()` | 차원 순서 변경 |
| `view()` | 기존 메모리를 이용해 Shape을 다르게 바라봄 |

---

## 9. 🧭 가장 쉽게 선택하는 방법

Shape을 바꿔야 할 때 먼저 목적을 생각한다.

| 하고 싶은 것 | 선택 |
| --- | --- |
| "그냥 다른 모양으로 만들고 싶다" | `reshape()` |
| "여러 Feature 차원을 하나로 펼치고 싶다" | `flatten()` |
| "Batch 같은 차원을 하나 추가하고 싶다" | `unsqueeze()` |
| "불필요한 크기 1 차원을 제거하고 싶다" | `squeeze()` |
| "Channel 위치처럼 차원의 순서를 바꾸고 싶다" | `permute()` |

---

## 10. ✅ 핵심 정리

```text
reshape()
→ 값은 그대로
→ Shape만 변경
→ 원소 개수는 반드시 동일
```

| 변환 | 가능 여부 |
| --- | --- |
| `[12]` → `[3, 4]` | 가능 |
| `[2, 3, 4]` → `[2, 12]` | 가능 |
| `[12]` → `[5, 3]` | 불가능 |

> 💡 **한 줄 요약** · **일반적인 Tensor Shape 변경에는 `reshape()`를 편하게 사용할 수 있고,
> 펼치기·차원 추가/제거·순서 변경처럼 목적이 명확할 때는 `flatten()`, `unsqueeze()`,
> `squeeze()`, `permute()`를 사용하면 된다.**
{: .prompt-info }

---

## 11. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **`reshape()`** : 값은 그대로 두고 Shape만 변경 — 형변환이 아니라 Shape 변환
- **원소 개수** : reshape 전 원소 개수 = reshape 후 원소 개수
- **`[12]` 기준** : `(3, 4)` `(2, 6)` `(4, 3)` 가능 / `(5, 3)` 불가능
- **`-1`** : 나머지 한 차원의 크기를 PyTorch가 자동 계산 — `[2, 3, 4]`에서 `reshape(2, -1)` = `reshape(2, 12)`
- **딥러닝 사용처** : CNN 출력 `[32, 16, 8, 8]`을 Linear에 넣기 위해 `reshape(32, -1)` → `[32, 1024]`, Batch는 유지
- **메모리 처리** : 기존 메모리를 쓸 수 있으면 그대로 활용, 어려우면 복사해서 새 Tensor 생성
- **`view()`와 차이** : `view()`는 기존 메모리를 다른 Shape으로 바라보므로 메모리 배치 조건이 맞아야 함
- **`permute()` 이후** : `view(2, 12)`는 실패할 수 있지만 `reshape(2, 12)`는 보통 정상 처리
- **`flatten()`** : 여러 차원을 하나로 펼침 — `torch.flatten(x, start_dim=1)`, `nn.Flatten()`
- **`unsqueeze()`** : 크기 1인 차원 추가 — `[3]` → `[1, 3]`, Batch 차원 추가에 사용
- **`squeeze()`** : 크기 1인 차원 제거 — `[1, 3]` → `[3]`
- **`permute()`** : 크기 재구성이 아니라 차원 순서 변경 — `[B, H, W, C]` → `[B, C, H, W]`
- **선택 기준** : 목적이 "그냥 다른 모양"이면 `reshape()`, 목적이 명확하면 전용 함수

</details>

---

## 12. 🔗 관련 글

- [입출력 차원 계산과 flatten](/posts/input-output-dimensions-and-flatten/)
- [Batch dimension과 broadcasting](/posts/batch-dimension-and-broadcasting/)
- [Tensor 기본 개념 - tensor 생성과 dtype/shape 확인](/posts/pytorch-tensor-basics/)
