---
title: "CNN의 Padding과 Stride 이해하기"
date: 2026-08-28 13:00:00 +0900
categories: [Notes, Deep Learning]
tags: [pytorch, cnn, conv2d, padding, stride]
---

> 🗂️ **Notes · Deep Learning** — `pytorch` `cnn` `conv2d` `padding` `stride`
{: .prompt-info }

---

## 1. 💡 먼저 핵심 개념

CNN에서 `Padding`과 `Stride`는 모두 **Convolution 결과의 공간 크기(H, W)에 영향을 주는
설정값**이다.

| 설정값 | 하는 일 |
| --- | --- |
| `Padding` | 입력 가장자리에 여유 공간을 추가 |
| `Stride` | Kernel이 몇 칸씩 이동할지 결정 |

---

## 2. 📖 Padding

`padding`은 입력 가장자리에 값을 덧붙이는 것이다.

```python
nn.Conv2d(
    in_channels=3,
    out_channels=8,
    kernel_size=3,
    padding=1
)
```

`padding=1`이면 이미지 주변에 한 칸을 추가한다.

```text
원본

[1 2 3]
[4 5 6]
[7 8 9]

padding=1

[0 0 0 0 0]
[0 1 2 3 0]
[0 4 5 6 0]
[0 7 8 9 0]
[0 0 0 0 0]
```

### Padding을 사용하는 이유

| | 결과 |
| --- | --- |
| Padding 없음 | Conv를 통과할수록 H, W가 감소 |
| Padding 사용 | 출력 크기 감소를 조절 / 이미지 가장자리 정보도 더 잘 활용 |

아래 그림은 같은 입력 `[1, 3, 32, 32]`에 `padding=0`과 `padding=1`을 각각 적용했을 때의
차이이다.

![CNN Convolution에서 Padding의 효과 — 입력 [1, 3, 32, 32]에 kernel=3, padding=0으로 Conv2d를 적용하면 가장자리를 채우지 않아 가로·세로가 2씩 줄어 [1, 8, 30, 30]이 되고, padding=1로 한 칸을 0으로 채우면 34×34가 되어 출력이 [1, 8, 32, 32]로 입력 크기를 유지한다](/assets/img/posts/cnn-padding-and-stride/padding-effect.png){: w="1448" h="1086" }

즉 `kernel_size=3`, `stride=1`에서는 보통 `padding=1`을 주면 공간 크기를 유지할 수 있다.

---

## 3. 📖 Stride

`stride`는 **Kernel이 한 번 계산한 뒤 몇 칸씩 이동할지**를 의미한다.

```python
nn.Conv2d(
    in_channels=3,
    out_channels=8,
    kernel_size=3,
    padding=1,
    stride=1
)
```

`stride=1`이면 다음처럼 한 칸씩 이동한다.

```text
위치 1
↓ 한 칸 이동
위치 2
↓ 한 칸 이동
위치 3
...
```

즉 촘촘하게 모든 영역을 본다.

---

## 4. 🔍 `stride=2`라면?

```python
nn.Conv2d(
    in_channels=3,
    out_channels=8,
    kernel_size=3,
    padding=1,
    stride=2
)
```

Kernel이 두 칸씩 이동한다.

```text
위치 1
↓ 두 칸 이동
위치 3
↓ 두 칸 이동
위치 5
...
```

따라서 확인하는 위치 수가 줄어들고 출력 크기도 작아진다. 아래 그림은 같은 입력에서
`stride=1`과 `stride=2`를 비교한 것이다.

![CNN에서 Stride가 출력 크기에 미치는 영향 — 입력 [1, 3, 32, 32]에 kernel=3, padding=1을 공통으로 두고 stride=1이면 커널이 한 칸씩 이동해 모든 위치를 촘촘히 커버하며 출력이 [1, 8, 32, 32]로 유지되지만, stride=2이면 두 칸씩 점프해 일부 위치만 샘플링하며 출력이 [1, 8, 16, 16]으로 절반이 된다](/assets/img/posts/cnn-padding-and-stride/stride-effect.png){: w="1448" h="1086" }

> 💡 `stride`가 커질수록 공간 크기는 더 빠르게 감소한다.
{: .prompt-info }

---

## 5. 🧪 Padding과 Stride를 같이 보면

```python
x = torch.randn(1, 3, 32, 32)
```

| Case | `kernel_size` | `padding` | `stride` | 출력 Shape |
| --- | :---: | :---: | :---: | --- |
| 1 | 3 | 0 | 1 | `[1, 8, 30, 30]` |
| 2 | 3 | 1 | 1 | `[1, 8, 32, 32]` |
| 3 | 3 | 1 | 2 | `[1, 8, 16, 16]` |

```python
# Case 1
nn.Conv2d(3, 8, kernel_size=3, padding=0, stride=1)

# Case 2
nn.Conv2d(3, 8, kernel_size=3, padding=1, stride=1)

# Case 3
nn.Conv2d(3, 8, kernel_size=3, padding=1, stride=2)
```

---

## 6. 🧠 가장 쉽게 기억하기

> 💡 **Padding** · "이미지 바깥에 여백 추가" → 가장자리 정보 보완, 출력 크기 감소 조절
{: .prompt-info }

> 📌 **Stride** · "Kernel이 몇 칸씩 이동할까?"
>
> - `stride=1` → 한 칸씩 이동 → 촘촘하게 확인
> - `stride=2` → 두 칸씩 이동 → 더 거칠게 확인 → 출력 크기 감소
{: .prompt-tip }

---

## 7. ✅ 핵심 정리

| 설정값 | 커지면 |
| --- | --- |
| `Padding` ↑ | 출력 공간 크기를 유지하거나 덜 줄어들게 함 |
| `Stride` ↑ | Kernel 이동 간격 증가 → 출력 공간 크기가 더 작아짐 |

> 💡 **한 줄 요약** · **Padding은 입력 가장자리에 여유 공간을 추가해서 출력 크기와 가장자리
> 정보 손실을 조절하고, Stride는 Kernel의 이동 간격을 조절해서 출력의 공간 크기를
> 결정한다.**
{: .prompt-info }

---

## 8. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **공통점** : Padding과 Stride 모두 Convolution 결과의 공간 크기(H, W)에 영향을 준다
- **Padding** : 입력 가장자리에 값을 덧붙이는 것 — `padding=1`이면 주변에 한 칸 추가
- **Padding의 이유** : 출력 크기 감소를 조절하고, 가장자리 정보도 더 잘 활용하기 위해
- **크기 유지 조합** : `kernel_size=3`, `stride=1`에서 `padding=1`이면 공간 크기 유지
- **Stride** : Kernel이 한 번 계산한 뒤 몇 칸씩 이동할지
- **`stride=1`** : 한 칸씩 이동 → 촘촘하게 모든 영역 확인
- **`stride=2`** : 두 칸씩 이동 → 확인 위치가 줄고 출력 크기도 작아진다
- **`[1, 3, 32, 32]` 기준** : `p=0,s=1` → `[1, 8, 30, 30]` / `p=1,s=1` → `[1, 8, 32, 32]` / `p=1,s=2` → `[1, 8, 16, 16]`

</details>

---

## 9. 🔗 관련 글

- [CNN Kernel 이해하기](/posts/cnn-kernel/)
- [입출력 차원 계산과 flatten](/posts/input-output-dimensions-and-flatten/)
- [PyTorch shape·device 오류 디버깅 체크리스트](/posts/pytorch-shape-device-debugging/)
