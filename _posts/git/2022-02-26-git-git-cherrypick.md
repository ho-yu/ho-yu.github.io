---
title: '[Git] Git (4) - cherrypick '
author: ho-yu
date: 2022-02-26 16:52:49 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

![git](https://user-images.githubusercontent.com/64628448/155834033-6e1dbb9a-3531-47c9-805f-6ed3ffa34702.png){: width="50%" height="10%"}

# 📚 Introduction

다른 브랜치의 커밋 하나를 가져와서 내 브랜치에 반영할 수 있는 cherrypick의 기본 개념과 사용법에 대해서 알아보자.

# 💥 Git cherrypick 이란? 
> 다른 브랜치의 커밋 하나를 내 브랜치에 반영하고 싶어요 !
<br>

## 🛎 이럴 때 사용해요 !

💡 개발자 A와 B, 2명이 개발을 진행한다고 가정해보자. <br>
`master` 브랜치를 각자 개발한 코드들을 합치는 main 브랜치라고 약속을 했다. <br> 
A와 B는 각자 자신이 개발해야 할 브랜치인 `feature/a`, `feature/b` 브랜치를 생성하고 각자 개발을 진행 할 것이다. <br>
여기서 A가 3개의 커밋을 만들었고, B는 자신이 수정한 코드에 A가 2번째로 만든 커밋만 가져와서 반영하고 싶다. <br>
바로 이 때, `cherry pick`을 이용해 A의 2번째 커밋만 가져와서 자신의 브랜치 `feature/b`에 반영할 수 있다.


# 💥 SourceTree에서 진행하기.
1. History → 코드를 합치고 싶은 branch로 check-out 한다.
2. 가져오고 싶은 커밋 우클릭 후 `cherry-pick`을 선택한다.
3. 가져오고 싶은 커밋의 커밋메시지와 함께 최신 커밋위에 달라 붙어 있으면 성공 ! <br>
    ( 제대로 반영됐는지 확인은 언제나 필수 ! )



