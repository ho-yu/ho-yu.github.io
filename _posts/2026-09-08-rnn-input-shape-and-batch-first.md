---
title: "RNN 입력 Shape과 batch_first — 시점 L과 h_n 읽는 법"
date: 2026-09-08 11:00:00 +0900
categories: [Notes, Deep Learning]
tags: [rnn, sequence, hidden-state, tensor-shape, pytorch]
---

> 🗂️ **Notes · Deep Learning** — `rnn` `sequence` `hidden-state` `tensor-shape` `pytorch`
{: .prompt-info }

---

## 1. 📖 RNN이란?

RNN(Recurrent Neural Network)은 **순서가 있는 데이터를 처리하기 위한 신경망**이다.

일반적인 신경망과 달리 RNN은 현재 입력만 보는 것이 아니라,

> **현재 입력 + 이전 시점의 Hidden State**

를 함께 사용한다. 즉 이전까지 처리한 정보를 `Hidden State`에 담아 다음 시점으로 전달한다.

```text
x1 → h1
     ↓
x2 → h2
     ↓
x3 → h3
     ↓
x4 → h4
```

수식으로는 다음과 같이 표현할 수 있다.

```text
h_t = f(x_t, h_(t-1))
```

| 기호 | 의미 |
| --- | --- |
| `x_t` | 현재 시점의 입력 |
| `h_(t-1)` | 이전 시점의 Hidden State |
| `h_t` | 현재 시점에서 새롭게 계산된 Hidden State |

---

## 2. 📐 입력 Shape `[B, L, D_in]`

예제 코드:

```python
x = torch.randn(2, 5, 4)
```

`batch_first=True`일 때 입력 Shape은 `[B, L, D_in]`이고, 현재 값은 `[2, 5, 4]`이다.
각 숫자가 무엇을 세는지는 아래 그림처럼 나눠 보면 명확해진다.

![입력 [2, 5, 4]를 분해한 그림 — Sample 1과 Sample 2 두 줄이 B=2, 각 줄에 t=1부터 t=5까지 5개의 시점 상자가 L=5, 각 시점 상자 안의 작은 칸 4개가 D_in=4를 나타낸다](/assets/img/posts/rnn-input-shape-and-batch-first/input-shape.svg){: w="720" h="300" }

| 기호 | 값 | 의미 |
| --- | --- | --- |
| `B` | 2 | Batch Size — 샘플 2개 |
| `L` | 5 | Sequence Length — 각 샘플을 5개의 시점으로 처리 |
| `D_in` | 4 | 각 시점마다 입력되는 Feature 개수 |

---

## 3. ⏱️ "각 샘플에 5가지 시점"의 의미

> ❓ "각 샘플에 5가지 시점이라는 말은, 입력받은 문장이 총 5번에 걸쳐서 작업을 해야한다는
> 의미인지?"

거의 맞지만 정확하게는

> **한 문장을 5번 반복해서 처리하는 것이 아니라, 문장을 구성하는 5개의 입력을 순서대로 5개
> 시점에 걸쳐 처리한다.**

예:

```text
나는 / 오늘 / 학교에 / 정말 / 간다
```

RNN은 개념적으로 다음과 같이 처리한다.

```text
1시점: 나는
→ h1

2시점: 오늘 + h1
→ h2

3시점: 학교에 + h2
→ h3

4시점: 정말 + h3
→ h4

5시점: 간다 + h4
→ h5
```

따라서

```text
L = 5
= RNN이 순서대로 처리해야 하는 단계가 5개
```

이다.

> 💡 **직접 5번 호출하지 않는다** · PyTorch에서는 `output, h_n = rnn(x)`를 한 번 호출하면
> 내부적으로 전체 Sequence를 처리한다.
{: .prompt-info }

---

## 4. 🔄 `batch_first=True`

> ❓ "`batch_first=true` 키워드에 대해서 자세히 설명해줘."

PyTorch RNN의 기본 입력 Shape은 `[L, B, D]`이다. 즉 기본값은 `batch_first=False`이다.
하지만 `batch_first=True`를 설정하면 입력을 `[B, L, D]` 순서로 사용할 수 있다.

![왼쪽은 PyTorch 기본값인 batch_first=False의 [L, B, D] 축 순서, 오른쪽은 batch_first=True의 [B, L, D] 축 순서이며 이번 코드의 x.shape = [2, 5, 4]가 여기에 해당한다는 비교, 아래에 h_n에는 batch_first가 적용되지 않는다는 주의](/assets/img/posts/rnn-input-shape-and-batch-first/batch-first.svg){: w="720" h="330" }

예:

```python
x.shape = [2, 5, 4]
```

