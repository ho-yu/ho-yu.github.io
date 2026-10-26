---
title: "RAG 근거 구성과 검색 개선 — Context부터 RRF·재정렬까지"
date: 2026-10-26 17:11:37 +0900
categories: [Notes, Deep Learning]
tags: [rag, chunking, bm25, rrf, reranking]
---

> 🗂️ **Notes · Deep Learning** — `rag` `chunking` `bm25` `rrf` `reranking`
{: .prompt-info }

## 1. 📖 전체 흐름

![RAG의 질문·검색·근거 구성·생성과 검사 흐름](/assets/img/posts/rag-context-hybrid-retrieval-reranking/01-rag-flow.png)

**관련 문서를 찾았어도, 답이 담긴 구간을 모델에게 전달하지 못하면 답할 근거가 부족하다.**
이 글은 2026년 10월 26일 강의 질문과 학습일지에서 다룬 개념을 연결한 정리다. 실제 모델 실행이나 성능 측정을 완료했다는 기록은 아니다.

2-Step RAG의 큰 흐름은 **검색 → 생성**이다. 검색으로 찾은 자료를 생성 모델의 참고 자료인 **Context**에 담는다. 아래의 출처 검사·검색 개선 단계는 학습한 구성 예이며, 모든 RAG에 같은 함수와 단계를 강제하지 않는다. [RAG와 2-Step 구조](https://docs.langchain.com/oss/python/deepagents/retrieval)

## 2. 🧩 청크 크기·검색 개수·budget

![청크 크기는 한 조각의 길이, k는 검색 후보 수, budget은 참고 자료의 전체 허용량](/assets/img/posts/rag-context-hybrid-retrieval-reranking/02-chunk-k-budget.png)

청크는 문서를 나눈 구간이다. 문단·규정 항목처럼 의미가 이어지는 경계를 고려하고, 대상·조건이 잘리지 않는지 확인한다. [문서 분할과 문맥 보존](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents)

```python
for budget in [120, 200, 300]:
    context, sources = pack_context(
        unique, max_chars=budget
    )
    print(budget, "실제 길이", len(context))
```

위 숫자는 **교안의 문자 예산 비교 예시**다. `budget`은 답변을 담는 공간이 아니라 **모델이 읽을 참고 자료의 총량**이다.

- 교안의 `pack_context`는 청크를 요약하지 않는다. 공간에 들어가면 통째로 담고, 들어가지 않으면 다음 청크를 확인한다.
- 라벨·제목·구분자도 공간을 사용하므로 청크 본문 길이로만 개수를 계산하면 안 된다.
- 같은 문서의 다른 구간은 서로 다른 근거일 수 있다. 중복 제거는 `document_id` 대신 **`chunk_id`**를 기준으로 한다.
- 실제 서비스에서는 모델별 토큰 한도와 시스템 지시문·질문·대화 기록·출력 공간을 함께 고려한다.

설정은 실제 질문에서 정답 근거가 **검색됐는지 → Context에 담겼는지**를 나누어 확인하며 조절한다.

## 3. ⚙️ 답변 생성과 형식 검사

![prepare는 검색과 근거 준비, invoke_model은 초안 생성, finish는 검사와 출처 연결](/assets/img/posts/rag-context-hybrid-retrieval-reranking/03-rag-chain.png)

교안의 세 함수는 `state`라는 작업용 딕셔너리로 값을 이어받는다.

- `prepare`: `rows`, `context`, `sources` 준비.
- `invoke_model`: 모델 응답 초안 `draft` 생성.
- `finish`: 응답 검사와 출처 연결.

모델 응답은 `status`·`answer`·`citations` 같은 일정한 필드로 받을 수 있다. **JSON Schema는 양식을 제한하는 규칙**이다. 형식이 맞아도 답변의 사실성은 따로 확인해야 한다. [Ollama 구조화 출력](https://docs.ollama.com/capabilities/structured-outputs)

## 4. 🔎 출처가 문장의 의미를 지지하는가

![답변의 출처 ID와 원문 발췌를 연결하고 문장의 의미 유지를 확인하는 대응 관계](/assets/img/posts/rag-context-hybrid-retrieval-reranking/04-citation.png)

`S1`은 현재 요청에서 붙인 출처 라벨이다. 이번 요청의 `sources`로 실제 청크에 연결한다. 모델이 URL을 새로 쓰게 하기보다 저장된 출처 URL을 사용한다.

**예시:** “1박당 12만원”을 “출장 전체에 12만원”으로 바꾸면 숫자가 같아도 단위가 달라진다. 답변의 **대상·금액·단위·조건**을 원문과 비교해야 한다.

교안의 단순 검사에서:

- `extractive_match`: 답변 문장이 원문 발췌와 동일.
- `review_meaning`: 문장이 달라 의미 검토가 필요. 올바른 바꿔쓰기에도 발생.
- URL 형식 통과: 실제 접속 가능성까지 확인했다는 뜻은 아님.

출처의 존재, 답변 내용의 정확성, 질문을 빠짐없이 답했는지는 별도 문제다. [ALCE의 답변·인용 품질 평가](https://arxiv.org/abs/2305.14627)

## 5. 🛑 근거 부족·질문 모호성·오류

![근거 부족, 시스템 요청 실패, 응답 파싱 및 검사 실패의 구분](/assets/img/posts/rag-context-hybrid-retrieval-reranking/05-abstention.png)

국내 숙박 규정으로 해외 항공 좌석 등급을 추측해서 답할 수는 없다. 근거가 부족하면 **확인하지 못한 항목과 필요한 자료**를 구체적으로 알린다. 질문 대상이 모호하면 확인한다.

교안의 앱 상태는 다음처럼 구분한다.

| 상태 | 의미 |
| --- | --- |
| `insufficient` | 현재 근거로 답하기 어려움 |
| `system_error` | 서버 연결·HTTP 요청 실패 |
| `invalid_output` | 응답 파싱·검사 규칙 위반 |

상태명과 보류 시 빈 인용 배열을 쓰는 규칙은 교안의 설계다. **자료에 명시되지 않았다는 사실을 금지·불가로 단정하지 않는 것**이 중요하다.

## 6. 🔍 BM25와 Dense

![BM25는 토큰 일치, Dense는 각각 만든 임베딩 벡터 유사도를 사용](/assets/img/posts/rag-context-hybrid-retrieval-reranking/06-bm25-dense.png)

BM25는 토큰 일치에 **희소성(IDF)·등장 빈도의 포화·길이 보정**을 반영한다. Dense는 질문과 청크를 각각 임베딩해 벡터 유사도로 찾는다. [BM25 점수 구성](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity), [Bi-Encoder 검색](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

교안의 “영수증 / 영수증을 / 영수증으로”가 서로 달라 검색 결과가 비는 현상은 해당 토큰화 구현의 사례다. 모든 BM25에 같은 결과가 적용되는 것은 아니다.

두 검색 방식은 사용처가 고정되지 않는다. 대표 질문에서 정답 청크의 포함 여부·순위·최종 답변 품질·시간·비용을 비교해 하나를 고르거나 결합한다. **BM25의 8.3과 Dense의 0.9처럼 척도가 다른 점수로 승자를 고르면 안 된다.**

Dense 유사도도 정답 확률은 아니다. 관련 문서를 찾아도 실제 정답이 있는 청크는 상위 결과에서 빠질 수 있다.

## 7. 🔀 RRF: 순위 통합

![RRF는 양쪽 검색기의 순위 기여도를 합산하며 예시 상수는 60](/assets/img/posts/rag-context-hybrid-retrieval-reranking/07-rrf.png)

**Hybrid Search**는 여러 검색 방식을 함께 쓰는 것이고, **RRF**는 검색기의 순위를 공통 기여도로 바꾸어 합치는 방법이다.

```text
RRF(청크) = 각 검색기에서 받은 1 / (c + 순위)의 합
순위는 1부터 시작
```

같은 `chunk_id`에 대한 기여도를 더한다. 한 검색기에 없는 청크는 그 검색기에서 기여도가 없다. `c`는 순위별 차이를 조절하는 상수로, 후보 수나 budget이 아니다. [RRF 공식 수식](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)

RRF 점수는 정답 확률이 아니다. 두 검색기가 같은 무관한 청크를 높게 평가하면 그 청크도 올라갈 수 있다.

## 8. 📑 Re-ranking: 내용 재평가

![Bi-Encoder는 따로 인코딩하고 Cross-Encoder는 질문과 청크를 함께 읽어 쌍별 평가](/assets/img/posts/rag-context-hybrid-retrieval-reranking/08-reranking.png)

RRF가 **기존 순위**를 합친다면, Cross-Encoder는 **질문과 후보의 실제 내용**을 함께 읽고 관련성을 다시 평가한다.

```text
(질문, 후보 A) → 점수 A
(질문, 후보 B) → 점수 B
(질문, 후보 C) → 점수 C
              → 높은 점수부터 재정렬
```

Bi-Encoder는 문서 벡터를 미리 저장할 수 있다. Cross-Encoder는 질문과 후보의 쌍별 계산이 필요하므로 검색한 후보를 재평가하는 데 사용한다. 후보가 늘면 평가할 쌍도 늘어난다. [검색 후 재정렬](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

교안처럼 활성화 함수를 Identity로 두고 원시 logit을 받으면 음수도 나올 수 있다. 이를 확률로 읽으면 안 된다. 입력 길이 제한을 넘으면 질문·본문이 잘릴 수 있다. [CrossEncoder 입력·출력 설정](https://www.sbert.net/docs/package_reference/cross_encoder/model.html)

> **RRF와 재정렬 모두 입력 후보에 없는 정답 청크를 되살리지는 못한다.**
{: .prompt-tip }

## 9. ✏️ 검색 표현과 사용자 의도

![Rewrite는 표현 하나 대체, Multi-Query는 같은 의도 여러 표현, 질문 분해는 서로 다른 하위 질문](/assets/img/posts/rag-context-hybrid-retrieval-reranking/09-query-methods.png)

검색 표현은 문서의 용어와 맞추되, 사용자 의도를 유지한다. 확인하지 않은 금액이나 정답을 미리 넣지 않는다. [Query Rewriting 원 논문](https://arxiv.org/abs/2305.14283)

![여러 표현으로 각각 검색한 뒤 청크 중복을 제거하고 원질문으로 답변하는 흐름](/assets/img/posts/rag-context-hybrid-retrieval-reranking/10-multi-query.png)

같은 검색 문장의 중복 제거와 같은 청크의 중복 제거는 별개다. 여러 질의의 결과를 통합하되, **단순히 발견한 순서가 관련도 순위는 아니다.** 재정렬과 답변 생성에는 원질문을 사용한다. [Multi-Query와 결과 합집합](https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever)

변형 문장을 늘리면 검색 횟수가 늘고, LLM으로 만들면 호출도 추가된다. 무관한 후보가 섞일 수 있으므로 효과를 실제 질문들로 확인한다.

## 10. 🐍 검색 결과를 읽는 코드

### 검색 문장마다 결과 확인

```python
for q in variants:
    rows = bm25(q, current, k=3)
    print(f"rows : \n{rows}")
    print(q, [
        (r["document_id"], r["start"])
        for r in rows
    ])
```

사전 조건은 `variants`가 검색 문장 목록, `current`가 검색 대상 청크, `bm25`가 교안의 검색 함수라는 것이다.

매 반복의 `rows`는 이번 검색 결과로 덮어쓴다. 첫 출력은 전체 결과, 두 번째는 검색 문장과 **(문서 ID, 시작 위치)** 목록이다. 이 코드 자체는 결과를 누적하거나 중복 제거하지 않는다. [리스트 컴프리헨션](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

### 조건을 만족하는 첫 기록 꺼내기

![next는 조건에 맞는 첫 딕셔너리를 반환하고 기본값이 있으면 미발견 시 그 값을 반환](/assets/img/posts/rag-context-hybrid-retrieval-reranking/11-next-result.png)

```python
run = next(
    (r for r in runs
     if r["question_id"] == "q06"),
    None
)
```

`runs`는 `question_id` 키가 있는 검색 기록 목록이다. 조건에 맞는 **첫 딕셔너리 전체를 `run`에 저장**한다. 일치 항목이 없으면 위 코드는 `None`을 반환하고, 기본값을 생략하면 `StopIteration`이 발생한다. [next 공식 설명](https://docs.python.org/3/library/functions.html#next)

## 11. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **청크 크기:** 한 조각의 길이. **k:** 검색 후보 수. **budget:** 참고 자료 전체 허용량.
- **형식 통과 ≠ 내용 정확:** 원문의 대상·금액·단위·조건과 답변 누락을 확인한다.
- **BM25·Dense:** 다른 검색 단서를 사용한다. 점수는 직접 비교하지 않는다.
- **RRF:** 순위 통합. **Cross-Encoder:** 질문과 내용을 함께 읽고 재평가.
- **Multi-Query:** 같은 의도의 여러 표현으로 검색하고, 원질문을 기준으로 답한다.
- **최종 기준:** 답에 필요한 근거가 실제 Context에 남았는가?

</details>

## 참고

- [원문: 2026-10-26 노션 학습 노트](https://app.notion.com/p/404682609ddd81bbbb90e30b095fa1ce)
- 강의 자료: RAG 4일차 오전 6장·오후 7장. 교안의 구현 규칙과 실습 예시는 일반 법칙과 구분했다.
- [검색 평가: 정답 자료의 순위와 포함 여부](https://www.sbert.net/docs/package_reference/sentence_transformer/evaluation.html)

## 관련 글

- [RAG 청킹에서 임베딩과 코사인 유사도까지](/posts/rag-chunking-embedding-cosine-similarity/)
- [RAG 검색 범위와 청크 관리 — Qdrant 필터부터 BM25까지](/posts/rag-filter-chunk-management-bm25/)

