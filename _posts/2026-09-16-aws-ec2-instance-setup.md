---
title: "EC2 인스턴스 생성부터 정리까지 — 초기 설정과 탄력적 IP"
date: 2026-09-16 08:55:00 +0900
categories: [Notes, AWS]
tags: [aws, ec2, elastic-ip, nginx]
mermaid: true
---

> 🗂️ **Notes · AWS** — `aws` `ec2` `elastic-ip` `nginx`
{: .prompt-info }

---

## 1. 📖 전체 흐름

```mermaid
flowchart LR
  A["EC2 인스턴스 생성"] --> B["접속 후 초기 설정"]
  B --> C["탄력적 IP 설정"]
  C --> D["사용하지 않을 때 정리"]
```

---

## 2. 🖥️ EC2 인스턴스 생성

| 항목 | 값 |
| --- | --- |
| OS | Ubuntu 24.04 LTS |
| 아키텍처 | 64비트(Arm) |
| 인스턴스 유형 | `t4g.micro` |
| 키 페어 | RSA — `.pem`으로 생성 |
| 보안그룹 | 인바운드, 아웃바운드 규칙 설정 |

---

## 3. 🔧 접속 후 초기 설정

```bash
sudo apt update
sudo apt install git
sudo apt install nginx
```

| 명령 | 역할 |
| --- | --- |
| `sudo apt update` | Ubuntu update |
| `sudo apt install git` | git |
| `sudo apt install nginx` | 인터넷 접속을 할 수 있게 할 수 있는 서버 |

---

## 4. 📌 탄력적 IP 설정

AWS의 public IP는 상시 할당되며 계속 바뀐다. 그래서 IP를 고정하기 위해 탄력적 IP를 사용한다.

![public IP는 상시 할당되며 계속 바뀌는 반면, 탄력적 IP는 할당한 뒤 대상 인스턴스에 연결해 IP를 고정한다는 비교](/assets/img/posts/aws-ec2-instance-setup/elastic-ip.svg){: w="720" h="250" }

> 💡 **경로** · 네트워크 및 보안 → 탄력적 IP → IP 주소 할당 후 대상 인스턴스에 연결하면 된다.
{: .prompt-info }

---

## 5. 🧹 인스턴스를 사용하지 않을 경우

아래 내용을 삭제한다.

- 탄력적 IP
- 보안그룹
- 키 페어
- 인스턴스

---

## 6. 🧠 핵심 기억 카드

<details markdown="1">
<summary><strong>펼쳐서 확인</strong></summary>

- **인스턴스 생성** : Ubuntu 24.04 LTS · 64비트(Arm) · `t4g.micro` · RSA `.pem` 키 페어 · 보안그룹 인바운드/아웃바운드
- **초기 설정** : `apt update` → `git` → `nginx` 설치
- **nginx** : 인터넷 접속을 할 수 있게 할 수 있는 서버
- **탄력적 IP를 쓰는 이유** : public IP는 상시 할당되며 계속 바뀌므로 고정용
- **탄력적 IP 경로** : 네트워크 및 보안 › 탄력적 IP › 할당 후 인스턴스에 연결
- **정리 순서** : 탄력적 IP · 보안그룹 · 키 페어 · 인스턴스 삭제

</details>

---

## 7. 🔗 관련 글

- [AWS 시작 전 체크리스트 — 리전, IAM, 크레딧, 도메인](/posts/aws-getting-started-checklist/)
