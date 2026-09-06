---
title: "PCA와 고유값 분해 핵심 정리"
date: 2026-09-05 10:00:00 +0900
categories: [Notes, Math]
tags: [linear-algebra, pca, eigenvalue, dimensionality-reduction, assignment]
math: true
---

> 🗂️ **Notes · Math** — `linear-algebra` `pca` `eigenvalue` `dimensionality-reduction` `assignment`
{: .prompt-info }

> 📌 기초수학 과제 — 문제 (2) 개념 복습 정리
{: .prompt-tip }

---

## 1. 🔄 전체 흐름

```text
원본 임베딩 (12, 6)
        ↓
평균 중심화
        ↓
공분산 행렬 (6, 6)
        ↓
고유값 · 고유벡터 계산
        ↓
고유값 큰 순서대로 정렬
        ↓
설명분산비 계산
        ↓
90% 이상 유지하는 최소 차원 결정
        ↓
상위 주성분으로 투영
6차원 → 3차원
        ↓
다시 6차원으로 복원
        ↓
MSE로 정보 손실 확인
```

> 💡 **핵심** · 데이터의 분산을 많이 보존하는 방향만 남겨 차원을 줄이는 것이다.
{: .prompt-info }

---

## 2. 📖 PCA란?

PCA(Principal Component Analysis)는 **데이터가 가장 많이 퍼져 있는 방향을 새로운 축으로
찾아, 중요한 정보는 최대한 유지하면서 차원을 줄이는 방법**이다.

예를 들어 다음처럼 압축할 수 있다.

```text
원래 데이터
6차원

↓

PCA

↓

중요한 정보가 많은
3차원
```

---

## 3. 🎯 평균 중심화

```python
embedding_mean = np.mean(document_embeddings, axis=0).reshape(1, 6)

centered_embeddings = document_embeddings - embedding_mean
```

각 열의 평균을 구한 후 원본 데이터에서 빼준다.

Shape:

```text
document_embeddings : (12, 6)

embedding_mean       : (1, 6)

centered_embeddings  : (12, 6)
```

### 의미

원래 데이터를 **평균 위치 기준**으로 옮기는 과정이다.

예:

```text
원본
[8, 10, 12]

평균
10

평균 제거
[-2, 0, 2]
```

즉:

```text
원래 값 자체
↓
평균에서 얼마나 떨어져 있는지
```

를 보게 된다.

### 왜 필요한가?

PCA는 데이터가 **어느 방향으로 얼마나 퍼져 있는지**를 분석한다. 따라서 데이터의 절대
위치보다 **평균을 기준으로 한 퍼짐**이 중요하다.

> 💡 **기억** · 평균 중심화 = 데이터의 중심을 0으로 이동.
{: .prompt-info }

---

## 4. 📊 공분산 행렬

```python
covariance = np.cov(
    centered_embeddings,
    rowvar=False,
    ddof=1
)
```

Shape:

```text
centered_embeddings : (12, 6)

↓

covariance           : (6, 6)
```

공분산 행렬은 **각 차원이 서로 어떻게 함께 변하는지**를 나타낸다.

| 관계 | 공분산 |
| --- | --- |
| A가 증가할 때 B도 증가 | 양의 공분산 |
| A가 증가할 때 B는 감소 | 음의 공분산 |

공분산 행렬의 대각선에는 각 변수의 **분산**이 들어간다.

### `rowvar=False`

```text
행(row) = 데이터 샘플
열(column) = 변수/차원
```

으로 해석하라는 뜻이다. 현재 데이터가 `12개 문서 × 6개 임베딩 차원`이므로 적절하다.

### `ddof=1`

**표본 공분산**을 계산한다는 의미다. 즉 분모를 `N`이 아니라 `N - 1`로 사용한다.

---

## 5. 🔍 고유값과 고유벡터

```python
eigenvalues, eigenvectors = np.linalg.eigh(covariance)
```

공분산 행렬은 대칭행렬이므로 `np.linalg.eigh()`를 사용한다.

### 고유벡터

고유벡터는 **데이터가 퍼져 있는 새로운 방향**이다. PCA에서는 이 고유벡터가 바로 **주성분
방향**이 된다.

```text
PC1
PC2
PC3
...
```

### 고유값

고유값은 **해당 고유벡터 방향으로 데이터를 투영했을 때의 분산 크기**를 나타낸다.

```text
고유값 큼
→ 그 방향으로 데이터가 많이 퍼져 있음
→ 많은 정보를 담고 있음

고유값 작음
→ 그 방향의 변화가 적음
→ 상대적으로 정보가 적음
```

---

## 6. 🤔 왜 가장 큰 고유값이 PC1인가?

공분산 행렬의 고유값은 해당 고유벡터 방향의 분산을 나타낸다. 따라서:

