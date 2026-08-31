---
title: "torch.cat()과 dim 이해하기"
date: 2026-08-31 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, tensor, torch-cat, dim, tensor-shape]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `tensor` `torch-cat` `dim` `tensor-shape`
{: .prompt-info }

---

## 1. 💡 `torch.cat()`이란?

`torch.cat()`은 **여러 텐서를 특정 차원 방향으로 이어붙이는 함수**다.

```python
torch.cat([tensor1, tensor2], dim=0)
```

기본 형태:

```text
여러 Tensor → torch.cat() → 하나의 Tensor
```

---

## 2. 💡 `dim`이란?

`dim`은 **어느 차원 방향으로 붙일지 지정하는 값**이다.

```python
a = torch.tensor([
    [1, 2],
    [3, 4]
])

b = torch.tensor([
    [5, 6],
    [7, 8]
])
```

각 텐서의 shape은 `(2, 2)`이다. 같은 `a`, `b`라도 `dim`에 따라 결과가 아래 그림처럼 달라진다.

![torch.cat의 dim에 따른 결과 비교 — a와 b가 각각 (2, 2)일 때 dim=0이면 세로로 쌓여 (4, 2)가 되어 행이 늘어나고, dim=1이면 가로로 이어붙여 (2, 4)가 되어 열이 늘어난다](/assets/img/posts/torch-cat-dim/cat-dim.svg){: w="720" h="404" }

---

## 3. 📖 `dim=0`

```python
torch.cat([a, b], dim=0)
```

결과:

```text
[[1, 2],
 [3, 4],
 [5, 6],
 [7, 8]]
```

shape:

```text
(2, 2) → (4, 2)
```

즉 **0번째 차원 방향으로 이어붙인다.** 2차원 표에서는 쉽게 **행이 늘어난다**고 생각하면 된다.

---

## 4. 📖 `dim=1`

```python
torch.cat([a, b], dim=1)
```

결과:

```text
[[1, 2, 5, 6],
 [3, 4, 7, 8]]
```

shape:

```text
(2, 2) → (2, 4)
```

즉 **1번째 차원 방향으로 이어붙인다.** 2차원 표에서는 쉽게 **열이 늘어난다**고 생각하면 된다.

---

## 5. 🔍 `dim`을 이해하는 핵심

Tensor의 shape이 `(batch, feature)`라면:

| `dim` | 방향 |
| --- | --- |
| `dim=0` | batch 방향 |
| `dim=1` | feature 방향 |

예를 들어 `(32, 10)`에서:

- `dim=0` → 데이터 개수 방향
- `dim=1` → feature 개수 방향

---

## 6. ⚠️ 주의점

`cat()`에서는 **붙이는 차원을 제외한 나머지 shape이 같아야 한다.**

| Shape 조합 | 연결 가능한 `dim` |
| --- | --- |
| `(3, 4)` + `(5, 4)` | `dim=0` |
| `(3, 4)` + `(3, 6)` | `dim=1` |

---

## 7. 🔍 `torch.cat()`과 `torch.stack()`의 차이

이름이 비슷해 헷갈리기 쉬운 함수로 `torch.stack()`이 있다. 둘의 차이는 **차원이 늘어나는가**에
있다.

| 함수 | 붙이는 방식 | 차원 수 |
| --- | --- | --- |
| `torch.cat()` | 이미 있는 차원 방향으로 이어붙인다 | 그대로 |
| `torch.stack()` | 새로운 차원을 만들어 쌓는다 | 하나 늘어난다 |

같은 `a`, `b`(둘 다 `(2, 2)`)를 넣어도 결과 shape이 다르다.

```python
torch.cat([a, b], dim=0).shape      # (4, 2)  — 2차원 그대로
torch.stack([a, b], dim=0).shape    # (2, 2, 2) — 3차원으로 늘어남
```

`stack()`의 결과 `(2, 2, 2)`에서 맨 앞의 `2`는 **쌓은 텐서의 개수**(`a`, `b`)이다.

> 💡 이어붙여서 **더 길어진 하나**를 만들고 싶으면 `cat()`, 원본을 그대로 두고 **여러 개를
> 나란히 묶고** 싶으면 `stack()`이라고 기억하면 구분하기 쉽다.
{: .prompt-info }

---

## 8. 🧪 코드로 확인하기

```python
import torch

a = torch.tensor([[1, 2],
                  [3, 4]])
b = torch.tensor([[5, 6],
                  [7, 8]])

print(torch.cat([a, b], dim=0))
print(torch.cat([a, b], dim=0).shape)   # (4, 2)

print(torch.cat([a, b], dim=1))
print(torch.cat([a, b], dim=1).shape)   # (2, 4)
```

---

## 9. ✅ 핵심 요약

```text
torch.cat()
= 여러 Tensor를 이어붙이는 함수

dim
= 어느 차원 방향으로 붙일지 결정

dim=0 → 첫 번째 차원
dim=1 → 두 번째 차원
```

> 💡 **한 줄 요약** · 2차원 Tensor에서는 처음에는 **`dim=0`은 행 방향, `dim=1`은 열
> 방향**이라고 기억하면 이해하기 쉽다.
{: .prompt-info }

---

## 10. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **`torch.cat()`** : 여러 텐서를 특정 차원 방향으로 이어붙이는 함수
- **`dim`** : 어느 차원 방향으로 붙일지 지정하는 값
- **`dim=0`** : 0번째 차원 방향 → 2차원에서는 행이 늘어난다 → `(2,2)` + `(2,2)` = `(4,2)`
- **`dim=1`** : 1번째 차원 방향 → 2차원에서는 열이 늘어난다 → `(2,2)` + `(2,2)` = `(2,4)`
- **`(batch, feature)`에서** : `dim=0`은 데이터 개수 방향, `dim=1`은 feature 개수 방향
- **주의** : 붙이는 차원을 제외한 나머지 shape이 같아야 한다
- **예** : `(3,4)` + `(5,4)` → `dim=0` 가능 / `(3,4)` + `(3,6)` → `dim=1` 가능
- **`stack()`과 차이** : `cat()`은 차원 수 그대로 `(4,2)`, `stack()`은 새 차원이 생겨 `(2,2,2)`

</details>

---

## 11. 🔗 관련 글

- [PyTorch argmax() 이해하기](/posts/pytorch-argmax-and-dim/)
- [Batch dimension과 broadcasting](/posts/batch-dimension-and-broadcasting/)
- [위험한 Broadcasting — 에러 없이 틀리는 Shape 불일치](/posts/dangerous-broadcasting/)
