---
title: "Qdrant로 질문 검색하기 — 필터와 검색 결과 정리"
date: 2026-10-21 17:36:39 +0900
categories: [Notes, Deep Learning]
tags: [rag, qdrant, embedding, python]
---

> 🗂️ **Notes · Deep Learning** — `rag` `qdrant` `embedding` `python`
{: .prompt-info }

## 1. 📖 개요

RAG 3일차 오전 5-2에서 다룬 **질문 벡터로 관련 청크를 검색하고, 원문과 점수를 정리하는
흐름**을 질문했던 코드와 함께 정리한다.

Upsert 후 `points[0].id`로 첫 Point를 다시 읽는 부분은 저장 내용이 예상과 맞는지 확인하는
용도다. 첫 Point를 고른 것은 하나를 간단히 확인하려는 것이며, 검색에 반드시 필요한 단계는 아니다.

## 2. 질문 임베딩과 검색 준비

- 5-2는 **질문을 벡터로 바꿔, 저장된 청크 중 의미가 비슷한 청크를 찾는 단계**다.
- 청크 28개와 각 384차원 벡터를 저장한다면 행렬 모양은 `(28, 384)`다. Collection의 `size`는 Point 개수 28이 아니라 벡터 하나의 차원인 384다.
- 임베딩은 자연어의 의미와 특징을 숫자 배열인 벡터로 표현하는 것이다. 문서와 질문을 같은 모델로 변환해 유사도를 비교한다.

```python
model = load_model()
question = "출장 숙박 비용 한도와 필요한 증빙은?"
query = model.encode(
    "query: " + question,
    normalize_embeddings=True,
)
```

- 이번 E5 실습은 문서에 `passage:`, 질문에 `query:` 접두사를 사용한다. `normalize_embeddings=True`는 벡터 길이를 1로 정규화한다.
- `query`에는 질문의 임베딩 벡터가 담긴다. 이번 모델의 `query.shape`는 `(384,)`다.

> 📌 **기억** · 같은 모델로 문서와 질문을 벡터화하고, 벡터의 유사도로 관련 청크를 찾는다.
{: .prompt-tip }

## 3. Metadata Filter와 must 조건

```python
current_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="metadata.status",
            match=models.MatchValue(value="current"),
        )
    ]
)
```

- `FieldCondition`은 확인할 필드와 조건을 정한다. `key="metadata.status"`는 payload의 `metadata` 안에 있는 `status`를 가리킨다.
- `MatchValue(value="current")`는 값이 정확히 `"current"`인 Point만 허용한다. 필터는 검색할 자료의 조건이다.
- `must`는 Qdrant가 정해 둔 옵션 이름이다. 목록 안의 조건들은 **AND로 묶여 모두 충족**해야 한다. 현재는 조건이 하나다.
- `current_filter`는 직접 정한 변수 이름이므로 바꿀 수 있다. `must`는 옵션 이름이므로 임의의 이름으로 바꾸지 않는다.
- 이 코드는 필터 객체를 만드는 부분이다. 검색할 때 `query_filter=current_filter`로 전달하면 적용된다.

> 📌 **기억** · must 목록의 모든 조건을 만족하는 Point만 검색 대상으로 허용한다.
{: .prompt-tip }

## 4. query_points와 Top-k 검색

```python
hits = client.query_points(
    collection,
    query=query.tolist(),
    limit=3,
    query_filter=current_filter,
    with_payload=True,
).points
```

- `collection`은 검색할 컬렉션 이름이다.
- `query.tolist()`는 **질문의 임베딩 벡터를 Python 리스트로 변환**한다.
- `limit=3`은 유사도 상위 Point를 최대 3개 반환한다는 뜻이다. 이번 실습에서는 청크 3개이며, 같은 문서의 청크가 여러 개 포함될 수 있다. 조건에 맞는 Point가 2개뿐이면 2개만 반환된다.
- `query_filter`는 검색 대상 Point의 조건이고, `with_payload=True`는 원문·출처 등도 함께 가져오는 설정이다.
- `query_points()`의 반환값은 응답 객체다. **`.points`는 그 안의 검색된 Point 목록을 꺼내는 속성**이며, 그 목록이 `hits`에 담긴다.
- `hits[0].id`는 첫 결과의 ID, `hits[0].score`는 유사도 점수, `hits[0].payload`는 원문·출처 등의 정보다.
- 교안의 식비·숙박비 복합 질문은 `k=1`일 때 합산 금지 규정만, `k=3`일 때 합산 금지와 두 비용의 한도까지 검색된다. 관련 청크 하나를 찾는 것과 질문 전체의 근거를 모으는 것은 다르다.
- 실습의 `SavedDenseIndex`는 Collection 생성, Upsert, 질문 벡터화와 검색 절차를 묶어둔 클래스다.

