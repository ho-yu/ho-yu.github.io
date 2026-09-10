---
title: "동적 Padding과 Collator — PAD를 줄이는 길이 정책"
date: 2026-09-10 09:10:00 +0900
categories: [Notes, Deep Learning]
tags: [nlp, data-collator, tokenizer, attention-mask, tensor-shape]
---

> 🗂️ **Notes · Deep Learning** — `nlp` `data-collator` `tokenizer` `attention-mask` `tensor-shape`
{: .prompt-info }

---

## 1. 📖 들어가며

> 📌 **이 글의 범위** · "여기까지 리셋하고, 새로운 개념 학습 시작" 이후의 질문과 답변입니다.
> 예시의 길이는 글자 수가 아니라 토큰 수입니다.
{: .prompt-tip }

[Dataset split과 map() — 학습 데이터를 준비하는 흐름](/posts/dataset-split-and-map/)에서
데이터를 나누고 토큰화하는 데까지 정리했습니다. 그 단계에서는 `padding=False`로 두었는데,
이 글에서는 **왜 padding을 미루고 실제 학습 batch에서 길이를 맞추는지**를 이어서 정리합니다.

---

## 2. 📦 Padding은 왜 필요하고, 무엇이 비효율적인가?

> ❓ "autotokenizer에서 padding으로 전부 같은 길이로 만드는게 편하다고 했는데, 비효율적인 부분은
> 없는건지 알려줘."

길이가 다른 샘플을 일반적인 직사각형 Tensor로 묶기 위해 padding합니다. 한 batch 안에서 길이를
맞추면 여러 샘플을 한꺼번에 계산할 수 있습니다.

![문장 A·B·C의 토큰 길이가 3·5·8일 때 모두 최장 길이 8에 맞춰 PAD를 채우면 실제 토큰 16개에 Tensor 위치는 24개가 되고 그중 8개가 PAD가 되는 그림](/assets/img/posts/dynamic-padding-and-collator/padding-waste.svg){: w="720" h="260" }

실제 토큰은 16개인데 Tensor에는 24개 위치가 생깁니다. 그중 8개, 약 33.3%는 PAD입니다. 이 수치는
padding 위치의 비율이며, 전체 실행 시간의 낭비 비율과 정확히 같은 것은 아닙니다.

일반적인 밀집 Tensor 계산에서는 PAD 위치도 계산과 메모리 사용에 영향을 줍니다. 특히 기본
self-attention의 토큰 간 비교량은 길이 `L`에 대해 대략 `L²`으로 증가하여, 불필요하게 길이를
늘리면 부담이 커질 수 있습니다. 실제 메모리 사용은 구현에 따라 달라집니다.

문장을 하나씩 처리하면 PAD는 줄어도 batch 병렬 처리의 장점을 잃을 수 있습니다. 따라서 병렬
처리의 이점을 유지하면서 PAD를 줄이는 방향으로 조절합니다.

---

## 3. ⚖️ 동적 padding과 max_length는 어떻게 다른가?

> ❓ "그러면 max_length는 사용할일이 거의 없는거 아닌지? 무조건 동적 padding만 사용하는게 좋아
> 보이는데,"

동적 padding과 길이 상한은 함께 사용할 수 있습니다. 혼동하기 쉬운 것은 `max_length`와
`padding="max_length"`가 서로 다른 역할이라는 점입니다.

| 설정 | 역할 |
| --- | --- |
| `padding=True` | 현재 함께 전달된 문장 중 최장 길이에 맞춰 채움 |
| `truncation=True, max_length=128` | 128을 넘는 입력을 자름 |
| `padding="max_length", max_length=128` | 짧은 입력도 128까지 채움 |
| `padding=False` | Padding하지 않음 |

> ⚠️ `max_length`를 지정한 것만으로 자동으로 잘리는 것은 아닙니다. 위 설명에서는
> `truncation=True`를 함께 사용합니다.
{: .prompt-warning }

### 동일한 입력으로 비교하기

```python
tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=128,
)
```

| 원래 길이 | Truncation 후 | 동적 padding 후 |
| --- | --- | --- |
| `[10, 15, 20]` | `[10, 15, 20]` | `[20, 20, 20]` |
| `[10, 15, 200]` | `[10, 15, 128]` | `[128, 128, 128]` |

