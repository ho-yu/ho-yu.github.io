---
title: "데이터 분리와 평가지표 — train/valid/test"
date: 2026-08-12 09:00:00 +0900
categories: [Notes, Machine Learning]
tags: [train-test-split, classification, regression, precision, recall]
---

> 🗂️ **Notes · Machine Learning** — `train-test-split` `classification` `regression` `precision` `recall`
{: .prompt-info }

---

## 1. 📖 개요

쇼핑몰 고객 1,000명(이탈 약 10%) 데이터로 이탈 예측 모델을 만든다. 개발자가 전체 데이터로 모델을 학습하고 같은 데이터로 Accuracy를 재면 98%가 나온다. 그런데 이 모델을 신규 고객에게 적용하니 실제 이탈자를 거의 못 찾는다.

이 모델은 학습에 쓴 데이터를 "외운" 것이다 — 답을 미리 보고 시험을 본 것과 같다. 처음 보는 데이터에서의 성능(일반화 성능)을 정직하게 재려면 학습에 쓰지 않은 데이터로 채점해야 한다. 그런데 검증까지만 하고 그 결과로 여러 모델·설정을 반복 비교하면, 이번에는 검증 데이터에 "선택의 편향"이 스며든다 — 그래서 학습(train)·선택(valid)·최종 확인(test) 세 역할이 각각 다른 데이터를 필요로 한다.

---

## 2. 💡 핵심 개념

### train / validation / test

수능을 준비하는 과정과 같다. 문제집(train)으로 개념을 익히고, 모의고사(valid)로 여러 학습법 중 무엇이 더 나은지 반복해서 비교하며 골라내지만, 모의고사를 반복해서 보정한 학습법은 이미 그 모의고사에 맞춰져 있다. 실제 실력은 한 번도 풀어본 적 없는 진짜 수능(test)에서만 정직하게 드러난다.

- **train** : 모델을 파라미터를 학습하는 데이터
- **validation** : 모델·하이퍼파라미터·임계값을 반복 비교해 선택하는 데이터
- **test** : 모든 선택을 고정한 뒤 성능을 단 한번 확인하는 데이터

```text
train = 모델 A, B, C 학습
valid = A 85% / B 91%(선택) / C 88%  ← 여기서 B를 고른다
test  = 선택된 B의 최종 성능을 한 번만 확인
```

### 분할 코드의 세 파라미터

```python
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y,
)
```

- **test_size=0.2** : 입력 데이터 중 전체의 20%를 떼어낼 비율. 1000개인 경우 800개 → `X_temp, y_temp`, 200개 → `X_test, y_test`
- **random_state** : 분할에 쓰이는 난수를 고정해, 같은 코드를 다시 실행해도 같은 분할이 나오게 함
- **stratify=y** : 분류 문제에서 나누기 전후로 클래스 비율을 유지함 (회귀에서는 제거)

2단계로 나누면 train:valid:test = 60:20:20이 된다(전체의 20%를 test로 먼저 떼고, 남은 80%의 25%를 valid로 떼면 `0.25 × 0.8 = 0.2`이므로 결과가 60:20:20).

![전체를 train+valid(80%)와 test(20%)로, 다시 train(60%)과 valid(20%)로 나누는 2단계 분할](/assets/img/posts/train-valid-test-split-and-metrics/train-valid-test-split.png)

---

## 3. 🔍 이해하기

### 분류 평가 지표

혼동행렬(TP·FP·FN·TN) 위에서 계산된다.

![혼동행렬에서 Precision은 "예측 Positive" 열, Recall은 "실제 Positive" 행을 사용한다](/assets/img/posts/train-valid-test-split-and-metrics/confusion-matrix-precision-recall.png)

| 지표 | 산식 | 언제 중요한가 |
|---|---|---|
| Accuracy | `(TP+TN)/전체` | 클래스 비율이 균형에 가깝고 오류 비용이 대칭일 때 |
| Precision | `TP/(TP+FP)` | 오탐(FP)의 비용이 클 때 |
| Recall | `TP/(TP+FN)` | 놓침(FN)의 비용이 클 때 |
| F1 | Precision·Recall의 조화평균 | 둘의 균형이 필요할 때 |

- **성립 조건:** Precision과 Recall은 서로 트레이드오프 관계다 — 양성 판정 기준(임계값)을 엄격히 하면 Precision은 오르고 Recall은 내려간다.

> ⚠️ **값의 방향** · 이탈 고객 100명 중 1명만 있는 데이터에서 "전부 유지"라고 예측해도 Accuracy는 99%지만, 실제 양성은 한 명도 못 찾는다(Recall 0). Accuracy 하나만으로는 이 실패를 볼 수 없다.
{: .prompt-warning }

> 💡 **한 줄 요약** · Accuracy는 전체 정답률, Precision은 예측한 양성이 얼마나 정확한지, Recall은 실제 양성을 얼마나 놓치지 않고 찾았는지를 보는 지표이다.
{: .prompt-info }

---

## 4. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- train은 학습, valid는 반복 비교를 통한 선택, test는 모든 선택이 끝난 뒤 단 한 번의 최종 확인 — 세 역할이 다르기 때문에 세 데이터가 필요하다.
- `test_size`는 현재 입력 데이터 대비 떼어낼 **비율**이고, `stratify`는 분류에서만 쓰며 클래스 비율을 유지한다.
- 회귀는 MAE(이상치에 덜 민감)·RMSE(큰 오차에 민감)·R²(음수 가능, 0은 평가 데이터 평균 기준)로, 분류는 오류 비용에 따라 Precision(FP 비용)·Recall(FN 비용)·F1(균형)로 채점한다.
- Accuracy는 불균형 데이터에서 다수 클래스만 맞혀도 높게 나올 수 있어 그 자체로는 신뢰할 수 없다.
- test 점수를 반복해서 보며 모델을 고치면 그 순간부터 test는 사실상 학습에 쓰인 것과 같아 성능이 부풀려진다.

</details>

---

## 5. 🔗 관련 글

- [지도학습과 비지도학습](/posts/supervised-vs-unsupervised-learning/)
- [지도·비지도 5개 모델 비교와 선택 기준](/posts/model-selection-linear-knn-tree-kmeans-pca/)
