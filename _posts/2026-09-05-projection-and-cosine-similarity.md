---
title: "Projection과 Cosine Similarity 핵심 정리"
date: 2026-09-05 09:00:00 +0900
categories: [Notes, Math]
tags: [linear-algebra, projection, cosine-similarity, normalization, assignment]
math: true
---

> 🗂️ **Notes · Math** — `linear-algebra` `projection` `cosine-similarity` `normalization` `assignment`
{: .prompt-info }

> 📌 기초수학 과제 — 문제 (1) 개념 복습 정리
{: .prompt-tip }

---

## 1. 🔄 전체 흐름

```text
문서 특징 벡터 (8차원)
        ↓
Linear Projection
        ↓
문서 임베딩 (6차원)
        ↓
L2 정규화
        ↓
Query와 내적
        ↓
Cosine Similarity
        ↓
유사도가 높은 문서 Top-3 검색
```

핵심은 **문서와 Query를 같은 임베딩 공간으로 변환한 뒤, 방향이 얼마나 비슷한지 비교하는
것**이다.

---

## 2. 📐 Linear Projection

```python
document_embeddings = document_features @ projection_matrix + projection_bias
```

수식:

$$
Z = XW + b
$$

Shape:

```text
document_features   : (12, 8)
projection_matrix   : (8, 6)

(12, 8) @ (8, 6)
        ↓
     (12, 6)

+ projection_bias (6,)
        ↓
document_embeddings : (12, 6)
```

### 의미

기존 **8차원 특징 벡터를 새로운 6차원 임베딩 공간으로 변환**한다.

Query도 반드시 같은 Projection을 사용한다.

```python
query_embedding = query_features @ projection_matrix + projection_bias
```

그래야 문서와 Query를 같은 공간에서 비교할 수 있다.

> 💡 **기억** · 검색 대상과 검색 Query는 반드시 같은 임베딩 공간에 있어야 한다.
{: .prompt-info }

---

## 3. 🔍 행렬곱도 결국 내적의 반복이다

```python
first_component_by_dot = (
    document_features[0]
    @ projection_matrix[:, 0]
    + projection_bias[0]
)
```

첫 번째 문서의 첫 번째 임베딩 값을 직접 계산하면:

```text
문서의 8개 특징
      ·
Projection Matrix의 첫 번째 열
      +
첫 번째 bias
```

가 된다. 즉 `X @ W`라는 행렬곱도 내부적으로는 **여러 개의 벡터 내적을 한꺼번에 수행하는
것**이다.

> 💡 **기억** · 행렬곱 = 여러 내적을 묶어서 계산하는 연산.
{: .prompt-info }

---

## 4. 📏 L2 Norm

벡터

$$
x = [x_1,x_2,\dots,x_n]
$$

의 L2 Norm은 벡터의 **길이(크기)** 이다.

$$
||x||_2 =
\sqrt{x_1^2+x_2^2+\cdots+x_n^2}
$$

NumPy:

```python
np.linalg.norm(vector)
```

행렬의 각 행별 norm:

```python
np.linalg.norm(matrix, axis=1, keepdims=True)
```

| 인자 | 의미 |
| --- | --- |
| `axis=1` | 각 **행(row)** 마다 계산한다 |
| `keepdims=True` | 결과 차원을 유지한다 |

```text
matrix        : (12, 6)

axis=1
keepdims=True
        ↓

norm_matrix   : (12, 1)
```

그래야 `(12,6) / (12,1)` broadcasting이 가능하다.

---

## 5. 🎯 L2 Normalization

```python
matrix / norm_matrix
```

수식:

$$
\hat{x} = \frac{x}{||x||}
$$

L2 정규화는 벡터를 **길이 1인 벡터로 만드는 과정**이다.

중요한 점은:

```text
벡터의 방향 → 유지
벡터의 크기 → 1로 변경
```

예:

```text
[3, 4]

L2 Norm = 5

정규화
→ [3/5, 4/5]
→ [0.6, 0.8]
```

정규화된 벡터의 norm은 `1`이 된다.

> 💡 **기억** · L2 정규화는 방향은 유지하고 크기만 제거한다.
{: .prompt-info }

---