```text
2 = Batch
5 = Sequence Length
4 = Feature
```

### 왜 `batch_first=True`를 쓰는가

> ❓ "결국, 디폴트로 정해져 있는데, 가독성 좋으라고 true 옵션 넣는거네?"

맞다. `batch_first=True`는 **모델 성능을 바꾸는 옵션이 아니다.** 데이터 Shape을 `[B, L, D]`
형태로 만들어 사람이 읽고 다루기 편하게 만드는 옵션이다.

```text
batch_first=True
→ 가독성과 사용 편의성 향상
```

> ⚠️ **중요한 예외** · `h_n`에는 `batch_first=True`가 적용되지 않는다.
{: .prompt-warning }

---

## 5. 🧠 Hidden State

Hidden State는 RNN이 **현재 시점까지 처리한 정보를 담고 있는 내부 상태**이다.

```text
x1 → h1
x2 + h1 → h2
x3 + h2 → h3
x4 + h3 → h4
x5 + h4 → h5
```

여기서 `h1, h2, h3, h4, h5`는 모두 각각의 시점에서 생성된 Hidden State이다.
`hidden_size=6`이라면 각 Hidden State는 Feature 6개를 갖는다.

---

## 6. 📦 `output` — 모든 시점의 Hidden State

> ❓ "rnn의 return 값에서 output은 뭐야. h_n은 마지막 hidden_state고."

RNN의 반환값은 다음과 같다.

```python
output, h_n = rnn(x)
```

여기서 `output`은

> **모든 시점에서 생성된 Hidden State들의 묶음**

이다. 예를 들어 Sequence Length가 5라면

```text
output = [h1, h2, h3, h4, h5]
```

이다.

> ❓ "output은 hidden_State를 모아놓은 값. 즉 hidden_state들의 묶음인거네?"

맞다. 이 표현이 가장 직관적이다.

### `output.shape`

현재 코드가

```python
x.shape = [2, 5, 4]
hidden_size = 6
batch_first = True
```

라면 `output.shape`은 `[2, 5, 6]`이다. 즉 `[B, L, H]`이며

```text
2 = 샘플
5 = 시점
6 = Hidden Feature
```

이다.

---

## 7. 🎯 `h_n` — 최종 Hidden State

`h_n`은 RNN의 **최종 Hidden State**이다. 단층·단방향 RNN이라면 `h_n = h5`라고 이해할 수 있다.

Shape 공식은 다음과 같다.

```text
[num_layers × num_directions, B, H]
```

현재 코드에 대입하면

| 항목 | 값 |
| --- | --- |
| `num_layers` | 1 |
| `num_directions` | 1 |
| `B` | 2 |
| `H` | 6 |

이므로

```text
[1 × 1, 2, 6]
= [1, 2, 6]
```

따라서 `h_n.shape`은 `(1, 2, 6)`이다.

지금까지의 `output`과 `h_n`의 관계를 한 장으로 보면 다음과 같다.

![x1부터 x5까지의 입력이 h1부터 h5까지의 Hidden State를 만들고, 그 다섯 개 전체가 output = [h1, h2, h3, h4, h5]이며 shape은 [B, L, H] = [2, 5, 6]인 반면, 마지막 h5가 output[:, -1, :] ≈ h_n[0]에 해당하고 h_n.shape은 (1, 2, 6)이라는 관계](/assets/img/posts/rnn-input-shape-and-batch-first/output-vs-hn.svg){: w="720" h="330" }

---

## 8. 🔍 `output[:, -1, :]`과 `h_n`

> ❓ "그러면, last_hidden값으로 output[:, -1, :] 이 의미는 출력된 hidden_State들을 역정렬한
> 후에, 제일 첫번째거. 즉, 제일 마지막의 hidden_State를 가져오는거고."

여기서 한 가지 정정이 필요하다.

> ⚠️ **`-1`은 역정렬이 아니다** · Python에서 `a[-1]`은 **마지막 원소 선택**이다.
{: .prompt-warning }

따라서 `output[:, -1, :]`은

```text
모든 Batch
+
마지막 시점
+
모든 Hidden Feature
```

를 가져온다. 즉 단층·단방향 RNN에서는

```text
output[:, -1, :]
≈ h_n[0]
```

이다.

### `h_n`이 있는데 왜 `output[:, -1, :]`을 쓰는가?

> ❓ "그런데, 이미 h_n으로 last_hidden_state를 return하는데 굳이 이런 행위를 하는 이유가 뭔지"

단층·단방향에서는 둘 다 같은 최종 Hidden State를 얻을 수 있다.