> 📌 가장 큰 고유값에 대응하는 고유벡터가 데이터의 분산을 가장 크게 만드는 방향이므로
> PC1이 된다.
{: .prompt-tip }

---

## 7. 🔗 고유값 · 고유벡터 함께 정렬

```python
sort_idx = np.argsort(eigenvalues)[::-1]

eigenvalues = eigenvalues[sort_idx]
eigenvectors = eigenvectors[:, sort_idx]
```

`np.linalg.eigh()` 결과는 PCA에서 원하는 큰 순서로 정렬되어 있다는 보장이 없으므로 직접
정렬한다.

### 중요한 점

고유값만 정렬하면 안 된다. `고유값 ↔ 고유벡터`는 서로 한 쌍이기 때문이다. 따라서 같은
`sort_idx`를 사용해

```python
eigenvalues[sort_idx]
eigenvectors[:, sort_idx]
```

둘 다 같이 정렬해야 한다.

> ⚠️ **기억** · 고유값과 고유벡터의 대응 관계를 절대 깨면 안 된다.
{: .prompt-warning }

---

## 8. 📈 설명분산비

```python
explained_ratio = eigenvalues / np.sum(eigenvalues)
```

각 고유값이 전체 고유값 합에서 차지하는 비율이다.

수식:

$$
\text{Explained Variance Ratio}_i
=
\frac{\lambda_i}
{\sum_j \lambda_j}
$$

예:

```text
PC1 → 68%
PC2 → 12%
PC3 → 10%
```

라면:

```text
PC1 하나만으로
전체 분산의 약 68% 설명

PC1 + PC2
약 80%

PC1 + PC2 + PC3
약 90%
```

이라는 뜻이다.

---

## 9. ➕ 누적 설명분산

```python
cumulative_ratio = np.cumsum(explained_ratio)
```

`np.cumsum()`은 앞에서부터 계속 더한다.

```text
explained_ratio
[0.50, 0.25, 0.15, 0.10]

↓

cumulative_ratio
[0.50, 0.75, 0.90, 1.00]
```

| 사용한 주성분 | 누적 설명분산 |
| --- | --- |
| PC1만 사용 | 50% |
| PC1~PC2 사용 | 75% |
| PC1~PC3 사용 | 90% |
| PC1~PC4 사용 | 100% |

---

## 10. 🎚️ `k_90`

```python
k_90 = np.argmax(cumulative_ratio >= 0.9) + 1
```

의 의미는 **누적 설명분산이 처음으로 90% 이상이 되는 최소 주성분 개수**를 구하는 것이다.

현재 결과가 예를 들어

```text
[0.6817,
 0.8023,
 0.9075,
 ...]
```

라면:

```text
PC1 → 68%
PC2까지 → 80%
PC3까지 → 90.7%
```

이므로 `k_90 = 3`이다.

### 왜 `+1`을 하는가?

`np.argmax()`는 Python index를 반환한다. `첫 번째 True 위치 index = 2`라면 사람 기준으로는
`3번째 주성분`이므로 `+ 1`이 필요하다.

> ⚠️ **기억** · index 2 ≠ 주성분 개수 2 — index 2 → 세 번째 위치 → k=3
{: .prompt-warning }

---

## 11. 🧩 `components`

```python
components = eigenvectors[:, :int(k_90)]
```

`components`는 설명분산비 자체가 아니다. **선택된 상위 주성분에 대응하는 고유벡터들**이다.

`k_90 = 3`이면:

```text
eigenvectors : (6, 6)

↓

앞 3개 열 선택

↓

components : (6, 3)
```

각 열은 다음을 의미한다.

```text
첫 번째 열 → PC1
두 번째 열 → PC2
세 번째 열 → PC3
```

---

## 12. 📐 PCA 투영

```python
projected_embeddings = centered_embeddings @ components
```

Shape:

```text
centered_embeddings : (12, 6)

components          : (6, 3)

            @

projected_embeddings: (12, 3)
```

즉:

```text
원래
12개 문서 × 6차원

↓

PCA

↓

12개 문서 × 3차원
```

으로 차원이 줄어든다.

### 의미

각 문서를 기존 6개 축이 아니라 `PC1`, `PC2`, `PC3`이라는 새로운 좌표축으로 표현하는 것이다.

---

## 13. ♻️ PCA 복원

```python
reconstructed_pca = (
    projected_embeddings @ components.T
    + embedding_mean
)
```

먼저

```text
projected_embeddings : (12, 3)

components.T         : (3, 6)

↓

(12, 3) @ (3, 6)

↓

(12, 6)
```

으로 다시 원래 6차원으로 펼친다.

### 왜 `.T`를 사용하는가?