> 📌 **기억** · 응답의 points에서 결과 목록을 꺼내고, 필요한 근거가 충분한지는 payload의 원문으로 확인한다.
{: .prompt-tip }

## 5. rows로 결과 정리하기와 딕셔너리 펼치기

```python
rows = [{**hit.payload, "score": float(hit.score)} for hit in hits]
```

- `for hit in hits`는 검색 결과를 하나씩 꺼낸다.
- `**hit.payload`는 payload의 모든 키와 값을 **새 딕셔너리에 펼쳐 넣는 문법**이다.
- `"score": float(hit.score)`는 유사도 점수를 Python 실수형으로 변환해 `score` 항목으로 넣는다.
- 바깥쪽 `[...]`는 만들어진 딕셔너리들을 리스트로 모은다. 원본 payload는 그대로 유지된다.
- 이후 `rows[0]["text"]`로 원문을, `rows[0]["score"]`로 점수를 읽을 수 있다.

> 📌 **기억** · payload의 내용을 새 딕셔너리에 담고 score를 붙여, 다루기 쉬운 리스트로 정리한다.
{: .prompt-tip }

## 6. enumerate로 순번과 데이터 함께 받기

`for rank, row in enumerate(rows, 1):`는 rows를 순회하면서 각 데이터와 1부터 시작하는 순번을 함께 받는 반복문의 시작 부분이다.

- 첫 번째 반복: `rank = 1`, `row = rows[0]`
- 두 번째 반복: `rank = 2`, `row = rows[1]`
- 세 번째 반복: `rank = 3`, `row = rows[2]`
- `rank`는 순번, `row`는 해당 딕셔너리를 받는다. 리스트의 실제 인덱스는 그대로이며, 첫 데이터에 붙일 순번을 1로 정한 것이다.

> 📌 **기억** · enumerate는 순회하면서 데이터와 순번을 함께 꺼내며, 1은 시작 순번이다.
{: .prompt-tip }

5-2의 전체 흐름:

```text
청크·벡터 등록 → 질문 임베딩 → 필터와 Top-k로 검색
→ 응답의 points 목록 꺼내기 → payload와 score 정리 → 순번을 붙여 읽기
```

## 7. ✅ 핵심 정리

- 문서와 질문은 같은 모델로 임베딩한다. `query.tolist()`는 질문 벡터를 Python 리스트로 바꾼다.
- `must`의 조건은 모두 충족해야 하며, 필터는 검색할 자료의 조건을 정한다.
- `limit=3`은 Point를 최대 3개 가져온다는 뜻이다. 필요한 근거가 충분한지는 원문에서 확인한다.
- 응답의 `.points`에서 결과 목록을 꺼내고, payload에 score를 붙여 rows로 정리한다.
- `enumerate(rows, 1)`은 데이터와 1부터 시작하는 순번을 함께 제공한다.

## 8. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **임베딩**: 자연어의 의미와 특징을 숫자 배열인 벡터로 표현한다.
- **필터 이름**: `current_filter`는 변수 이름, `must`는 Qdrant가 정한 옵션 이름이다.
- **.points**: 응답 객체에 들어 있는 검색 결과 목록을 읽는 속성이다.
- **딕셔너리 펼치기**: `{**hit.payload, "score": float(hit.score)}`는 원문 정보와 점수를 담은 새 딕셔너리를 만든다.
- **순번과 인덱스**: 첫 순번이 1이어도 첫 데이터는 `rows[0]`이다.

</details>

## 참고

- RAG 3일차 오전 5장 강의자료 — 5-2 Collection 생성 / Upsert / Query

## 관련 글

- [Qdrant의 Point 구조와 저장·조회 흐름](/posts/qdrant-point-collection-upsert-retrieve/)
- [RAG 청킹에서 임베딩과 코사인 유사도까지](/posts/rag-chunking-embedding-cosine-similarity/)
