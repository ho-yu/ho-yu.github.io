---
title: "SVD를 이용한 저랭크 압축과 정보 손실 분석"
date: 2026-09-06 09:00:00 +0900
categories: [Notes, Math]
tags: [linear-algebra, svd, low-rank-approximation, dimensionality-reduction, assignment]
math: true
---

> 🗂️ **Notes · Math** — `linear-algebra` `svd` `low-rank-approximation` `dimensionality-reduction` `assignment`
{: .prompt-info }

> 📌 기초수학 과제 — 문제 (3) 개념 복습 정리
{: .prompt-tip }

---

## 1. 🎯 핵심 목표

이번 문제의 핵심은 `centered_embeddings`를 SVD로 분해한 뒤,

- 중요한 정보만 남겨 **저랭크(rank-r) 행렬로 압축**
- rank에 따른 **에너지 보존율**
- 원본과 복원 행렬 사이의 **재구성 오차**
- 압축 후 필요한 **저장 원소 수**
- **정보 보존과 압축 효율의 trade-off**

를 비교하는 것이다.

전체 흐름은 다음과 같다.

```text
centered_embeddings
        ↓
   Compact SVD
        ↓
     U, S, Vᵀ
        ↓
특이값별 에너지 계산
        ↓
rank 1 / 2 / 3 저랭크 복원
        ↓
에너지 · MSE · 상대오차 · 저장량 비교
        ↓
90% 이상 보존하는 최소 rank 결정
        ↓
r_90 선택
```

---

## 2. 📖 SVD란?

SVD(Singular Value Decomposition, 특이값 분해)는 하나의 행렬을 다음 세 행렬로 분해하는
방법이다.

$$
A = U\Sigma V^T
$$

각 요소의 의미:

| 요소 | 의미 |
| --- | --- |
| $U$ | 데이터의 왼쪽 방향 정보 |
| $\Sigma$ | 각 방향의 중요도인 **특이값** |
| $V^T$ | 데이터의 오른쪽 방향 정보 |

이번 문제에서는 다음을 사용했다.

```python
U, S, Vt = np.linalg.svd(
    centered_embeddings,
    full_matrices=False
)
```

---

## 3. 🗜️ Compact SVD

```python
full_matrices=False
```

를 사용하면 불필요하게 큰 행렬을 만들지 않는 **Compact SVD**가 수행된다.

원본이

```text
centered_embeddings.shape = (12, 6)
```

이면:

```text
U.shape  = (12, 6)
S.shape  = (6,)
Vt.shape = (6, 6)
```

가 된다.

### 중요한 점

수학에서는

$$
\Sigma =
\begin{bmatrix}
\sigma_1 & 0 & \cdots\\
0 & \sigma_2 & \cdots\\
\vdots & & \ddots
\end{bmatrix}
$$

처럼 **대각행렬**이지만 NumPy는 메모리를 아끼기 위해

```python
S = [σ1, σ2, σ3, ...]
```

처럼 **1차원 벡터**로 반환한다. 따라서 복원할 때는 `np.diag(S_r)`를 이용해 대각행렬로
만들어준다.

---

## 4. 📊 특이값(Singular Value)

`S`의 각 값은 해당 SVD 성분의 중요도를 나타낸다. `S`는 큰 값부터 작은 값 순서로 정렬된다.

```text
σ1 ≥ σ2 ≥ σ3 ≥ ...
```

따라서:

- 첫 번째 성분 → 가장 중요한 정보
- 두 번째 성분 → 그다음 중요한 정보
- 세 번째 성분 → 그다음 중요한 정보

순서가 된다.

---

## 5. ⚡ 왜 특이값을 제곱하는가?

SVD에서 각 성분이 가지고 있는 **에너지(Energy)** 는

$$
\sigma_i^2
$$

로 측정한다. 따라서 각 성분의 에너지 비율은

$$
\frac{\sigma_i^2}
{\sum_j \sigma_j^2}
$$

이다.

```python
singular_energy_ratio = (
    S ** 2
) / np.sum(S ** 2)
```

### 의미

예를 들어

```text
성분 1 → 전체 정보의 68%
성분 2 → 전체 정보의 12%
성분 3 → 전체 정보의 10%
```

와 같은 방식으로 각 성분이 전체 행렬의 정보를 얼마나 담당하는지 판단할 수 있다.