## 6. 🤔 왜 L2 정규화를 하는가?

일반 내적

$$
A \cdot B
$$

은 두 가지 영향을 동시에 받는다.

```text
1. 두 벡터의 방향
2. 두 벡터의 크기(norm)
```

따라서 벡터의 크기가 매우 크면 방향이 덜 비슷하더라도 내적 점수가 커질 수 있다.

문서 검색에서는 보통 **벡터 크기보다 Query와 문서가 얼마나 같은 방향을 바라보는가**가 더
중요하다. 그래서 L2 정규화를 통해 크기의 영향을 제거한다.

---

## 7. 📖 Cosine Similarity

$$
\cos(\theta)
=
\frac{A\cdot B}
{||A||\,||B||}
$$

두 벡터의 **방향 유사도**를 측정한다.

대략적인 해석:

| 값 | 의미 |
| :---: | --- |
| `1` | 매우 같은 방향 |
| `0` | 서로 관계없는 방향 |
| `-1` | 정반대 방향 |

---

## 8. ✨ L2 정규화 후 내적 = Cosine Similarity

문서와 Query를 모두 L2 정규화하면:

$$
||\hat{A}||=1
$$

$$
||\hat{B}||=1
$$

따라서:

$$
\cos(\theta)
=
\frac{\hat{A}\cdot\hat{B}}
{1\times1}
$$

즉:

$$
\boxed{
\cos(\theta)=\hat{A}\cdot\hat{B}
}
$$

그래서 코드가 단순하게

```python
cosine_scores = normalized_documents @ normalized_query
```

가 된다.

Shape:

```text
normalized_documents : (12, 6)
normalized_query     : (6,)

(12, 6) @ (6,)
        ↓
      (12,)
```

문서 12개 각각에 대한 Cosine Similarity 점수 12개가 나온다.

> 📌 **핵심** · 정규화된 벡터끼리는 내적 자체가 Cosine Similarity이다.
{: .prompt-tip }

---

## 9. 🧮 `np.argsort()`와 Top-K 검색

```python
np.argsort(cosine_scores)
```

값 자체를 정렬하는 것이 아니라 **정렬했을 때의 인덱스 순서**를 반환한다. 기본은
오름차순이다.

```python
np.argsort(cosine_scores)[::-1]
```

`[::-1]`을 이용해 순서를 뒤집으면 내림차순이 된다. 그리고 `[:3]`을 사용하면 상위 3개만
선택한다.

따라서:

```python
top3_indices = np.argsort(cosine_scores)[::-1][:3]
```

의 의미는:

```text
Cosine 점수 정렬
→ 높은 순서로 뒤집기
→ 상위 3개의 문서 index 선택
```

이다.

---

## 10. 🐍 리스트 컴프리헨션

```python
top3_titles = [
    document_titles[i]
    for i in top3_indices
]
```

의미:

```text
top3_indices의 각 i를 순회하면서
document_titles[i]를 가져와
새로운 리스트 생성
```

일반 for문으로 쓰면 다음과 같다.

```python
top3_titles = []

for i in top3_indices:
    top3_titles.append(document_titles[i])
```

---

## 11. 📡 Broadcasting

다음 연산

```python
document_features @ projection_matrix + projection_bias
```

에서

```text
행렬 결과         : (12, 6)
projection_bias   : (6,)
```

이지만 NumPy는 `(6,)`을 각 행에 자동으로 적용한다.

개념적으로:

```text
(6,)
↓
(1,6)
↓
12개 행에 반복 적용
↓
(12,6)
```

이것이 **Broadcasting**이다.

같은 원리로

```python
matrix / norm_matrix
```

에서

```text
matrix      : (12,6)
norm_matrix : (12,1)
```

도 각 행의 norm이 해당 행 전체에 자동 적용된다.

---

## 12. 🛡️ `eps=1e-12`를 넣는 이유

```python
matrix / (norm_matrix + eps)
```

`eps`는 아주 작은 값이다. 벡터가 전부 0이면 `norm = 0`이 될 수 있고, `vector / 0`은 계산
오류를 발생시킨다.

따라서 `norm + 1e-12`처럼 아주 작은 값을 더해 **0으로 나누는 문제를 방지**한다.

