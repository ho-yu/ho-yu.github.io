---
title: "Task별 Backbone / Head 정형화 판별 순서"
date: 2026-09-13 10:00:00 +0900
categories: [Notes, Deep Learning]
tags: [backbone, head, model-selection, tensor-shape, loss-function]
---

> 🗂️ **Notes · Deep Learning** — `backbone` `head` `model-selection` `tensor-shape` `loss-function`
{: .prompt-info }

---

## 1. 🔄 전체 흐름

```text
Task 정의
↓
Input 구조 확인
↓
필요한 정보 확인
↓
Backbone 후보 선정
↓
Backbone Output Shape 확인
↓
Head 선정
↓
Final Output Shape 확인
↓
Target / Loss 호환성 확인
↓
Metric 설정
↓
Validation 성능 비교
↓
최종 모델 선정
```

---

## 2. 🎯 Task 정의

모델이 최종적으로 **무엇을 예측해야 하는지** 먼저 결정한다.

- Classification
- Regression
- Detection
- Segmentation
- Language Modeling

---

## 3. 📥 Input 구조 확인

입력 데이터의 종류와 구조를 확인한다.

- 이미지
- 텍스트
- 음성
- 시계열

---

## 4. 🔍 Task에 필요한 정보 확인

문제를 해결하기 위해 어떤 정보가 유지되어야 하는지 판단한다.

| Task | 유지되어야 하는 정보 |
| --- | --- |
| Classification | 전체적인 의미 |
| Detection | 객체 종류 + 위치 정보 |
| Segmentation | 픽셀 단위 정보 |
| NLP | 토큰 순서 + 문맥 정보 |

---

## 5. 🧱 Backbone 선정

입력 데이터를 잘 처리하면서 Task에 필요한 정보를 충분히 **추출하고 보존할 수 있는
Backbone**을 선택한다.

| 입력 | Backbone 예 |
| --- | --- |
| 이미지 | ResNet / EfficientNet / ViT |
| 텍스트 | Transformer 계열 |

---

## 6. 📐 Backbone Output Shape 확인

Backbone이 어떤 형태의 Feature를 출력하는지 확인한다.

```text
[B, D]
[B, L, D]
[B, C, H, W]
```

Head가 이 Feature를 정상적으로 입력받을 수 있어야 한다.

---

## 7. 🎯 Head 선정

Task가 요구하는 **정답의 형태**에 맞춰 Head를 선택한다.

| Task | Head |
| --- | --- |
| Classification | Classification Head |
| Regression | Regression Head |
| Detection | Detection Head |
| Segmentation | Segmentation Head |

---

## 8. 📐 Final Output Shape 확인

Head가 실제 Task에서 필요한 출력 Shape을 만들어내는지 확인한다.

| 예 | 출력 Shape |
| --- | --- |
| 5개 클래스 분류 | `[B, 5]` |
| 숫자 하나 예측 | `[B, 1]` |

---

## 9. 🔗 Target / Loss 호환성 확인

다음 세 가지가 서로 호환되어야 한다.

```text
Head Output ↔ Target ↔ Loss
```

예:

```text
Output : [B, C] logits
Target : [B] class index
Loss   : CrossEntropyLoss
```

---

## 10. 📊 Metric 설정

Task에 적합한 평가 지표를 선택한다.

| Task | Metric |
| --- | --- |
| Classification | Accuracy / F1-score |
| Regression | MAE / RMSE |
| Detection | mAP |

---

## 11. ✅ Validation으로 최종 선정

구조적으로 적합한 Backbone과 Head 후보를 실제 데이터로 학습한 뒤 비교한다.

주요 비교 기준:

- Validation 성능
- 추론 속도
- 메모리 사용량
- 모델 크기
- 실제 운영 환경에서의 효율성

---

## 12. 📌 핵심 정리

| 항목 | 기준 |
| --- | --- |
| **Head** | 정답의 형태를 기준으로 선택 |
| **Backbone** | 입력 형태 + Task에 필요한 정보를 기준으로 선택 |
| **최종 검증** | Output → Target → Loss의 구조적 호환성 + Validation 성능 |

> 💡 **한 줄 요약** · 구조적으로 먼저 적합한 후보를 걸러내고, 최종적으로 실제 Validation
> 결과를 통해 Backbone과 Head 조합을 선택한다.
{: .prompt-info }

---

## 13. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **판별 순서** : Task → Input 구조 → 필요한 정보 → Backbone 후보 → Backbone Output Shape → Head → Final Output Shape → Target/Loss 호환 → Metric → Validation → 최종 선정
- **Task 정의** : 무엇을 예측할지 — Classification / Regression / Detection / Segmentation / Language Modeling
- **Input 구조** : 이미지 / 텍스트 / 음성 / 시계열
- **필요한 정보** : Classification 전체 의미 / Detection 종류+위치 / Segmentation 픽셀 단위 / NLP 토큰 순서+문맥
- **Backbone** : 입력을 처리하며 Task에 필요한 정보를 추출·보존 — 이미지 ResNet/EfficientNet/ViT, 텍스트 Transformer 계열
- **Backbone Output Shape** : `[B, D]` / `[B, L, D]` / `[B, C, H, W]` — Head가 입력받을 수 있어야 함
- **Head** : 정답의 형태에 맞춰 선택 — Classification/Regression/Detection/Segmentation Head
- **Final Output Shape** : 5개 클래스 분류 `[B, 5]`, 숫자 하나 예측 `[B, 1]`
- **호환성 3요소** : Head Output ↔ Target ↔ Loss — 예: `[B, C]` logits / `[B]` class index / CrossEntropyLoss
- **Metric** : Classification Accuracy/F1 / Regression MAE/RMSE / Detection mAP
- **최종 선정 기준** : Validation 성능 + 추론 속도 + 메모리 + 모델 크기 + 운영 효율성
- **핵심 기억법** : Head = 정답 형태 / Backbone = 입력 형태 + 필요한 정보 / 검증 = 구조 호환성 + Validation

</details>

---

## 14. 🔗 관련 글

- [Hugging Face Model Card와 Pipeline, 그리고 Task · Backbone · Head](/posts/hugging-face-model-card-and-backbone-head/)
- [MLP와 CNN 모델 설계 — Shape 흐름과 train/eval 차이](/posts/mlp-cnn-model-design-and-shape-flow/)
- [CrossEntropyLoss 이해하기 — 다중 클래스 분류](/posts/cross-entropy-loss/)