---

## 6. ➕ 누적 에너지 보존율

우리는 각 성분 하나의 정보량보다 **앞에서부터 r개의 성분을 사용할 때 전체 정보를 얼마나
보존하는가**가 더 중요하다. 따라서 다음을 사용한다.

```python
cumulative_energy = np.cumsum(
    singular_energy_ratio
)
```

예:

```text
rank 1 → σ1 정보
rank 2 → σ1 + σ2 정보
rank 3 → σ1 + σ2 + σ3 정보
```

> 💡 rank는 특정 성분 하나를 의미하는 것이 아니라 **앞에서부터 r개 성분을 누적해서 사용하는
> 것**이다.
{: .prompt-info }

---

## 7. ✂️ 저랭크 근사(Truncated SVD)

원본 SVD

$$
A = U\Sigma V^T
$$

에서 중요한 앞부분 `r`개만 사용하면

$$
A_r = U_r\Sigma_rV_r^T
$$

가 된다. 이를 **rank-r approximation**, 즉 저랭크 근사라고 한다.

```python
U_r = U[:, :r]
S_r = S[:r]
Vt_r = Vt[:r, :]
```

그리고 복원:

```python
reconstructed_matrix = (
    U_r
    @ np.diag(S_r)
    @ Vt_r
)
```

---

## 8. 📏 Shape 흐름

rank가 `r`일 때:

```text
U_r        : (12, r)
S_r        : (r,)
diag(S_r)  : (r, r)
Vt_r       : (r, 6)
```

따라서:

```text
(12,r)
   @
(r,r)
   @
(r,6)
   ↓
(12,6)
```

원본과 동일한 `(12, 6)` Shape으로 복원된다.

> 📌 **핵심** · 저랭크 압축을 해도 복원 결과의 Shape은 원본과 같다. 다만 원본 정보를
> 완벽하게 가지고 있는 것이 아니라 중요한 성분 `r`개만 이용해 원본을 **근사**한다.
{: .prompt-tip }

---

## 9. ⚖️ Rank가 증가하면 어떻게 되는가?

rank를 증가시키면 사용하는 SVD 성분이 많아진다.

```text
rank ↑
   ↓
사용하는 특이값 ↑
   ↓
보존 정보 ↑
   ↓
에너지 보존율 ↑
재구성 오차 ↓
```

하지만 동시에:

```text
rank ↑
   ↓
U, S, Vᵀ에 저장할 값 ↑
   ↓
저장량 ↑
   ↓
압축 효과 ↓
```

즉 중요한 개념은 **Trade-off**이다.

```text
정보 보존 ↑  ↔  저장 공간 절감 ↓
```

---

## 10. 🔋 에너지 보존율

rank `r`의 보존 에너지는 다음과 같다.

```python
energy_ratio = cumulative_energy[r - 1]
```

왜 `r - 1`인가? Python index는 `0`부터 시작하기 때문이다.

```text
rank 1 → index 0
rank 2 → index 1
rank 3 → index 2
```

---

## 11. 📉 재구성 MSE

저랭크 복원 행렬이 원본과 얼마나 다른지를 MSE로 측정한다.

$$
MSE =
\frac{1}{mn}
\sum (A-A_r)^2
$$

```python
reconstructed_mse = np.mean(
    (centered_embeddings - reconstructed_matrix) ** 2
)
```

### 의미

```text
MSE ↓
→ 복원된 행렬이 원본과 가까움

MSE ↑
→ 정보 손실이 큼
```

정상적인 SVD에서는 `rank ↑ → MSE ↓`가 된다.

---

## 12. 📐 Relative Frobenius Error

MSE는 절대적인 평균 오차를 측정한다. 반면 Relative Frobenius Error는 **원본 행렬의 전체
크기와 비교했을 때 복원 오차가 상대적으로 얼마나 큰가**를 측정한다.

$$
\frac{\|A-A_r\|_F}
{\|A\|_F}
$$

```python
relative_frobenius_err = (
    np.linalg.norm(
        centered_embeddings - reconstructed_matrix,
        ord="fro"
    )
    /
    np.linalg.norm(
        centered_embeddings,
        ord="fro"
    )
)
```

### 해석

```text
0에 가까움
→ 원본과 매우 비슷함

값이 커짐
→ 상대적인 정보 손실이 큼
```

