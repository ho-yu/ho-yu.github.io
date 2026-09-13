---
title: "Hugging Face Model Card와 Pipeline, 그리고 Task · Backbone · Head"
date: 2026-09-13 09:00:00 +0900
categories: [Notes, Deep Learning]
tags: [hugging-face, model-card, pipeline, backbone, head]
---

> 🗂️ **Notes · Deep Learning** — `hugging-face` `model-card` `pipeline` `backbone` `head`
{: .prompt-info }

---

## 1. 🤗 Hugging Face의 model id와 revision

| 용어 | 의미 |
| --- | --- |
| `model id` | 저장소 |
| `revision` | 저장소의 특정 버전 |

---

## 2. 📋 Model Card 읽는 순서

1. 어떤 task와 language를 지원하나요?
2. Base Model인가요, Fine-tuned Model인가요?
3. intended use와 out-of-scope use는 무엇인가요?
4. 어떤 데이터로 학습했나요?
5. 어떤 dataset과 metric으로 평가했나요?
6. limitations, bias, failure case는 무엇인가요?
7. license 조건은 무엇인가요?

---

## 3. 🔄 Pipeline 흐름

```text
1. 문자열 입력
        ↓
2. Tokenizer / pre-processing
        ↓
3. model forward
        ↓
4. task-specific post-processing
        ↓
5. return python object
```

---

## 4. 🧩 Task · Backbone · Head

| 구성 요소 | 역할 | 의미 |
| --- | --- | --- |
| **Task** | 목적 | 모델이 해결해야 하는 문제 — 무엇을 예측할지 결정 |
| **Backbone** | 특징 추출기 | 입력에서 중요한 특징을 추출하는 모델 본체 — feature 추출 |
| **Head** | 최종 답변기 | backbone의 feature를 task에 맞는 최종 출력으로 변환하는 부분 — task별 답 생성 |

---

## 5. 🛠️ 모델을 구성하는 순서

특정 task를 먼저 정의하고, 사람이 데이터의 특성을 분석해 적절한 전처리 방식과 입력 및 정답
형식을 설계한다. 그 다음 task를 해결하는데 적합한 backbone과 head 구조를 선택해 모델을
구성하고 학습시킨다.

> 💡 동일한 전체 pipeline을 사용하더라도, backbone과 head가 달라지면 출력의 형태와
> 의미뿐 아니라 성능도 달라질 수 있다.
{: .prompt-info }

---

## 6. 🧭 Backbone / Head 조합 판별 순서

task별 head와 backbone을 사람이 직접 정하는 만큼, task별 head와 backbone이 자연스러우면서
적합한 조합인지 판별이 필요하다. 완전 표준화된 단 하나의 공식은 없지만, 일반적으로 많이
사용하는 정형화된 판별 순서가 있다고 한다.

1. task 정의
2. 입력 구조 확인
3. 정답 / 출력 구조 확인
4. backbone 후보 결정
5. head 구조 결정
6. shape 호환성 확인
7. loss와 출력 호환성 확인
8. validation으로 최종 검증

---

## 7. ✅ 핵심 정리

| 구성 요소 | 결정 기준 |
| --- | --- |
| **Head** | "정답의 형태"에서 결정한다 |
| **Backbone** | "입력의 형태와 task에 필요한 정보"를 기준으로 결정한다 |
| **최종 검증** | output – target – loss의 구조적 호환성과 validation 성능으로 검증한다 |

> 📌 **습관** · 새로운 모델을 볼 때는 `input → backbone output → head output → target →
> loss`의 shape을 한 줄로 적어보는 습관을 들여, 구조가 자연스러운지 스스로 판별할 수
> 있는 능력을 기르자.
{: .prompt-tip }

---

## 8. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **model id / revision** : 저장소 / 저장소의 특정 버전
- **Model Card 읽는 순서** : task·language → Base/Fine-tuned → intended/out-of-scope use → 학습 데이터 → 평가 dataset·metric → limitations·bias·failure case → license
- **Pipeline 흐름** : 문자열 입력 → Tokenizer/pre-processing → model forward → task-specific post-processing → python object 반환
- **Task** : 목적 — 무엇을 예측할지 결정
- **Backbone** : 특징 추출기 — 입력에서 feature를 추출하는 모델 본체
- **Head** : 최종 답변기 — backbone의 feature를 task에 맞는 출력으로 변환
- **구성 순서** : task 정의 → 데이터 분석·전처리·입출력 형식 설계 → backbone·head 선택 → 학습
- **같은 pipeline이라도** : backbone·head가 달라지면 출력의 형태·의미와 성능이 달라질 수 있음
- **판별 순서 8단계** : task → 입력 구조 → 정답/출력 구조 → backbone 후보 → head 구조 → shape 호환 → loss·출력 호환 → validation
- **Head 기준** : 정답의 형태 / **Backbone 기준** : 입력의 형태 + task에 필요한 정보
- **최종 검증** : output – target – loss 구조적 호환성 + validation 성능
- **습관** : `input → backbone output → head output → target → loss` shape을 한 줄로 적어보기

</details>

---

## 9. 🔗 관련 글

- [Task별 Backbone / Head 정형화 판별 순서](/posts/task-backbone-head-selection-order/)
- [MLP와 CNN 모델 설계 — Shape 흐름과 train/eval 차이](/posts/mlp-cnn-model-design-and-shape-flow/)
- [Attention과 Transformer, 그리고 모델을 고르고 조합하는 법](/posts/attention-transformer-and-model-combination/)
