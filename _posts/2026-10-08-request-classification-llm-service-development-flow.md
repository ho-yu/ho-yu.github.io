---
title: "요청 분류 + LLM 응답 서비스 프로젝트 — 전체 개발 흐름과 분류 모델 선정 방식 확정"
date: 2026-10-08 17:28:00 +0900
categories: [Projects, AI Service]
tags: [classification, tf-idf, bert, langchain, fastapi]
---

> 🗂️ **Projects · AI Service** — `classification` `tf-idf` `bert` `langchain` `fastapi`
{: .prompt-info }

---

## 1. 오늘 한 일

- 새 팀 프로젝트 시작
- 전체 개발 흐름 정리
- 분류 모델 개발·선정 방식 확정
- 개발 단계와 서비스 실행 단계 구분
- 팀 공유용 흐름도 수정(v2)

> 오늘 확정한 범위는 **개발 흐름**까지다. 코드 구현이나 모델 학습은 아직 하지 않았다.
{: .prompt-warning }

---

## 2. 전체 개발 흐름

아래 그림처럼 **문서 관리 → 모델 준비 → 서비스 운영** 세 영역으로 나눴다.

![문서 관리, 분류 모델 학습·비교·선정, 서비스 요청 분류부터 LangChain 처리·LLM 호출·응답 기록까지 이어지는 프로젝트 개발 흐름도 v2](/assets/img/posts/request-classification-llm-service-development-flow/development-flow-v2.webp){: w="720" h="450" }

| 영역 | 실행 시점 | 단계 |
| --- | --- | --- |
| 문서 관리 | 등록·추가·수정 시 | ① FastAPI 기반 문서 등록·관리 |
| 모델 준비 | 최초 구축·모델 개선 시 | ② 분류 모델 학습·비교·선정 |
| 서비스 운영 | 사용자 요청마다 | ③ 요청 유형 분류 → ④ LangChain 처리 → ⑤ Local/Cloud LLM 호출 → ⑥ 응답 기록·분석 |

모델 준비 단계에서 평가를 마친 저장 모델을 서비스 운영 단계의 요청 분류에서 사용한다.

---

## 3. 분류 모델 개발 방식

| 구분 | 내용 |
| --- | --- |
| 베이스라인 | TF-IDF + 로지스틱 회귀 |
| 비교 모델 | BERT 등 사전학습 분류 모델 최소 1개 파인튜닝 |
| 비교 방법 | 동일한 검증 데이터·지표로 비교 |
| 최종 선정 | 성능 + 리소스·시간을 함께 고려해 선정·저장 |

- 데이터 파일명·수량·구성은 아직 미정

---

## 4. 개발 단계 vs 서비스 실행 단계

| 구분 | 개발 단계 | 서비스 실행 단계 |
| --- | --- | --- |
| 하는 일 | 모델 학습·비교·선정 | 저장된 최종 모델로 새 요청 분류 → LangChain·LLM 처리 |
| 실행 시점 | 요청마다 실행하지 않음 | 요청이 들어올 때마다 |

> '서비스 분류'를 평가 완료 데이터를 FastAPI 서비스별로 나누는 의미로 이해했는데, 실제로는 **저장된 모델로 새 요청의 유형을 분류**하는 단계였다 — 이 부분을 바로잡았다.
{: .prompt-warning }

---

## 5. 공유 자료 · 진행 관리

- 팀 공유용 개발 흐름도와 분류기 구축·테스트 가이드 요청
- 개발 과정과 실행 과정이 섞여 보이던 흐름도 수정 요청 → 수정본 v2 생성
- 프로젝트 Notion 페이지 접근·편집 가능 여부 확인 요청 — 편집 가능 여부는 아직 미확인
- 프로젝트 채팅을 전체 진행 흐름 팔로업 용도로 쓰기로 함

---

## 6. 오늘의 핵심

> 분류 모델의 **개발·선정 방식**과 실제 서비스에서 **사용하는 흐름**을 명확히 확정했다.
{: .prompt-tip }

---

## 7. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **전체 흐름** : 문서 관리 → 모델 준비 → 서비스 운영(요청 분류 → LangChain → LLM → 응답 기록)
- **베이스라인** : TF-IDF + 로지스틱 회귀
- **비교 모델** : BERT 등 사전학습 분류 모델 최소 1개 파인튜닝
- **선정 기준** : 동일 검증 데이터·지표, 성능 + 리소스·시간
- **개발 vs 실행** : 학습·비교·선정은 요청마다 실행하지 않음, 서비스는 저장된 모델로 분류
- **미정** : 데이터 파일명·수량·구성, Notion 편집 권한
- **진행 상태** : 흐름 확정까지, 구현·학습 전

</details>

---

## 8. 🔗 관련 글

- [선형모델 — Linear Regression과 Logistic Regression](/posts/linear-regression-and-logistic-regression/)
- [Task별 Backbone / Head 정형화 판별 순서](/posts/task-backbone-head-selection-order/)
- [로컬 LLM 비교 프로젝트 — 로컬·클라우드·베이스 모델 최종 비교](/posts/local-llm-comparison-final-results-local-cloud-base/)