투영할 때 `6차원 → 3차원`으로 변환했으므로, 복원할 때는 `3차원 → 6차원`으로 다시 변환해야
한다. 따라서 `components.T`를 사용한다.

### 왜 평균을 다시 더하는가?

처음에

```python
centered_embeddings
=
document_embeddings - embedding_mean
```

으로 평균을 뺐다. 따라서 마지막에는 `+ embedding_mean`을 해야 원래 좌표계로 돌아간다.

> 💡 **기억** · 평균을 뺐으면 복원할 때 다시 더한다.
{: .prompt-info }

---

## 14. 🕳️ 복원이 완벽하지 않은 이유

원래는 6개의 주성분이 있는데

```text
PC1
PC2
PC3
PC4
PC5
PC6
```

중 `PC1`, `PC2`, `PC3`만 사용했다. 즉 `PC4~PC6의 정보는 버림`이다.

따라서 다시 6차원으로 복원해도 원본과 완전히 같지는 않다.

---

## 15. 📉 재구성 MSE

```python
pca_reconstruction_mse = np.mean(
    (document_embeddings - reconstructed_pca) ** 2
)
```

MSE:

$$
MSE
=
\frac{1}{N}
\sum
(원본-복원값)^2
$$

**PCA로 압축했다가 복원했을 때 원본과 얼마나 달라졌는지 측정하는 값**이다.

```text
MSE 작음
→ 원본과 복원값이 비슷함
→ 정보 손실이 적음

MSE 큼
→ 복원 오차 큼
→ 정보 손실이 큼
```

### MSE에서 제곱을 먼저 해야 한다

| | 코드 | 계산 |
| --- | --- | --- |
| 정답 | `np.mean((원본 - 복원) ** 2)` | `mean(error²)` |
| 잘못된 형태 | `np.mean(원본 - 복원) ** 2` | `mean(error)²` |

---

## 16. 📋 `pca_table`

```python
pca_table = pd.DataFrame({
    "component": np.arange(1, len(eigenvalues) + 1),
    "eigenvalue": eigenvalues,
    "explained_ratio": explained_ratio,
    "cumulative_ratio": cumulative_ratio,
})
```

각 주성분별로

```text
PC 번호
고유값
설명분산비
누적 설명분산
```

을 한눈에 확인하기 위한 표다.

---

## 17. 📈 누적 설명분산 그래프

```python
plt.plot(
    np.arange(1, len(cumulative_ratio) + 1),
    cumulative_ratio
)
```

이 그래프는 **주성분을 몇 개까지 사용했을 때 전체 정보를 얼마나 보존하는지** 확인하기 위한
그래프다.

| 코드 | 의미 |
| --- | --- |
| `plt.axhline(y=0.90)` | 가로선 → 목표 설명분산 90% |
| `plt.axvline(x=k_90)` | 세로선 → 90%를 처음 만족하는 최소 주성분 개수 |

---

## 18. 🔵 PC1 · PC2 산점도

```python
plt.scatter(
    projected_embeddings[:, 0],
    projected_embeddings[:, 1]
)
```

의 의미:

```text
x축 → PC1
y축 → PC2
```

각 점은 하나의 문서를 의미한다. 즉 원래 6차원 데이터를 `PC1`, `PC2` 두 축만 사용해 시각적으로
표현하는 것이다.

---

## 19. 📏 Shape 흐름

이번 문제에서 가장 중요하게 기억해야 할 Shape이다.

```text
document_embeddings
(12, 6)

↓

평균 중심화

centered_embeddings
(12, 6)

↓

공분산

covariance
(6, 6)

↓

고유값 / 고유벡터

eigenvalues
(6,)

eigenvectors
(6, 6)

↓

상위 3개 고유벡터

components
(6, 3)

↓

PCA 투영

projected_embeddings
(12, 3)

↓

복원

reconstructed_pca
(12, 6)
```

---

## 20. ⚠️ 꼭 구분해야 할 개념

| 구분 | 왼쪽 | 오른쪽 |
| --- | --- | --- |
| 고유값 ≠ 고유벡터 | 고유값 → 해당 방향의 분산 크기 | 고유벡터 → 실제 방향 |
| 설명분산비 ≠ components | `explained_ratio` → 각 주성분이 전체 분산의 몇 %를 담당하는지 | `components` → 실제 선택된 주성분 방향(고유벡터) |
| `k_90` ≠ index | index = 2 → 세 번째 위치 | `k_90` = 3 → 주성분 3개 사용 |
| 투영 ≠ 복원 | 투영 → 6차원 → 3차원 | 복원 → 3차원 → 6차원 |

---

## 21. 🔗 PCA에서 반드시 기억해야 할 연결

