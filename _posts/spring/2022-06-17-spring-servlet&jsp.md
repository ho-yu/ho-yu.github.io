---
title: '[Spring] Spring - Servlet & JSP (1) '
author: ho-yu
date: 2022-06-22 22:22:57 +0900
categories: [Study, Spring]
tags: [spring]
---

![spring](https://user-images.githubusercontent.com/64628448/173368063-e326ec44-d5c9-4932-afaa-9fab1b072633.png){: width="75%"}

# 📚 Introduction
Servlet & JSP <br>

# Servlet 이란?

- 자바를 사용하여 웹을 만들기 위해 필요한 기술.<br>
- 일반적으로 웹서버는 정적인 페이지만 제공. <br>
웹 서버가 동적인 페이지를 제공할 수 있도록 도와주는 Application이 Servlet이며, 동적인 페이지를 생성하는 Application이 CGI다.<br>

- 서블릿의 생명주기 (Life Cycle) → <br>
    웹 애플리케이션 컨테이너에서 콘텍스트가 초기화되면 생명주기가 시작된다.<br>
    1. 초기화 (initialize)<br>
    2. 서비스 (service)<br>
    3. 소멸 (destroy)<br><br>

- 서블릿의 동작방식 → <br>
    1. 사용자(클라이언트)가 URL을 치고 엔터치면 HTTP Request를 Servlet Container로 전송.<br>
    2. Servlet Contatiner는 HttpServletRequest, HttpServletResponse 두 객체 생성.<br>
    3. web.xml은 사용자가 요청한 URL을 분석하여 어느 서블릿에 대해 요청을 한 것인지 찾는다.<br>
    4. 해당 서블릿에서 service 메소드를 호출한 후 클라이언트의 POST, GET 여부에 따라 doGet() 또는 doPost()를 호출한다.<br>
    5. doGet(), doPost()는 동적 페이지를 생성한 후 HttpServletResponse 객체에 응답을 보낸다.<br>
    6. 응답이 끝나면 HttpServletRequest, HttpServletResponse 두 객체를 소멸시킨다.<br>

<img width="853" alt="ServletEx" src="https://user-images.githubusercontent.com/64628448/175036132-c3b74196-6bfc-49bb-9ff0-6deac23d31fe.png"><br>

- @WebServlet = @Controller + @RequestMapping. 그리고 HttpServlet을 상속받는다. <br>
- Servlet : 기본적으로 singleton. (1개의 인스턴스로 재활용.) <br>
- Spring도 마찬가지로 하나의 인스턴스로 여러 요청을 처리함.<br>

- Servlet의 기본 객체 ->
<img width="1004" alt="servletDefault" src="https://user-images.githubusercontent.com/64628448/175036960-fdbfebea-a336-474d-a73a-1dfb66092a43.png"><br>

# CGI (Common Gateway Interface) 란?

- 웹 서버와 요청을 받아 처리해줄 로직을 담고있는 애플리케이션 프로그램 사이의 인터페이스. <br>
- CGI가 비효율적이라 나온 것이 Servlet.<br>
<img width="584" alt="CGI" src="https://user-images.githubusercontent.com/64628448/175035948-2f783353-811c-46cd-83b6-f5543a52ddb9.png"><br>

# JSP (Java Servlet Page) 란?

- HTML 코드에 Java 코드를 넣어 동적 웹페이지를 생성하는 Web Application 도구이다.<br>
- JSP가 실행되면, 자바 서블릿으로 변환되고, 웹 어플리케이션 서버에서 동작되면서 필요한 기능을 수행한 후, 생성된 데이터를 웹 페이지와 함께 클라이언트로 응답한다. <br>

# JSP의 호출 과정

<img width="435" alt="jsp(1)" src="https://user-images.githubusercontent.com/64628448/175037402-d28f7fa8-7091-4575-b950-4bbd389ed495.png"> <br>
<img width="308" alt="jsp(2)" src="https://user-images.githubusercontent.com/64628448/175037442-f7c10442-5a08-4b57-9f0c-7d9fe73f159e.png"> <br>

- JSP가 실행되면 WAS는 내부적으로 JSP 파일을 Java Servlet(.java)으로 변환한다.<br>
- WAS는 이 변환한 Servlet을 동작하여 필요한 기능을 수행한다.<br>
    1. WAS는 사용자 요청에 맞는 적절한 Servlet 파일을 컴파일(.class 파일 생성)한다.<br>
    2. .class 파일을 메모리에 올려 Servlet 객체를 만든다.<br>
    3. 메모리에 로드될 때 Servlet 객체를 초기화하는 init() 메서드가 실행된다.<br>
    4. WAS는 Request가 올 때마다 thread를 생성하여 처리한다.<br>
    5. 각 thread는 Servlet의 단일 객체에 대한 service() 메서드를 실행한다.<br>
    6. service() 메서드는 요청에 맞는 적절한 메서드(doGet, doPost 등)를 호출한다.<br>
    수행 완료 후 생성된 데이터를 웹 페이지와 함께 클라이언트로 응답한다.<br>
 
- 유효범위와 속성 <br>
ServletContext에는 pageContext라는 지역변수와 application라는 공통저장소가 존재. <br>
-> pageContext는 요청 하나만 처리하고 초기화, application은 공용으로 사용하기에 여러 클라이언트의 요청을 저장하기에 부적합.<br>

따라서 session을 사용.<br>
session = 각 클라이언트마다 갖는 개별 저장소라고 보면 됨.<br>
--> session객체는 서버부담이 제일 크기 때문에 최소한의 클라이언트 정보만 저장하는 것이 좋음.<br>
--> 페이지들 간에 데이터 전달이 필요하다면 request객체 사용.<br>

<img width="1049" alt="servletDefault(2)" src="https://user-images.githubusercontent.com/64628448/175037970-9d739c45-49e0-46a4-9d9f-d79292dd1fd2.png"><br>

💡 




