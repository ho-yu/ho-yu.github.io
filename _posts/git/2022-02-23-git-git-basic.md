---
title: '[Git] Git (1) '
author: ho-yu
date: 2022-02-23 18:15:21 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

## Inroduction
들어가기전에 버전관리가 무엇인지 알아보자.

RPG 게임을 예를 들면, 한 캐릭터로 게임을 진행하다가 게임을 종료하기 전에 지금까지 진행한 게임데이터를 저장을한다. 그리고 나중에 저장한 데이터를 불러와서 이어서 게임을 할수가 있다.

혹은 파일을 편집하다가 ctrl+z 등으로 수정했던 전 단계로 돌아갈 수 있다.

이렇게 자신이 원하는 시점 혹은 버전으로 이동할 수 있게 해주는 것이 `버전관리`이고, 이를 도와주는 툴을 `버전관리시스템` 이라고 한다. ( 형상관리, 형상관리시스템, 형상관리 툴 )

보통 혼자 프로젝트를 진행하면 버전관리가 나름 용이하겠지만, 여러명이 함께 한 프로젝트를 진행한다면, <br>
여러명이 동시에 같은 버전으로 커밋을 하거나, <br> 
프로젝트 인원 수 혹은 프로젝트 기간이 연장되는 경우도 있을 것이다.<br>
이렇게 된다면 최종버전이 무엇인지도 헷갈리게 되고, 결론적으로 버전을 관리하는게 까다로울 것이다. 

이 때 관리를 용이하게 해주기 위해 사용하는 것이 버전관리이며, 버전관리시스템이다.

버전관리 툴은 `GitHub`, `GitLab`, `BitBucket` 등이 있다.

### 💡 기본적인 용어
    1. 워킹트리 (working tree) ⇒ 
        - 커밋을 체크아웃하면 생성되는 파일과 디렉토리.
            (작업폴더에서 [.git]폴더 (로컬저장소) 를 제외한 나머지 부분.
        - 사용자가 파일과 하위 폴더를 만들고 작업 결과물을 저장하는 곳
    2. 로컬저장소 (local repository) ⇒
        - Git init 명령으로 생성되는 [.git] 폴더가 로컬저장소이다.
    3. 원격저장소 (remote repository) ⇒
        - 로컬저장소를 업로드하는 곳. (GitHub, BitBucket 등)
    4. Git 저장소 ⇒
        - 일반적으로 Git 명령으로 관리할 수 있는 폴더 전체를 뜻한다.