```text
평균 중심화
→ 데이터의 중심을 0으로 이동

공분산 행렬
→ 데이터의 퍼짐과 변수 간 관계 표현

고유벡터
→ 데이터가 퍼지는 주요 방향

고유값
→ 각 방향의 분산 크기

설명분산비
→ 각 방향이 전체 분산의 몇 %인지

누적 설명분산
→ 앞에서부터 몇 개를 썼을 때 얼마나 보존되는지

k_90
→ 90% 이상 보존하는 최소 차원

Projection
→ 원래 차원을 PCA 차원으로 축소

Reconstruction
→ 축소 데이터를 다시 원래 차원으로 복원

MSE
→ 복원 과정의 정보 손실 측정
```

---

## 22. 🐍 핵심 Python 문법

| 목적 | 코드 |
| --- | --- |
| 열별 평균 | `np.mean(data, axis=0)` |
| Shape 변경 | `.reshape(1, 6)` |
| 공분산 | `np.cov(data, rowvar=False, ddof=1)` |
| 대칭행렬 고유값 분해 | `np.linalg.eigh(matrix)` |
| 내림차순 index | `np.argsort(values)[::-1]` |
| 누적합 | `np.cumsum(values)` |
| 첫 번째 조건 만족 위치 | `np.argmax(condition)` |
| 앞쪽 열 선택 | `matrix[:, :k]` |
| 전치 행렬 | `matrix.T` |

---

## 23. ✅ 최종 한 줄 요약

> 💡 **PCA는 평균 중심화된 데이터의 공분산 행렬을 고유값 분해하여 분산이 큰 방향부터
> 주성분으로 선택하고, 필요한 설명분산을 유지하는 최소 차원으로 투영함으로써 정보 손실을
> 최소화하며 차원을 줄이는 방법이다.**
{: .prompt-info }

---

## 24. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **PCA** : 데이터가 가장 많이 퍼져 있는 방향을 새 축으로 찾아 정보는 유지하면서 차원을 줄이는 방법
- **평균 중심화** : 데이터의 중심을 0으로 이동 — 절대 위치가 아니라 평균 기준 퍼짐이 중요하기 때문
- **공분산 행렬** : 각 차원이 서로 어떻게 함께 변하는지 — 대각선에는 각 변수의 분산
- **`rowvar=False`** : 행 = 데이터 샘플, 열 = 변수/차원으로 해석
- **`ddof=1`** : 표본 공분산 — 분모를 `N`이 아니라 `N - 1`로 사용
- **`np.linalg.eigh()`** : 공분산 행렬이 대칭행렬이므로 사용
- **고유벡터** : 데이터가 퍼져 있는 새로운 방향 = 주성분 방향
- **고유값** : 그 고유벡터 방향으로 투영했을 때의 분산 크기 — 크면 정보가 많음
- **PC1인 이유** : 가장 큰 고유값의 고유벡터가 분산을 가장 크게 만드는 방향
- **정렬 주의** : 고유값과 고유벡터는 한 쌍 — 같은 `sort_idx`로 `eigenvalues[sort_idx]`, `eigenvectors[:, sort_idx]` 둘 다 정렬
- **설명분산비** : $\lambda_i / \sum_j \lambda_j$ — 각 고유값이 전체 합에서 차지하는 비율
- **누적 설명분산** : `np.cumsum()` — 앞에서부터 몇 개 썼을 때 얼마나 보존되는지
- **`k_90`** : `np.argmax(cumulative_ratio >= 0.9) + 1` — 90%를 처음 넘는 최소 주성분 개수, index 2 → k=3이라 `+1` 필요
- **`components`** : 설명분산비가 아니라 선택된 상위 고유벡터들 — `(6, 6)` → 앞 3열 → `(6, 3)`
- **투영** : `centered @ components` → `(12, 6) @ (6, 3)` = `(12, 3)`
- **복원** : `projected @ components.T + embedding_mean` → `(12, 3) @ (3, 6)` = `(12, 6)`, 뺀 평균은 다시 더한다
- **완벽 복원 불가** : PC4~PC6 정보를 버렸기 때문
- **재구성 MSE** : `np.mean((원본 - 복원) ** 2)` — 제곱을 먼저, `np.mean(...) ** 2`는 틀림
- **Shape 흐름** : `(12,6)` → 중심화 `(12,6)` → 공분산 `(6,6)` → 고유벡터 `(6,6)` → components `(6,3)` → 투영 `(12,3)` → 복원 `(12,6)`

</details>

---

## 25. 🔗 관련 글

- [Projection과 Cosine Similarity 핵심 정리](/posts/projection-and-cosine-similarity/)
- [벡터 기초 — 정의부터 정규화까지](/posts/vector-basics/)
- [MSELoss 이해하기 — 차이, 제곱, 평균](/posts/mse-loss/)