같은 입력 `[10, 15, 20]`에 `padding="max_length"`를 사용하면 모두 128까지 채워집니다.

> 💡 상한은 "얼마나 긴 입력까지 허용할지", 동적 padding은 "현재 batch를 어느 길이로 맞출지"를
> 결정합니다.
{: .prompt-info }

### 그렇다면 고정 길이 padding은 언제 쓰는가?

항상 같은 입력 shape가 필요한 실행 환경이나 고정 shape에 맞춰 최적화한 환경에서 사용할 수
있습니다. 데이터 길이가 원래 비슷하다면 PAD 낭비가 작을 수도 있습니다.

따라서 동적 padding이 일반적으로 PAD를 줄이는 데 유리하지만, 모든 환경에서 실행 속도까지 무조건
가장 빠르다고 단정할 수는 없습니다.

---

## 4. 📏 그런데 왜 하필 max_length=128인가?

> ❓ "문장길이가 [10, 15, 20] 이건데 왜 max_length가 128인지 이해할 수 있게 간단하게 설명해줘."
>
> ❓ "아니, 128이라고 설정한 기준이 있는건지 궁금해."

앞선 설명의 128은 예시 수치였습니다. `[10, 15, 20]`에서 계산되어 나온 값이 아닙니다. 직접 올린
코드의 `max_length=16`도 교육용 상한입니다. 실제로는 다음 기준을 보고 정합니다.

| 기준 | 확인할 내용 |
| --- | --- |
| 데이터 길이 | 이 길이 안에 샘플이 얼마나 들어오는가? |
| 정보 손실 | 잘리는 부분에 중요한 내용이 있는가? |
| 계산 자원 | 메모리와 처리 시간을 감당할 수 있는가? |
| 모델 제한 | 모델이 지원하는 입력 길이 안인가? |

예를 들어 가상의 길이 조사 결과가 다음과 같다고 하겠습니다.

![가상의 길이 조사에서 평균 35, 99% 샘플이 들어오는 길이 121, 최대 487일 때 max_length를 128로 두면 대부분을 보존하고 그보다 긴 구간만 잘리는 것을 보여주는 축 그림](/assets/img/posts/dynamic-padding-and-collator/length-policy.svg){: w="720" h="240" }

```text
평균 길이: 35
99%의 샘플이 들어오는 길이: 121
최대 길이: 487
```

이 경우 128을 후보로 정하면 대부분을 보존하면서 극단적으로 긴 일부 샘플을 제한할 수 있습니다.
다만 잘리는 내용의 중요성도 확인해야 합니다.

> ⚠️ 길이를 조사할 때는 **truncation하기 전의 토큰 길이**를 봐야 합니다. 이미 16에서 자른
> 데이터만 측정하면 원래 얼마나 길었는지 알 수 없습니다. 모델에 추가되는 특수 토큰도 입력 길이에
> 포함해 판단합니다.
{: .prompt-warning }

동적 padding을 사용한다면 현재 문장들이 `[10, 15, 20]`이어도 상한을 128로 둔 것 자체가 128까지의
padding 낭비를 만들지는 않습니다. 현재 batch는 여전히 20으로 맞춰집니다.

---

## 5. 🧺 Collator는 무엇이며, 왜 여기서 padding하는가?

> ❓ "그리고, collator는 뭔지 간단하게 알려줘"

Collator는 여러 샘플을 모델이 한 번에 처리할 batch로 묶는 구성요소입니다. 모든 collator가
padding을 하는 것은 아니지만, 여기서 사용하는 `DataCollatorWithPadding`은 동적 padding을
담당합니다.