| 방식 | 의미 |
| --- | --- |
| `output[:, -1, :]` | `output`에 들어 있는 모든 시점 중 마지막 시점을 직접 선택 |
| `h_n[0]` | RNN이 별도로 반환한 최종 Hidden State 사용 |

### Multi-Layer에서는 차이가 있다

`num_layers=3`이라면

```text
Layer 1 → 마지막 Hidden
Layer 2 → 마지막 Hidden
Layer 3 → 마지막 Hidden
```

`h_n`은 모든 Layer의 최종 Hidden을 가진다. 반면 `output`은

> 마지막 Layer의 모든 시점 Hidden State

만 가진다. 두 값이 가리키는 위치를 그림으로 보면 차이가 분명해진다.

![num_layers=3인 RNN의 Layer 1부터 Layer 3까지, t=1부터 t=5까지의 Hidden State 격자에서 output은 마지막 Layer인 Layer 3의 가로 한 줄 전체를 가리키고 h_n은 각 Layer의 마지막 시점인 t=5 세로 한 줄을 가리킨다](/assets/img/posts/rnn-input-shape-and-batch-first/multi-layer.svg){: w="720" h="344" }

### Bidirectional RNN에서는 더 중요하다

양방향 RNN에서는

```text
Forward 방향 최종 Hidden
Backward 방향 최종 Hidden
```

을 `h_n`에서 각각 얻을 수 있다.

> ⚠️ 따라서 양방향 RNN에서는 단순히 `output[:, -1, :]`과 `h_n`을 동일하게 보면 안 된다.
{: .prompt-warning }

---

## 9. ✅ 핵심 정리

| 항목 | 내용 |
| --- | --- |
| RNN | 순서가 있는 데이터를 처리 |
| `[B, L, D]` | Batch / Sequence Length / Feature |
| `L` | RNN이 처리하는 시점 개수 |
| Hidden State | 현재 시점까지의 내부 정보 |
| `output` | 모든 시점의 Hidden State 묶음 |
| `h_n` | 각 Layer / 방향의 최종 Hidden State |
| `output[:, -1, :]` | 마지막 시점의 Hidden State 선택 |

> 💡 **한 줄 요약** · **RNN은 Hidden State를 다음 시점으로 전달하며 Sequence를 처리하고,
> `output`에는 모든 시점의 Hidden State가, `h_n`에는 최종 Hidden State가 담긴다.**
{: .prompt-info }

---

## 10. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **RNN** : 현재 입력 + 이전 시점의 Hidden State를 함께 사용 — `h_t = f(x_t, h_(t-1))`
- **입력 Shape** : `batch_first=True`이면 `[B, L, D_in]` — 예제는 `[2, 5, 4]`
- **`B`** : Batch Size — 샘플 개수 (예제 2)
- **`L`** : Sequence Length — 순서대로 처리하는 시점 개수 (예제 5)
- **`D_in`** : 한 시점에 들어가는 Feature 개수 (예제 4)
- **시점의 의미** : 문장을 5번 반복 처리가 아니라, 5개의 입력을 5개 시점에 걸쳐 처리
- **호출** : `output, h_n = rnn(x)` 한 번이면 내부에서 전체 Sequence를 처리
- **`batch_first`** : 기본값 `False`(`[L, B, D]`) → `True`면 `[B, L, D]`
- **`batch_first`의 성격** : 성능이 아니라 가독성·사용 편의성 옵션
- **예외** : `h_n`에는 `batch_first=True`가 적용되지 않는다
- **Hidden State** : 현재 시점까지 처리한 정보를 담은 내부 상태 — `hidden_size=6`이면 Feature 6개
- **`output`** : 모든 시점의 Hidden State 묶음 — `[B, L, H] = [2, 5, 6]`
- **`h_n`** : 최종 Hidden State — `[num_layers × num_directions, B, H] = (1, 2, 6)`
- **`-1`** : 역정렬이 아니라 **마지막 원소 선택**
- **`output[:, -1, :]`** : 모든 Batch + 마지막 시점 + 모든 Hidden Feature → 단층·단방향에서 `≈ h_n[0]`
- **Multi-Layer** : `h_n`은 모든 Layer의 최종 Hidden, `output`은 마지막 Layer의 모든 시점
- **Bidirectional** : `h_n`에서 Forward·Backward 최종 Hidden을 각각 얻으므로 `output[:, -1, :]`과 같다고 보면 안 된다

</details>

---

## 11. 🔗 관련 글

- [RNN의 Hidden State와 output — 무엇이 최종 표현인가](/posts/rnn-hidden-state-and-output/)
- [경사 소실과 경사 폭발 — LSTM/GRU와 Gradient Clipping](/posts/vanishing-exploding-gradient/)
