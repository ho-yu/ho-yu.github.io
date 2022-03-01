---
title: '[Git] Git (6) - stash '
author: ho-yu
date: 2022-02-26 17:35:51 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

![git](https://user-images.githubusercontent.com/64628448/155834033-6e1dbb9a-3531-47c9-805f-6ed3ffa34702.png){: width="75%"}

# 📚 Introduction

커밋을 만들지 않고, 변경사항을 잠시 서랍(?) 속에 저장할 수 있는 stash의 기본 개념과  사용법에 대해서 알아보자.
<br>

# 💥 Git stash 란? 
> 변경사항을 잠시 다른 곳에 저장하고 싶어요, 커밋은 만들지 않을래요 !<br>

> 커밋하지 않은 변경사항을 서랍(?) 속에 넣어두기.

<br>

# 💥 SourceTree에서 진행하기.
1. History → `stash`하고 싶은 커밋을 선택 후, 상단 스태시 탭을 선택한다.
2. 스태시에 대한 설명을 적고 확인을 선택한다.
3. 저장된 스태시를 꺼내려면 왼쪽 사이드바의 스태시 섹션에서 원하는 스태시를 선택하고, 우클릭한 후, 스태시 적용을 선택한다.
4. 스태시했던 변경사항이 스테이지로 튀어나온 것을 확인할 수 있다.


💡 `stash`에는 `tracked 상태` (추적 중 - Git에 한번이라도 올렸던 상태) 인 파일들만 들어간다. <br>
새로만든 파일은 `untracked` 상태라 들어가지 않는다.