> ⚠️ `eps` = 수치적 안정성을 위한 안전장치.
{: .prompt-warning }

---

## 13. 🔗 꼭 기억해야 할 핵심 연결

```text
Projection
8차원 → 6차원 임베딩 공간으로 변환

        ↓

L2 Norm
벡터의 길이 측정

        ↓

L2 Normalization
벡터의 길이를 1로 만듦

        ↓

Normalized Dot Product
크기 영향 제거

        ↓

Cosine Similarity
방향 유사도 측정

        ↓

argsort
점수가 높은 문서 순위 결정
```

---

## 14. ⚠️ 헷갈리기 쉬운 부분

### Norm ≠ Normalization

| 용어 | 의미 |
| --- | --- |
| Norm | 벡터의 길이를 구하는 것 |
| Normalization | 그 길이로 벡터를 나누어 길이를 1로 만드는 것 |

### Dot Product ≠ 항상 Cosine Similarity

일반적으로:

$$
A\cdot B
\neq
CosineSimilarity
$$

하지만 두 벡터가 L2 정규화되어 있다면:

$$
\boxed{
A\cdot B
=
CosineSimilarity
}
$$

### Projection과 Cosine Similarity는 역할이 다르다

| 연산 | 역할 |
| --- | --- |
| Projection | 벡터를 새로운 공간으로 변환 |
| Cosine Similarity | 변환된 두 벡터가 얼마나 비슷한지 비교 |

Projection 자체를 Cosine Similarity로 대체하는 것이 아니다.

---

## 15. ✅ 최종 한 줄 요약

> 💡 **문서와 Query를 같은 임베딩 공간으로 Projection한 뒤 L2 정규화하여 크기 영향을
> 제거하고, 정규화된 내적으로 Cosine Similarity를 계산해 가장 방향이 비슷한 문서를
> 검색한다.**
{: .prompt-info }

---

## 16. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **Linear Projection** : $Z = XW + b$ — 8차원 특징 벡터를 6차원 임베딩 공간으로 변환
- **같은 공간 원칙** : 검색 대상과 검색 Query는 반드시 같은 Projection을 써야 비교 가능
- **행렬곱** : `X @ W`는 여러 개의 벡터 내적을 한꺼번에 수행하는 연산
- **L2 Norm** : 벡터의 길이 — $\sqrt{x_1^2+\cdots+x_n^2}$, `np.linalg.norm()`
- **`axis=1, keepdims=True`** : 행별 norm을 `(12, 1)`로 유지해 `(12,6) / (12,1)` broadcasting 가능
- **L2 Normalization** : $\hat{x} = x / ||x||$ — 방향은 유지, 크기만 1로 — `[3, 4]` → `[0.6, 0.8]`
- **정규화하는 이유** : 내적은 방향과 크기 둘 다에 영향받아, 크기가 크면 방향이 덜 비슷해도 점수가 커질 수 있음
- **Cosine Similarity** : $\cos(\theta) = A\cdot B / (||A||\,||B||)$ — 방향 유사도, `1` 같은 방향 / `0` 무관 / `-1` 정반대
- **핵심 등식** : L2 정규화된 벡터끼리는 내적 자체가 Cosine Similarity
- **Top-K** : `np.argsort(scores)[::-1][:3]` — 인덱스 정렬 → 내림차순 뒤집기 → 상위 3개
- **Broadcasting** : `(6,)` bias가 `(1,6)` → 12개 행에 반복 적용되어 `(12,6)`에 더해짐
- **`eps=1e-12`** : norm이 0일 때 0으로 나누는 오류를 막는 수치적 안정성 안전장치
- **Norm ≠ Normalization** : 길이를 구하는 것 vs 그 길이로 나눠 1로 만드는 것
- **Projection ≠ Cosine Similarity** : 공간 변환 vs 변환된 두 벡터의 비교 — 서로 대체 관계가 아님

</details>

---

## 17. 🔗 관련 글

- [벡터 기초 — 정의부터 정규화까지](/posts/vector-basics/)
- [PCA와 고유값 분해 핵심 정리](/posts/pca-and-eigen-decomposition/)
- [Batch dimension과 broadcasting](/posts/batch-dimension-and-broadcasting/)