```python
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

Tokenizer를 전달하는 이유는 PAD ID, padding 방향 등 해당 tokenizer의 규칙을 사용해야 하기
때문입니다.

### Dataset 단계에서는 padding을 미룬다

> ❓ "Dataset에서는 padding=False, collator에서는 padding하는 이유는 무엇인가요?"

토큰화 단계에서는 `truncation=True`, `max_length=16`, `padding=False`로 처리했습니다. 이 설정은
16을 넘는 입력은 자르되, 짧은 샘플에는 PAD를 붙이지 않는다는 뜻입니다. 여기서 "길이 보존"은
원문을 무조건 보존한다는 뜻이 아니라, truncation 후의 가변 길이를 padding으로 늘리지 않는다는
뜻입니다.

예를 들어 토큰화 후 길이가 `[5, 8, 14, 7]`이고 학습 batch를 두 개씩 묶으면 다음과 같습니다.

![토큰화 후 길이 5·8·14·7을 두 개씩 묶어 Batch 1은 최장 8에 맞춰 shape [2, 8]이 되고 Batch 2는 최장 14에 맞춰 shape [2, 14]가 되는 동적 padding 그림](/assets/img/posts/dynamic-padding-and-collator/dynamic-padding-batches.svg){: w="720" h="268" }

| 실제 학습 batch | 샘플 길이 | Padding 후 길이 | Shape |
| --- | --- | --- | --- |
| Batch 1 | `[5, 8]` | `[8, 8]` | `[2, 8]` |
| Batch 2 | `[14, 7]` | `[14, 14]` | `[2, 14]` |

처음부터 모두 16으로 채우는 것보다 PAD가 줄어듭니다. 다만 동적 padding도 `[10, 12, 15, 500]`처럼
긴 샘플 하나가 섞이면 낭비가 큽니다. 길이가 비슷한 샘플끼리 묶는 방식으로 이 차이를 줄일 수
있습니다.

### `map()`의 결과가 곧바로 완성된 학습 batch는 아니다

사용한 `splits.map()` 코드는 원본 열을 자동으로 전부 제거하는 코드가 아닙니다. `text`, `label`에
더해 `input_ids`, `attention_mask`, `labels` 등이 남을 수 있습니다.

이 결과를 collator에 직접 넘길 때는 문자열 `text`와 중복 정답 열 `label` 등을 정리하여 모델에
필요한 열만 전달해야 합니다. `labels`는 정답 열로 유지합니다. 사용한 학습 도구가 이 정리를
대신하는 경우도 있습니다.

---

## 6. 🔢 Shape와 attention mask 읽기

> ❓ "input_ids [6, 14]의 14는 전체 데이터의 최대 길이인가요?"

| 축 | 의미 |
| --- | --- |
| 6 | 현재 batch의 샘플 수 |
| 14 | Padding 후 각 샘플의 토큰 길이 |

일반적인 최장 길이 기준 동적 padding이면, `14`는 현재 6개 샘플 중 가장 긴 입력 길이입니다. 전체
데이터셋의 최대 길이라는 뜻은 아닙니다.

> ⚠️ 다만 특정 배수로 길이를 맞추는 추가 옵션이 있다면 실제 최장 길이보다 더 길게 채워질 수
> 있습니다. 이 노트의 예시는 그런 추가 설정이 없는 경우입니다.
{: .prompt-warning }

### PAD 위치의 mask는 왜 0인가?

> ❓ "PAD 위치의 attention mask가 0이어야 하는 이유는 무엇인가요?"

모델이 PAD 위치를 실제 문맥 정보로 참고하지 않도록 표시하기 위해서입니다.

| 위치 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| 입력 토큰 | CLS | 실제 토큰 | 실제 토큰 | SEP | PAD | PAD |
| attention mask | 1 | 1 | 1 | 1 | 0 | 0 |

이것은 질문한 모델 계열에서 사용하는 일반적인 mask 규칙입니다. 특수 토큰인 CLS와 SEP도 padding은
아니므로 `1`입니다.

Self-attention에서 PAD 위치를 문맥의 key로 참고하지 않도록 처리합니다. 단, mask가 `0`이라고 PAD
위치에 대한 모든 계산이 없어지거나 그 위치의 출력 벡터가 반드시 `0`이 되는 것은 아닙니다.

---

## 7. 📝 잘린 문장이 없어도 max_length를 기록하는 이유

> ❓ "Truncation 비율이 0%여도 max_length 기록이 필요한 이유는 무엇인가요?"

`0%`는 현재 데이터에서 잘린 샘플이 없다는 **결과**이고, `max_length`는 앞으로도 적용할 입력 처리
**규칙**입니다.

```text
정책: truncation=True, max_length=16

