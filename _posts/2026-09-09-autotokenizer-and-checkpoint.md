---
title: "AutoTokenizer와 체크포인트 — 토크나이저를 맞춰야 하는 이유"
date: 2026-09-09 13:00:00 +0900
categories: [Notes, Deep Learning]
tags: [tokenizer, checkpoint, nlp, embedding, subword]
---

> 🗂️ **Notes · Deep Learning** — `tokenizer` `checkpoint` `nlp` `embedding` `subword`
{: .prompt-info }

---

## 1. 📖 AutoTokenizer는 무엇을 자동으로 해 주는가?

> 📌 **이 글의 범위** · 대화에서 직접 질문한 문장과 작성한 답변을 인용해 정리했습니다.
> 그림의 토큰과 숫자는 실제 실행 결과가 아닌 설명용 예시입니다.
{: .prompt-tip }

> ❓ "autotokenizer에 대해서 자세히 설명해줘."

AutoTokenizer는 사용할 모델의 체크포인트를 보고, 그 모델에 맞는 토크나이저를 선택해 불러오는
클래스입니다. 먼저 세 가지를 구분하면 이해하기 쉽습니다.

| 이름 | 역할 |
| --- | --- |
| **토큰(Token)** | 텍스트를 처리하기 위해 나눈 단위. 반드시 한 글자나 한 단어인 것은 아님 |
| **토크나이저(Tokenizer)** | 텍스트를 토큰으로 나누고, 토큰을 숫자 ID로 바꾸는 도구 |
| **AutoTokenizer** | 모델에 맞는 토크나이저를 자동으로 선택해 불러오는 도구 |

토큰은 모델의 규칙에 따라 단어보다 작은 **서브워드(Subword)** 가 될 수도 있습니다. 여기서는
"띄어쓰기만 기준으로 자르는 것은 아니다"라고 기억하면 충분합니다.

> ⚠️ `Auto`는 **토크나이저 선택**을 자동으로 해 준다는 뜻입니다. 문장을 보고 가장 좋은 모델을
> 고르거나, 실행할 때마다 새로운 토큰 분리 규칙을 학습한다는 뜻은 아닙니다.
{: .prompt-warning }

```python
from transformers import AutoTokenizer

checkpoint = "google-bert/bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
```

| 코드 | 의미 |
| --- | --- |
| `from transformers import AutoTokenizer` | Transformers 라이브러리에서 클래스를 가져옴 |
| `checkpoint` | 불러올 모델 자료의 이름을 담은 변수 |
| `from_pretrained(checkpoint)` | 이미 준비된 어휘와 토큰 분리·특수 토큰 설정 등을 불러옴 |
| `tokenizer` | 이후 실제 텍스트를 처리하는 객체 |

**체크포인트(checkpoint)** 는 학습된 모델이나 관련 설정을 저장해 둔 묶음입니다. 이름 대신 로컬
저장 경로를 사용할 수도 있습니다. 위 호출은 토크나이저를 불러오며, 예측을 수행할 모델 가중치는
별도로 불러옵니다.

---

## 2. 🔗 모델과 토크나이저의 체크포인트를 맞추는 이유

> ❓ "Model과 tokenizer checkpoint를 맞춰야 하는 이유는 무엇인가요?"

모델은 학습할 때 특정한 토큰↔ID 대응 관계를 사용합니다. 토크나이저가 만든 ID가 그 관계와
일치해야 합니다. 가령 A와 B의 어휘 사전이 다음처럼 다르다고 가정해 보겠습니다.

| 토큰 | A 토크나이저의 ID | B 토크나이저의 ID |
| --- | --- | --- |
| 제품 | 350 | 820 |
| 배송 | 820 | 350 |

A와 함께 학습한 모델에 `350`을 넣으면, 모델은 학습 당시 `제품`에 대응하던 임베딩을 참조합니다.
그런데 B로 `배송`을 변환해도 `350`이 나오므로, 이를 그대로 A 모델에 넣으면 서로 다른 내용을
같은 번호로 전달하게 됩니다.

![위쪽은 제품이 A 토크나이저를 거쳐 ID 350이 되고 A 모델에서 제품의 임베딩으로 맞게 연결되는 정상 경로, 아래쪽은 배송을 B 토크나이저가 같은 ID 350으로 바꿔 A 모델이 제품의 임베딩을 참조하게 되는 불일치 경로](/assets/img/posts/autotokenizer-and-checkpoint/checkpoint-mismatch.svg){: w="720" h="292" }

따라서 다음 약속이 모델의 학습 당시와 맞아야 합니다.

- 텍스트를 어떤 규칙으로 토큰으로 나누는가?
- 각 토큰은 어떤 ID에 대응하는가?
- 특수 토큰은 무엇이며, 어느 위치에 추가하는가?

여기서 특수 토큰은 문장 경계나 패딩 같은 역할을 표시하는 토큰입니다. 예를 들어 BERT는
`[CLS]`, `[SEP]`, `[PAD]` 등을 사용합니다. 모델마다 사용하는 종류와 규칙은 다릅니다.

> 💡 같은 체크포인트에서 모델과 토크나이저를 불러오는 것이 기본입니다. 본질적인 조건은 이름
> 문자열 자체가 아니라 **학습 당시의 토크나이저 규칙과 호환되는가**입니다. 다른 이름으로 저장된
> 파인튜닝 모델이라도 원래 토크나이저를 그대로 사용했다면 호환될 수 있습니다.
{: .prompt-info }

---

## 3. ⚙️ `tokenize()`와 `tokenizer(...)`는 무엇이 다른가?

> ❓ "tokenize()와 tokenizer(...)의 목적 차이는 무엇인가요?"

