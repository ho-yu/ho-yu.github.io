---
title: '[Git] Git (5) - reset, revert '
author: ho-yu
date: 2022-02-26 17:29:16 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

![git](https://user-images.githubusercontent.com/64628448/155834033-6e1dbb9a-3531-47c9-805f-6ed3ffa34702.png){: width="50%" height="10%"}

# 📚 Introduction

예전 커밋으로 브랜치를 되돌리는 reset과 
비슷한 개념인 revert의 기본 개념과 사용법을 알아보자.

# 💥 Git reset 이란? 
> 예전 커밋으로 브랜치를 되돌리고 싶어요 !
<br>

# 💥 SourceTree에서 진행하기.
- `Soft / Mixed reset` ⇒
    
    모든 이력을 남기면서 브랜치를 되돌리기. 
    - Soft와 Mixed의 차이점 ⇒ <br>
        `[Mixed]`는  변경사항을 스테이지 아래로 내려서 다시 무엇을 스테이지 위로 Add 할지 고민할 수 있고, `[Soft]`는 변경사항을 스테이지 위로 올려서 다시 당장 커밋할 수 있다는 차이점이 있다.
        
- `Hard reset` ⇒
    
    모든 이력을 지우며 브랜치를 되돌리기.
    - 현재 브랜치가 어디에 있던지, 커밋하지 않은 변경사항이 얼마나 있는지와 상관없이 어디로든 깔끔하게 이동할 수 있다.
    - 공통 브랜치에서 ( 강제 푸쉬 = History를 수정하는 푸쉬 )를 하면 히스토리가 꼬일 수 있기 때문에, 반드시 자신 혼자만 사용하는 브랜치에서 사용해야 한다.


# 💥 Git revert 란? 
> 커밋 잘못했는데, 이 커밋의 변경사항을 되돌리고 싶어요 ! 

🛎 방금 한 커밋 만이 아니라, 이전에 한 커밋도 되돌릴 수 있다 !
<br>

# 💥 SourceTree에서 진행하기.
1. History → 되돌리고 싶은 커밋 우 선택한다.
2. 커밋 되돌리기를 선택한다.

# 💥 reset보다 revert ?
💡 `reset`으로 커밋을 아무도 모르게 없앨 수도 있지만, <br> 
여러 사람들과 협업하고 있고, 이력 관리가 중요하다면,<br> 
잘못된 커밋을 없애는 것보다 변경 사항을 되돌리는 새로운 커밋을 만드는게 더 좋다.