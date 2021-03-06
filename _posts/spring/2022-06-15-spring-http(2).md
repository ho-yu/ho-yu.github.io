---
title: '[Spring] Spring - HTTP(2) '
author: ho-yu
date: 2022-06-15 22:20:51 +0900
categories: [Study, Http, Spring]
tags: [http, spring]
---

![spring](https://user-images.githubusercontent.com/64628448/173368063-e326ec44-d5c9-4932-afaa-9fab1b072633.png){: width="75%"}

# 📚 Introduction

protocol, http에 대해 간략히 정리.

# 프로토콜(Protocol) 이란?
- 클라이언트와 서버 서로 간의 통신을 위한 약속, 규칙. <br>
- 주고 받을 데이터에 대한 형식을 정의한 것. <br>
ex) 편지(business letter), 편지봉투. <br>

# HTTP(Hyper Text Transfer Protocol) 란?
- 텍스트 기반의 프로토콜. <br>
- 상태를 유지하지 않는다.(stateless) -> 클라이언트 정보를 저장하지 않는다. -> 이를 보완하기 위해 쿠키와 세션을 사용한다. <br>
- 확장이 가능하다 -> 커스텀 헤더(header) 추가가 가능하다. <br>


# HTTP 메서드

1. GET <br>
(1-1). 서버의 리소스를 가져오기 위해 설계. <br>
(1-2). queryString을 통해 데이터를 전달.(소용량) <br>
(1-3). URL에 데이터가 노출되므로 보안에 취약하다.<br>
(1-4). 데이터 공유에 상대적으로 유리. <br>
ex) 검색엔진에서 검색단어 전송에 이용. <br>

2. POST <br>
(2-1). 서버에 데이터를 올리기 위해 설계됨. <br>
(2-2). 전송데이터 크기의 제한이 없음.(대용량) <br>
(2-3). 데이터를 요청메시지의 body에 담아 전송. <br>
(2-4). GET에 비해 보안에 유리한 편, 데이터 공유에는 GET보다 불리. <br>
(+)HTTPS = HTTP + TLS <br>
ex) 게시판에 글쓰기, 로그인, 회원가입. <br>


# 바이너리 파일(Binary File) 

- 문자와 숫자가 저장되어 있는 파일. <br>
- 데이터를 있는 그대로 읽고 쓴다. <br>

# 텍스트 파일(Text File) = 

- 문자만 저장되어 있는 파일. <br>
- 숫자를 문자로 변환 후 쓴다. <br>

# MIMF (Multipurpose Internet Mail Extensions)

- 텍스트 기반 프로토콜에 바이너리 데이터 전송하기 위해 고안. <br>
- HTTP Content-Type헤더에 사용, 데이터 타입을 명시.<br>






💡 