`tokenize()`는 나뉜 토큰을 확인할 때, `tokenizer(...)`는 모델 입력을 준비할 때 사용합니다.

```python
text = "This product is easy to use."

# 어떻게 나뉘었는지 토큰 문자열을 확인
tokens = tokenizer.tokenize(text)

# 숫자 ID와 모델이 요구하는 입력 정보를 생성
encoded = tokenizer(text)
```

| 비교 항목 | `tokenizer.tokenize(text)` | `tokenizer(text)` |
| --- | --- | --- |
| 주요 결과 | 토큰 문자열 리스트 | `input_ids` 등을 담은 딕셔너리처럼 접근 가능한 객체 |
| 주된 목적 | 토큰 분리 결과 관찰 | 실제 모델 입력 준비 |
| ID 변환 | 별도 메서드로 수행 | 함께 수행 |
| 모델용 특수 토큰 추가 | 이 단계만으로 입력 구성이 완성되지는 않음 | 모델 설정과 옵션에 따라 추가 |
| 패딩·잘라내기·텐서 변환 | 이 메서드의 주된 역할이 아님 | 옵션으로 지정 |

`tokenizer(text)`는 객체를 함수처럼 호출하는 파이썬 문법입니다. 텍스트 하나나 여러 개를 전달할
수 있습니다. 패딩은 기본적으로 자동 적용되는 것이 아니라 `padding` 옵션으로 요청합니다.

처리 과정을 나눠 확인할 때는 다음 메서드도 사용할 수 있습니다.

```python
# 분리한 토큰 문자열들을 ID로 변환
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# ID를 텍스트로 변환하되, 특수 토큰은 표시하지 않음
decoded_text = tokenizer.decode(token_ids, skip_special_tokens=True)
```

소문자 변환이나 공백 처리 등이 적용되었다면 `decode()`의 결과가 원본 문장과 완전히 같지는 않을
수 있습니다.

반환값의 대표적인 키는 다음과 같습니다.

| 키 | 담고 있는 정보 |
| --- | --- |
| `input_ids` | 입력 토큰을 정수 ID로 변환한 결과 |
| `attention_mask` | 패딩처럼 어텐션에서 참조하지 않을 위치를 구분하는 정보 |
| `token_type_ids` | BERT 같은 일부 모델에서 입력의 첫 번째·두 번째 문장 구간 등을 구분하는 정보 |

모든 모델이 위 키를 전부 사용하는 것은 아닙니다. 특히 `token_type_ids`는 반환되지 않는 경우가
있습니다.

### 토큰 ID는 임베딩 벡터와 다르다

`제품 → 350`이라면 `350`은 토큰을 가리키는 번호입니다. 이 숫자 자체가 `제품`의 의미를 담은
벡터는 아닙니다.

```text
토크나이저 → 토큰을 정수 ID로 변환
임베딩 층  → 각 ID에 대응하는 벡터를 가져옴
이후 층    → 벡터들을 처리하며 문맥을 반영
```

ID가 `820`이라고 해서 `350`보다 중요하거나 의미가 더 크다는 뜻은 아닙니다.

---

## 4. ✅ 내가 작성한 답변과 정확한 표현

질문 순서대로 직접 작성한 답변 중 이 글에 해당하는 것입니다.

1. 전자는 분할 관찰용 token 문자열, 후자는 batch와 mask를 포함한 실제 모델 입력 생성에
   적합합니다.
2. 같은 ID가 같은 token과 special token 규칙을 가리켜야 하기 때문입니다.

두 답변 모두 핵심을 이해한 답입니다. 복습할 때는 다음처럼 표현을 다듬어 기억하면 정확합니다.

| 항목 | 기억할 답변 |
| --- | --- |
| 두 호출의 목적 | `tokenize()`는 토큰 문자열 관찰, `tokenizer(...)`는 모델 입력 준비. 배치·패딩·텐서 변환은 입력과 옵션에 따라 적용 |
| 체크포인트 호환 | 토큰 분리, 토큰↔ID 매핑, 특수 토큰 규칙이 학습 당시와 일치해야 함 |

---

## 5. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **AutoTokenizer** : 체크포인트를 보고 그 모델에 맞는 토크나이저를 선택해 불러오는 클래스
- **`Auto`의 의미** : 토크나이저 **선택**이 자동 — 좋은 모델을 고르거나 분리 규칙을 학습하지 않는다
- **checkpoint** : 학습된 모델이나 관련 설정을 저장해 둔 묶음 — 로컬 경로도 가능
- **체크포인트를 맞추는 이유** : A에서 `제품=350`이어도 B에서는 `배송=350`일 수 있다
- **맞아야 하는 세 가지** : 토큰 분리 규칙 / 토큰↔ID 매핑 / 특수 토큰과 그 위치
- **본질적인 조건** : 이름 문자열이 아니라 **학습 당시 토크나이저 규칙과 호환되는가**
- **`tokenize()`** : 토큰 문자열 리스트 — 분리 결과 관찰용
- **`tokenizer(...)`** : `input_ids` 등을 담은 객체 — 실제 모델 입력 준비용
- **주요 키** : `input_ids` / `attention_mask` / `token_type_ids` (모두 반환되지는 않음)
- **ID ≠ 임베딩 벡터** : ID는 번호, 벡터는 임베딩 층이 가져온다 — 820이 350보다 중요하지 않다

</details>

---

## 6. 🔗 관련 글

- [패딩과 잘라내기, 그리고 shape — 여러 문장을 한 배치로 묶기](/posts/padding-truncation-and-shape/)
- [Token과 Vocabulary — 텍스트가 숫자가 되기까지](/posts/nlp-token-subword-vocabulary/)
- [Checkpoint 저장·복원·Resume와 최종 Test](/posts/checkpoint-save-load-resume/)
