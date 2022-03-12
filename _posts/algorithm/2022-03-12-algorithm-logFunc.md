---
title: '[Algorithm] (2) 정수의 자릿수 구하기 '
author: ho-yu
date: 2022-03-12 14:42:35 +0900
categories: [Study, Algorithm]
tags: [java, algorithm]
---

![Algorithm](https://user-images.githubusercontent.com/64628448/156101894-2c24e063-ab4f-4421-9a2e-a63f1e22eed7.png){: width="75%"}

# 📚 Introduction
오늘은 간단하게 ! <br> 
정수의 자릿수는 어떻게 구할까?

# 💥 log()

Math클래스의 log 함수를 이용하면 자릿수를 구할 수 있다. <br>
`log(x)` 는 밑이 e (2.718...)인 자연로그 함수이다. <br>
`log10()` 는 밑이 10인 로그함수이다. <br>

그렇다면 정수의 자릿수는 어떻게 구할까? <br>
log10() 함수를 이용한 예시를 보면, <br>

```
Math.log10(10) // 1.0
Math.log10(100) // 2.0
Math.log10(1000) // 3.0
```

<img width="339" alt="스크린샷 2022-03-12 14 27 45" src="https://user-images.githubusercontent.com/64628448/158005209-ae4c3c58-9aa8-4ee7-b017-63dd6bee7ccd.png">

해당 값이 어떻게 나오는지 위 예시코드와 사진을 보면 이해가 될 것이다. <br>

log10() 함수가 double형으로 값을 리턴하니까, 이를 int형으로 변환한 후, 1을 더해주면 정수값의 자릿수를 얻을 수 있다. <br>

끝 !