---

## 13. 🔗 Frobenius Norm

Frobenius Norm은 행렬 전체 원소의 크기를 하나의 값으로 표현한다.

$$
\|A\|_F =
\sqrt{
\sum_{i,j} A_{ij}^2
}
$$

벡터의 L2 Norm을 **행렬 전체로 확장한 개념**이라고 보면 된다. 문제 1에서 배운 L2 Norm과
연결된다.

```text
Vector
→ L2 Norm

Matrix
→ Frobenius Norm
```

---

## 14. 💾 저장 원소 수

원본 행렬 `m × n`의 저장량은

$$
mn
$$

이다. 이번 문제는 `12 × 6 = 72`이므로 원본은 **72개 숫자**를 저장해야 한다.

### Rank-r SVD 저장량

저랭크 SVD에서는 원본 행렬 대신

```text
U_r   → m × r
S_r   → r
Vt_r  → r × n
```

을 저장한다. 따라서 총 저장량은

$$
mr+r+rn
$$

이다.

```python
stored_elements = (
    m * r
    + r
    + r * n
)
```

이번 데이터에서는:

| Rank | 저장 원소 수 |
| ---: | ---: |
| 1 | 19 |
| 2 | 38 |
| 3 | 57 |
| 원본 | 72 |

rank가 증가할수록 저장량도 증가한다.

---

## 15. 📦 저장 절감률

원본과 비교해 저장 공간을 얼마나 줄였는지 계산한다.

$$
\frac{
원본저장량-압축저장량
}{
원본저장량
}
$$

```python
storage_reduction_ratio = (
    original_storage_elements - stored_elements
) / original_storage_elements
```

### 해석

```text
값이 큼
→ 저장 공간을 많이 줄임
→ 압축 효과 큼

값이 작음
→ 저장 공간을 적게 줄임
→ 압축 효과 작음
```

---

## 16. 🧭 압축 효율의 의미

이번 문제에서 압축 효율은 단순히 저장량만 적다는 뜻이 아니다. 핵심은 **가능한 적은
저장량으로 원본 정보를 최대한 많이 유지하는 것**이다.

따라서 함께 봐야 하는 파라미터는 다음과 같다.

```text
정보 보존
├─ retained_energy
├─ mse
└─ relative_frobenius_error

저장 효율
├─ stored_values
└─ storage_reduction
```

---

## 17. 🎚️ `r_90`

`r_90`은 **전체 에너지의 90% 이상을 보존하는 최소 rank**이다.

```python
r_90 = (
    np.argmax(cumulative_energy >= 0.9)
    + 1
)
```

동작 과정:

```text
cumulative_energy >= 0.9
          ↓
[False, False, True, ...]
          ↓
np.argmax(...)
          ↓
처음 True인 index
          ↓
+ 1
          ↓
실제 rank
```

이번 결과는 `r_90 = 3`이다. 즉 rank 3부터 전체 정보의 90% 이상을 보존한다.

---

## 18. 🤔 왜 최소 rank를 선택하는가?

예를 들어 rank 4, 5, 6도 90% 이상을 보존할 수 있다. 하지만 rank를 계속 높이면:

```text
정보 보존 ↑
MSE ↓

하지만

저장량 ↑
압축 효과 ↓
```

가 된다. 따라서 목표가 `에너지 ≥ 90%`라면 그 조건을 **처음 만족하는 최소 rank**를 선택하는
것이 합리적이다.

---

## 19. 📈 그래프로 확인하는 Trade-off

그래프에서는 두 가지를 함께 확인했다.

```text
Rank ↑
│
├─ Retained Energy ↑
│
└─ Reconstruction MSE ↓
```

이 그래프를 통해 rank를 높일수록 정보는 더 많이 보존하지만 저장 공간도 더 필요하다는
관계를 시각적으로 확인할 수 있다.

---

## 20. 🔎 이번 문제의 결과 해석

이번 결과에서:

```text
원본 저장량 = 72
r_90 = 3
rank 3 MSE ≈ 0.01958
```

이었다. 따라서 rank 3은:

- 에너지 보존율 90% 이상 만족
- 낮은 재구성 오차
- 원본 72개 대신 57개 원소 저장

이라는 특성을 가진다.

