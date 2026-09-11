---
title: "AWS 시작 전 체크리스트 — 리전, IAM, 크레딧, 도메인"
date: 2026-09-11 08:50:00 +0900
categories: [Notes, AWS]
tags: [aws, iam, region]
---

> 🗂️ **Notes · AWS** — `aws` `iam` `region`
{: .prompt-info }

---

## 1. 🌏 리전은 반드시 확인한다

| 구분 | 리전 |
| --- | --- |
| 국내 | 한국 |
| 해외 | 일본 |

> ⚠️ 작업 전에 **반드시 리전을 확인**한다.
{: .prompt-warning }

---

## 2. 🔐 root 계정 대신 IAM 계정

root 계정은 최대한 사용하지 않는다. IAM 계정을 생성한 뒤 사용자에게 배포한다.

![root 계정은 최대한 사용하지 않고, IAM 계정을 생성한 뒤 여러 사용자에게 배포하는 구조](/assets/img/posts/aws-getting-started-checklist/root-vs-iam.svg){: w="720" h="210" }

---

## 3. 💳 크레딧 관련 팁

- **혁신의 숲** → AWS 크레딧 행사
- 정부 지원 크레딧 등을 받을 수 있음
- 정보통신업이면 상관없음

---

## 4. 🌐 도메인 관련 팁

- **내도메인.한국** → 가입하면 무료라고 함

---

## 5. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **리전** : 국내는 한국, 해외는 일본 — 작업 전 반드시 확인
- **root 계정** : 최대한 사용하지 않는다
- **IAM 계정** : 생성 후 사용자에게 배포
- **크레딧** : 혁신의 숲 AWS 크레딧 행사, 정부 지원 크레딧 (정보통신업이면 상관없음)
- **도메인** : 내도메인.한국 — 가입하면 무료라고 함

</details>