현재 입력: 모두 길이 16 이하 → 잘린 샘플 0%
새 입력: 길이 23 → 16으로 잘림
```

상한을 기록해야 재실행할 때 같은 정책을 적용하고, 새 데이터가 길어졌을 때의 동작도 설명할 수
있습니다. 정확한 재현을 위해서는 truncation 사용 여부와 tokenizer 기준도 함께 일치해야 합니다.

---

## 8. ✅ 핵심 정리

| 질문 | 핵심 답변 |
| --- | --- |
| 왜 Dataset 토큰화에서는 `padding=False`인가? | 실제 학습 batch가 정해질 때까지 불필요한 길이 맞춤을 미루기 위해 |
| 왜 collator에서 padding하는가? | 현재 학습 batch의 최장 길이에 맞춰 Tensor로 묶기 위해 |
| 동적 padding과 `max_length`를 함께 쓰는가? | 가능. 필요한 만큼 채우면서 지나치게 긴 입력은 제한 |
| 왜 128인가? | 앞선 답변에서는 예시. 실제 값은 길이 분포·정보 손실·자원·모델 한도로 결정 |
| `[6, 14]`의 14는 무엇인가? | 현재 batch의 padding 후 토큰 길이 |
| PAD mask는 왜 0인가? | PAD를 실제 문맥 key로 참고하지 않도록 하기 위해 |
| Truncation 0%인데 상한을 기록하는 이유는? | 재실행과 새 데이터에 같은 입력 정책을 적용하기 위해 |

---

## 9. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **PAD 낭비** : 길이 `[3, 5, 8]` → 실제 16개 / 위치 24개 / PAD 8개(약 33.3%)
- **`L²`** : 기본 self-attention의 토큰 간 비교량은 길이에 대해 대략 제곱으로 증가
- **한 문장씩 처리하면** PAD는 줄어도 batch 병렬 처리의 장점을 잃는다
- **`padding=True`** : 함께 전달된 문장 중 최장 길이에 맞춤 (동적 padding)
- **`padding="max_length"`** : 짧은 입력도 상한까지 채움 — `max_length`와 역할이 다르다
- **`max_length`만 지정** : `truncation=True`가 없으면 자동으로 잘리지 않는다
- **상한 vs 동적 padding** : "얼마나 긴 입력까지 허용할지" vs "현재 batch를 어느 길이로 맞출지"
- **고정 길이 padding** : 항상 같은 shape가 필요하거나 길이가 원래 비슷할 때 쓸 수 있다
- **128의 근거** : 예시 수치 — 실제로는 길이 분포·정보 손실·계산 자원·모델 제한으로 결정
- **길이 조사 주의** : truncation **전**의 토큰 길이를 봐야 하며, 특수 토큰도 포함해 판단
- **Collator** : 샘플을 학습 batch로 묶는 구성요소 — `DataCollatorWithPadding`이 동적 padding 담당
- **tokenizer를 넘기는 이유** : PAD ID, padding 방향 등 그 tokenizer의 규칙을 써야 하므로
- **동적 padding 효과** : `[5, 8, 14, 7]` → `[2, 8]`, `[2, 14]` — 처음부터 16으로 채우는 것보다 적다
- **동적 padding의 한계** : `[10, 12, 15, 500]`처럼 긴 샘플 하나가 섞이면 낭비가 크다
- **`map()` 결과** : 원본 열이 남을 수 있어 모델에 필요한 열만 넘겨야 한다 (`labels`는 유지)
- **`[6, 14]`의 14** : 현재 batch의 padding 후 길이 — 전체 데이터셋 최대 길이가 아니다
- **attention mask** : CLS·SEP도 padding이 아니므로 `1`, PAD만 `0`
- **mask가 0이어도** : 그 위치의 모든 계산이 사라지거나 출력 벡터가 `0`이 되는 것은 아니다
- **Truncation 0%** : 현재 데이터의 **결과**일 뿐, `max_length`는 앞으로 적용할 **규칙**

</details>

---

## 10. 🔗 관련 글

- [Dataset split과 map() — 학습 데이터를 준비하는 흐름](/posts/dataset-split-and-map/)
- [패딩과 잘라내기, 그리고 shape — 여러 문장을 한 배치로 묶기](/posts/padding-truncation-and-shape/)
- [AutoTokenizer와 체크포인트 — 토크나이저를 맞춰야 하는 이유](/posts/autotokenizer-and-checkpoint/)