즉 rank 1·2보다 저장량은 증가하지만, **90% 정보 보존이라는 조건을 만족하는 최소
rank**라는 점에서 선택할 수 있다.

---

## 21. 🧬 PCA와 SVD의 연결

문제 2의 PCA와 문제 3의 SVD는 서로 밀접하게 연결되어 있다.

PCA에서는:

```text
공분산 행렬
→ 고유값 / 고유벡터
→ 중요한 방향 탐색
```

SVD에서는:

```text
centered_embeddings
→ U, S, Vᵀ
→ 중요한 방향 탐색
```

특히 **평균 중심화된 데이터**에 SVD를 적용하면

```text
Vᵀ의 주요 방향
↔ PCA의 주성분 방향
```

이 연결된다. 또한

```text
PCA의 고유값
↔ SVD 특이값²
```

이 서로 관련되어 있다. 그래서 동일한 rank를 사용하면 PCA와 SVD의 복원 결과 및 복원 오차가
연결된다.

---

## 22. ⚖️ 문제 2와 문제 3의 차이

| PCA | SVD |
| --- | --- |
| 공분산 행렬 사용 | 데이터 행렬 직접 분해 |
| 고유값 분해 | 특이값 분해 |
| 고유값으로 설명분산 계산 | 특이값²으로 에너지 계산 |
| 주성분 개수 `k` 선택 | rank `r` 선택 |
| 차원 축소 중심 | 저랭크 근사·압축 관점 |

하지만 두 문제 모두 핵심 질문은 비슷하다.

> 💡 **얼마나 적은 성분으로 원본 정보를 충분히 유지할 수 있는가?**
{: .prompt-info }

---

## 23. 🐍 주요 NumPy 문법 정리

### `np.linalg.svd()`

```python
U, S, Vt = np.linalg.svd(
    matrix,
    full_matrices=False
)
```

행렬을 Compact SVD로 분해한다.

### `np.diag()`

```python
np.diag(S_r)
```

```text
[5, 2, 1]

↓

[[5, 0, 0],
 [0, 2, 0],
 [0, 0, 1]]
```

1차원 특이값 벡터를 대각행렬로 만든다.

### `np.cumsum()`

```python
np.cumsum(singular_energy_ratio)
```

값을 앞에서부터 누적해서 더한다.

### `np.argmax()`

```python
np.argmax(condition)
```

조건 배열에서 처음으로 가장 큰 값(`True`)이 등장하는 index를 반환한다.

### `.size`

```python
centered_embeddings.size
```

행렬 전체 원소의 개수를 반환한다.

```text
(12,6) → 72
```

### 딕셔너리에 rank별 복원행렬 저장

```python
svd_reconstruction[r] = reconstructed_matrix
```

예:

```text
{
    1: rank1 복원행렬,
    2: rank2 복원행렬,
    3: rank3 복원행렬
}
```

따라서 `svd_reconstruction[r_90]`으로 원하는 rank의 복원행렬을 바로 가져올 수 있다.

---

## 24. ⚠️ 자주 헷갈린 부분

### ① `S_r`와 $\Sigma_r$는 Shape이 다르다

```text
S_r
→ (r,) 벡터

Σ_r
→ (r,r) 대각행렬
```

따라서 `U_r @ S_r @ Vt_r`가 아니라 `U_r @ np.diag(S_r) @ Vt_r`를 사용한다.

### ② rank 3은 세 번째 성분 하나가 아니다

```text
rank 1 = 성분 1

rank 2 = 성분 1 + 2

rank 3 = 성분 1 + 2 + 3
```

즉 누적 개념이다.

### ③ 에너지 보존율의 분모는 전체 S

rank 2의 에너지를 계산한다고 해서 `S_r² / sum(S_r²)`를 사용하면 안 된다. 그러면 선택된 성분
안에서 다시 100%가 되어버린다. 비교 기준은 항상 **전체 SVD 에너지**이다.

### ④ MSE는 평균까지 계산해야 한다

```python
(centered_embeddings - reconstructed_matrix) ** 2
```

는 제곱오차 **행렬**이다. MSE는 `np.mean(...)`까지 수행해야 숫자 하나가 된다.

### ⑤ 저장 원소 수는 Shape의 합이 아니라 곱

행렬 `(12, 3)`의 원소 수는:

```text
12 + 3 ❌

12 × 3 ✅
```

이다.

---

