---
title: "Qdrant의 Point 구조와 저장·조회 흐름"
date: 2026-10-21 16:41:09 +0900
categories: [Notes, Deep Learning]
tags: [rag, qdrant, embedding, upsert]
---

> 🗂️ **Notes · Deep Learning** — `rag` `qdrant` `embedding` `upsert`
{: .prompt-info }

## 1. 📖 개요

RAG 3일차 오전 5-1에서 다룬 **청크와 벡터를 Point로 연결하고, Qdrant에 저장한 뒤 ID로
조회하는 흐름**을 정리한다.

> 📌 **이 단계의 목적** · 이후 질문 검색과 답변에 사용할 원문·출처를 벡터와 함께 준비한다.
{: .prompt-tip }

## 2. 🧩 청크와 벡터를 Point로 연결하기

청크 목록과 임베딩 행렬은 **같은 순서**여야 한다. `travel` 청크의 위치를 찾고,
같은 위치의 벡터를 가져와 짝짓는다.

```python
chunk = chunks[number]
vector = vectors[number]
```

`PointStruct`는 다음 세 가지를 하나의 Point로 묶는다.

| 구성 | 역할 |
| --- | --- |
| `id` | Point를 구분하는 고유 식별자 |
| `vector` | 검색용 벡터 |
| `payload` | 원문과 출처를 담은 데이터 |

벡터는 검색에 사용하고, 함께 저장한 원문과 출처는 이후 답변의 근거로 사용한다.

> 📌 **기억** · 같은 원문에서 나온 청크와 벡터를 짝지어, 원문·출처와 함께 저장한다.
{: .prompt-tip }

## 3. 🗂️ Collection 생성과 Upsert

`create_collection`은 Point를 저장할 컬렉션을 만들고, **벡터 차원과 비교 방식**을 설정한다.
실습에서는 벡터 차원을 `vectors.shape[1]`로 지정하고, 비교 방식은 코사인으로 설정한다.

이번 실습은 `QdrantClient(":memory:")`를 사용하므로 메모리에 임시로 저장한다.

### 같은 청크에 같은 ID 만들기

`uuid5()`는 같은 네임스페이스와 같은 `chunk_id`에 항상 같은 ID를 만든다.

```python
point_id = str(uuid5(NAMESPACE_URL, chunk["chunk_id"]))
```

### ID를 기준으로 등록하거나 갱신하기

```python
client.upsert("point_demo", points=[point], wait=True)
```

`upsert`는 ID가 없으면 등록하고, 이미 있으면 해당 Point를 갱신한다.
같은 ID로 두 번 등록해도 Point 수는 하나로 유지된다.

> 📌 **기억** · Collection은 저장할 공간, Upsert는 ID를 기준으로 등록하거나 갱신하는 동작이다.
{: .prompt-tip }

## 4. 🔎 Point ID로 조회하기

`retrieve`는 **정확한 `point_id`로 저장된 Point를 읽는다.**

```python
saved = client.retrieve(
    "point_demo",
    ids=[point_id],
    with_payload=True,
)[0]
```

`with_payload=True`로 원문과 메타데이터를 함께 가져와 문서 ID, 제목, 청크의 시작·끝 위치를
확인한다.

질문 벡터로 관련 문서를 찾는 과정은 다음 단계인 5-2에서 이어진다. 5-1에서는 저장한 자료를
ID로 조회한다.

> 📌 **기억** · `retrieve`는 지정한 ID의 자료를 읽는 조회이며, 질문에 필요한 문서를 찾는 검색은
> 다음 단계다.
{: .prompt-tip }

## 5. ✅ 핵심 정리

```text
청크와 벡터 짝짓기 → Point 구성 → Collection 생성 → Upsert → ID로 조회
```

- **PointStruct**: ID, 검색용 벡터, 원문·출처를 하나의 Point로 묶는다.
- **create_collection**: Point를 저장할 컬렉션과 벡터 설정을 만든다.
- **upsert**: ID를 기준으로 등록하거나 갱신한다.
- **retrieve**: 지정한 Point ID로 저장된 자료를 조회한다.

## 6. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **청크와 벡터의 순서**: 같은 원문을 가리키도록 같은 위치에서 가져온다.
- **UUID5와 Upsert**: 같은 입력으로 만든 같은 ID를 사용하면 기존 Point가 갱신된다.
- **임시 저장**: 이번 실습이 임시 저장인 이유는 `":memory:"` 모드를 사용하기 때문이다.
- **조회와 검색**: 5-1은 ID 조회, 5-2는 질문 벡터를 사용하는 검색으로 이어진다.

</details>

## 참고

- RAG 3일차 오전 5장 강의자료 — 5-1 Vector Store와 Qdrant 데이터 모델

## 관련 글

- [RAG 청킹에서 임베딩과 코사인 유사도까지](/posts/rag-chunking-embedding-cosine-similarity/)
- [Chunk와 Overlap — 문서를 나누는 기준 이해하기](/posts/chunk-and-overlap/)
