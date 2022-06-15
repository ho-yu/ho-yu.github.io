---
title: '[Spring] Spring - HTTP(1) '
author: ho-yu
date: 2022-06-13 22:48:51 +0900
categories: [Study, Http, Spring]
tags: [http, spring]
---

![spring](https://user-images.githubusercontent.com/64628448/173368063-e326ec44-d5c9-4932-afaa-9fab1b072633.png){: width="75%"}

# 📚 Introduction

앞으로 복습할 내용들은 SpringMVC를 이용해 간단한 게시판과 웹사이트를 만들어 볼 계획이고, <br>
다시 복습하면서 학습했던 내용들을 간단히 기록해놓으려고 한다. <br>

# (1)
오늘은 클라이언트와 서버가 대략 무엇인지, 어떻게 동작하는지에 대해 간단히 훑어보았다. <br>
클라이언트는 우리가 매일 사용하는 컴퓨터, 즉, 서비스를 이용하고자 하는 개체라고 보면 될 것 같고, <br>
서버는 개체들이 원하는 서비스를 제공하는 일종의 집합(?)이라고 해야하나?
쉽게 말하면 손님과 가게 사장 같은 관계로 이해했다. <br>

아래 이미지는 SpringMVC를 학습하기전에 Servlet이 어떻게 데이터를 주고받는지에 대한 예시이다.
<br>
![http](https://user-images.githubusercontent.com/64628448/173360075-11600e81-7968-49cc-b62b-d0f7ce25a537.png)
<br>
"/" 로 구분해주고, 파라미터는 "?"뒤에 Key-Value 형태로 붙여준다. 여러개를 붙일 때는 "&"를 사용한다.
<br>

만약 여러개를 보내는데, Key가 모두 같을 경우, 아래와 같이 하면 된다.
<br>
![http](https://user-images.githubusercontent.com/64628448/173360289-346a5de7-7e6d-4103-a975-6fcc85c44f8c.png)
<br>

# (2)
만약 하나의 클라이언트가 각자 다른 서비스를 제공하는 여러개의 서버가 있을 경우, <br>
IP주소 만으로는 어떤 서버를 호출하는지 알 수가 없다. -> 이 때, port번호로 구분한다. <br>

# (3)
WAS란? (Web Application Server) <br>
=> 프로그램을 서버에 설치하고, 클라이언트들은 서버로 원격프로그램을 호출해서 실행결과만 전송해서 클라이언트들에게 편의성을 제공.
<br>
-- 과거에는 클라이언트에 프로그램을 설치해서 사용. -> update가 불편. -> 서버 하나에만 설치해서 서버는 update만 하면 된다.
<br>

💡 