## 25. 🔄 문제 3의 핵심 Trade-off

최종적으로 봐야 하는 관계는 이것이다.

```text
                 rank 증가
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
   정보 보존 증가             저장량 증가
        ↓                       ↓
 retained_energy ↑       storage_reduction ↓
 MSE ↓
 relative error ↓
```

즉 좋은 rank란 단순히 가장 큰 rank가 아니라 **필요한 정보 보존 기준을 만족하면서 저장량을
가능한 적게 사용하는 rank**이다.

---

## 26. ✅ 핵심 요약

> 💡 **SVD는 행렬을 중요한 특이 성분으로 분해하고, 앞의 r개 성분만 사용해 원본을 저랭크로
> 근사한다. rank가 증가하면 에너지 보존율은 높아지고 복원 오차는 감소하지만 저장량이
> 증가하므로, 정보 보존과 압축 효율 사이의 trade-off를 고려해 적절한 rank를 선택해야 한다.**
{: .prompt-info }

---

## 27. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **SVD** : $A = U\Sigma V^T$ — $U$ 왼쪽 방향 정보 / $\Sigma$ 각 방향의 중요도(특이값) / $V^T$ 오른쪽 방향 정보
- **Compact SVD** : `full_matrices=False` — `(12,6)` 입력에서 `U (12,6)`, `S (6,)`, `Vt (6,6)`
- **`S`는 벡터** : 수학의 $\Sigma$는 대각행렬이지만 NumPy는 1차원 벡터로 반환 → 복원 시 `np.diag(S_r)` 필요
- **특이값 정렬** : `σ1 ≥ σ2 ≥ σ3 ≥ ...` — 앞쪽일수록 중요한 정보
- **에너지** : 성분의 에너지는 $\sigma_i^2$, 비율은 $\sigma_i^2 / \sum_j \sigma_j^2$
- **누적 에너지** : `np.cumsum()` — rank r은 앞에서부터 r개 성분을 누적해서 쓰는 것
- **저랭크 근사** : $A_r = U_r\Sigma_rV_r^T$ — `U[:, :r]`, `S[:r]`, `Vt[:r, :]`
- **Shape** : `(12,r) @ (r,r) @ (r,6)` = `(12,6)` — 압축해도 복원 Shape은 원본과 같고, 내용은 근사
- **Trade-off** : rank ↑ → 에너지 보존 ↑, MSE ↓ / 저장량 ↑, 압축 효과 ↓
- **`cumulative_energy[r - 1]`** : Python index가 0부터라 rank r은 index r-1
- **재구성 MSE** : $\frac{1}{mn}\sum(A-A_r)^2$ — `np.mean((원본 - 복원) ** 2)`
- **Relative Frobenius Error** : $\|A-A_r\|_F / \|A\|_F$ — 원본 크기 대비 상대적 오차, `ord="fro"`
- **Frobenius Norm** : $\sqrt{\sum_{i,j}A_{ij}^2}$ — 벡터 L2 Norm을 행렬로 확장한 개념
- **저장량** : 원본 $mn$ = 72 / rank-r은 $mr+r+rn$ — rank 1·2·3 = 19·38·57
- **`r_90`** : `np.argmax(cumulative_energy >= 0.9) + 1` — 이번 결과 3
- **최소 rank를 쓰는 이유** : rank 4~6도 90%를 넘지만 저장량만 늘고 압축 효과가 줄어듦
- **이번 결과** : rank 3 → 에너지 90% 이상, MSE ≈ 0.01958, 72개 대신 57개 저장
- **PCA ↔ SVD** : 평균 중심화 데이터에서 `Vᵀ의 주요 방향 ↔ PCA 주성분`, `PCA 고유값 ↔ SVD 특이값²`
- **헷갈린 점** : `S_r (r,)` ≠ `Σ_r (r,r)` / rank 3은 누적 3개 / 에너지 분모는 항상 전체 S / MSE는 `np.mean`까지 / 저장 원소 수는 Shape의 곱

</details>

---

## 28. 🔗 관련 글

- [PCA와 고유값 분해 핵심 정리](/posts/pca-and-eigen-decomposition/)
- [Projection과 Cosine Similarity 핵심 정리](/posts/projection-and-cosine-similarity/)
- [벡터 기초 — 정의부터 정규화까지](/posts/vector-basics/)
