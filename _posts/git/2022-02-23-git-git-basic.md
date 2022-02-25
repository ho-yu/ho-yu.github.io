---
title: '[Git] Git (1) '
author: ho-yu
date: 2022-02-23 18:15:21 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

## Introduction
들어가기전에 버전관리가 무엇인지 알아보자.

RPG 게임을 예를 들면, 한 캐릭터로 게임을 진행하다가 게임을 종료하기 전에 지금까지 진행한 게임데이터를 저장을 한다. 그리고 나중에 저장한 데이터를 불러와서 이어서 게임을 할수가 있다.

혹은 파일을 편집하다가 ctrl+z 등으로 수정했던 전 단계로 돌아갈 수 있다.

이렇게 자신이 원하는 시점 혹은 버전으로 이동할 수 있게 해주는 것이 `버전관리`이고, 이를 도와주는 툴을 `버전관리시스템` 이라고 한다. ( 형상관리, 형상관리시스템, 형상관리 툴 )

보통 혼자 프로젝트를 진행하면 버전관리가 나름 용이하겠지만, 여러명이 함께 한 프로젝트를 진행한다면, <br>
여러명이 동시에 같은 버전으로 커밋을 하거나, <br> 
프로젝트 인원 수 혹은 프로젝트 기간이 연장되는 경우도 있을 것이다.<br>
이렇게 된다면 최종버전이 무엇인지도 헷갈리게 되고, 결론적으로 버전을 관리하는게 까다로울 것이다. 

이 때 관리를 용이하게 해주기 위해 사용하는 것이 버전관리이며, 버전관리시스템이다.

버전관리 툴은 `GitHub`, `GitLab`, `BitBucket` 등이 있다.

## 💡 기본적인 용어
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

## 계정정보인증

#### Git 계정정보인증관련 명령어이다.

주로 <br>
1.  Github에서 비밀번호를 변경했는데, local git에 저장된 인증정보를 수정하지 않은 경우.
2.  local git에 인증정보를 저장할 때, 정보를 잘못입력했을 경우<br>

등의 원인으로 발생하는 오류를 해결할 때 도움이 되었어서 추가정리를 해봤다. 😊

### 💡 인증관련 명령어
- `git config --local credential.helper`
- `git config --global credential.helper`
- `git config --system credential.helper`
- `git config credential.helper "cache --timeout=30"`
    - 30초간 아이디 및 패스워드 설정.
- `git config credential.helper store`
    - 인증 방식 store로 변경.
- `git config --unset credential.helper`
    - 옵션 삭제.
- `file ~/.git-credentials`
    - 인증파일 정보 확인.
- `rm ~/.git-credentials`
    - 인증파일 삭제.

### 💡 옵션설정관련 명령어
    코드의 { }, [ ] 등과 같은 괄호들은 구분이 용이하도록 작성한 것 이므로, 괄호는 제거하고 입력해야한다.  

- `git config --global {옵션명}`
    - 지정한 전역 옵션의 내용을 보여줘 !
- `git config --global {옵션명} {새로운 값}`
    - 지정한 전역 옵션의 값을 새로 설정해줘 !
- `git config --global --unset {옵션명}`
    - 지정한 전역 옵션을 삭제해줘 !
- `git config --local {옵션명}`
    - 지정한 지역 옵션의 내용을 보여줘 !
- `git config --local {옵션명} {새로운 값}`
    - 지정한 지역 옵션의 값을 새로 설정해줘 !
- `git config --local --unset {옵션명}`
    - 지정한 지역 옵션의 값을 삭제해줘 !
- `git config --system {옵션명}`
    - 지정한 시스템 옵션의 내용들을 보여줘 !
- `git config --system {옵션명} {값}`
    - 지정한 시스템 옵션의 값을 새로 설정해줘 !
- `git config --system --unset {옵션명} {값}`
    - 지정한 시스템 옵션의 값을 삭제해줘 !
- `git config --list`
<br><br>

위에서 local, global, system은 범위를 의미한다. <br>
(우선순위 = local > global > system)
- local : 특정 저장소.
- global : 특정 사용자. 
- system : 시스템의 모든 사용자와 저장소

보통 local과 global을 사용해도 충분하지만, <br>
자신의 원인을 파악한 후에, 적용 범위를 잘 선택해서 진행하면 될 것이다.








