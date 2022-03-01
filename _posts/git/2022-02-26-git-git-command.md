---
title: '[Git] Git (2) '
author: ho-yu
date: 2022-02-26 15:59:57 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

![git](https://user-images.githubusercontent.com/64628448/155834033-6e1dbb9a-3531-47c9-805f-6ed3ffa34702.png){: width="75%"}

# 📚 Introduction

자주 사용하는 기본적인 명령어들을 정리해봤다.

# 💥 Git 기본명령어
<br>

- `git init`
    - Git 저장소 생성해줘 ! ( Git 초기화 과정 )
        
        ( 터미널 혹은 cmd로 해당 폴더로 이동 후 위 명령어를 입력하면, 해당 폴더에서 버전관리를 할 수 있다. )
        
- `git config --global user.email “yourEmail”
 git config --global user.name “yourName”`
    
    ex) `git config --global[user.email](http://user.email)“Ho@gmail.com”`,<br> 
    `git config --global [user.name](http://user.name) “Ho”`
    
    위 두 명령어는 버전관리시스템에서 보여질 내 이메일과 이름을 설정한다.
    
- `git status`
    - Git working tree의 상태를 보여줘 !
    - `git status -s` ⇒
        
        working tree의 상태를 짧게 요약해서 보여줘 ! ( 변경된 상태가 많을 때 유용 )
        
- `git add`
    - 이 커밋을 스테이지에 올려줘 !
- `git commit`
    - 스테이지에 있는 파일들을 커밋해줘 !
    - `git commit -a`
        - add 명령 생략하고 바로 커밋할게 !
            
            ( 변경된 파일과 삭제된 파일은 자동으로 스테이징되고 커밋된다. )
            
            ( Untracked 파일은 커밋되지 않는다. )
            
    - `git commit -m “commit message”`
        - 커밋메세지는 이렇게 할테니까 커밋해줘 !
- `git log`
    - 지금까지 만든 커밋 이력을 보여줘! ( 오름차순으로 가장 최근 내역 )
    - `git log` 명령어 옵션
        - `git log -p -5` ⇒
            
            `-p` 옵션은 각 커밋의 차이점 결과를 보여주고, 
            
            `-[숫자]` 옵션은 최근 몇개의 이력을 보여줄 것인지 지정하는 것.
            
        - `git log --stat` ⇒
            
            `--stat` 옵션은 각 커밋의 수정내역과 요약정보 등, 대략적인 통계정보를 볼 수 있다.
            
        - `git log --pretty` ⇒
            
            `--pretty` 옵션은 다양한 형식으로 커밋메세지를 볼 수 있는데, 부가옵션을 추가할 수 있다.
            
            - `git log --pretty=oneline` ⇒
                
                oneline 옵션은 커밋을 한줄로 표현해주며, short, full, fuller 옵션은 각 단계에 따라 정보들을 추가적으로 보여준다.
                
        - `git log --graph` ⇒
            
            커밋 기록을 그래프 형식으로 보여줘 !
            
        - `git log --oneline` ⇒
            
            커밋 해시와 제목만 보여줘 !
            
        - `git log --online --graph --decorate` ⇒
            
            HEAD와 관련된 커밋들을 좀 더 자세히 보여줘 !
            
        - `git log --oneline --graph --all --decorate` ⇒
            
            모든 브랜치의 이력을 보여줘 !
            
        - `git log --oneline -5` ⇒
            
            내 브랜치의 최신 커밋 5개만 보여줘 !
            
        
- `git checkout [commitId]`
    - 내가 지정한 커밋 위치로 이동해줘 ! ( commitId = commitId 앞 7자리만으로도 가능 )
    
    `git checkout -` ⇒
    
    - 최근 커밋 위치로 이동해줘 !
- `git remote add [원격저장소 이름] [원격저장소 주소]`
    - 로컬저장소야! 내 원격저장소 주소를 알려줄게 ! ( 로컬저장소와 원격저장소 연동개념 )
    - `git remote -v`
        
        원격저장소 목록을 조회해줘 !
        
- `git clone [원격저장소 주소] [새로운 폴더명]`
    - 저장소 주소에서 프로젝트를 복제해서 가져와줘 !
        
        ( 저장소 주소는 꼭 원격일 필요가 없으며, 로컬저장소도 git clone으로 가능하다. )
        
- `git push [-u] [원격저장소 이름] [브랜치 이름]`
    - 현재 브랜치에서 새로 생성한 커밋들을 원격저장소에 올려줘 !
        
        ( -u 옵션으로 브랜치의 업스트림을 등록할 수 있다. )
        
        ( 한 번 등록한 후에는 `git push` 만 입력해도 된다. )
        
    
    ex) `git push -u origin master`  
    
    커밋한 내용을 원격저장소의 master branch에  올려줘 ! 
    
    ( 여기서 origin은 원격저장소를 의미하며, master는 해당 원격저장소의 branch를 의미 )
    
- `git fetch [원격저장소 이름] [브랜치 이름]`
    - 원격저장소의 브랜치와 커밋들을 로컬저장소와 동기화한다.
    - 옵션을 생략하면 모든 원격저장소에서 모든 브랜치를 가져온다.
- `git merge [브랜치 이름]`
    - 지정한 브랜치의 커밋들을 현재 브랜치 및 워킹트리에 반영한다.
- `git pull`
    - 원격저장소에 새로운 커밋이 있으면, 내 로컬저장소로 가져와줘 !
        
        ( `git fetch` + `git merge` 와 동일한 결과이다. )
        
- `git clone [원격저장소 주소]`
    - 원격저장소의 커밋을 로컬저장소로 옮겨줘 !
    
    > git clone 명령어 뒤에 원격저장소 주소를 적고 한 칸 띄고 마침표를 찍어야 현재 폴더에 저장된다.
    > 
    
    ( GitHub에 Download Zip 으로도 소스를 받을 수 있지만, 원격저장소와 버전 정보가 제외되므로, 원격저장소에 있는 소스코드로 작업을 이어서 할 목적이면 clone하는게 간편하다. )
    
- `git reset [파일명]`
    - 스테이지 영역에 있는 파일들을 스테이지에서 내려줘 ! ( Unstaging )
    -   워킹트리의 내용은 변경되지 않으며, 옵션을 생략할 경우 스테이지의 모든 변경사항을 초기화한다.
<br><br>

# 💥 branch 관련 명령어
<br>

## 🛎 HEAD에 대해 반드시 기억할 점    

    1. HEAD는 현재 작업 중인 브랜치를 가리킨다. 
    2. 브랜치는 커밋을 가리키므로 HEAD도 커밋을 가리킨다.
    3. 결국 HEAD는 현재 작업 중인 브랜치의 최근 커밋을 가리킨다.
<br>

## 🛎 HEAD~, HEAD^

    1. HEAD~[숫자]
    ⇒ HEAD~은 HEAD의 부모 커밋, HEAD~2는 헤드의 할아버지 커밋을 말한다.
    HEAD~n은 n번째 위쪽 조상이라는 뜻이다.
    
    2. HEAD^[숫자]
    ⇒ HEAD^은 똑같이 부모 커밋이다. 반면 HEAD^2는 두 번째 부모를 가리킨다.
    병합 커밋처럼 부모가 둘 이상인 커밋에서만 의미가 있다.

- `git branch [-v]`
    - 로컬 저장소의 브랜치 목록을 보여줘 !
        - `-v` 옵션을 사용하면 마지막 커밋도 함께 보여준다.
- `git branch [브랜치 이름]`
    - 지정한 이름으로 브랜치 만들어줘 !
    - 추가 예시 )
        - `git checkout -b feature1`
            - ⇒ feature1 브랜치 생성 및 체크아웃
        - `git checkout -b hotfix master`
            - ⇒ master 브랜치로부터 hotfix 브랜치 생성 및 체크아웃
- `git branch [-f] [브랜치 이름] [커밋체크섬]`
    - 새로운 브랜치를 만들어줘 !
        - 커밋 체크섬 값을 주지 않으면 HEAD로부터 브랜치를 생성한다.
        - 이미 있는 브랜치를 다른 커밋으로 옮기고 싶을 때는 `-f` 옵션을 줘야 한다.
- `git branch -r[v]`
    - 원격저장소에 있는 브랜치를 보여줘 !
        - `-v` 옵션을 추가해서 커밋 요약도 볼 수 있다.
- `git checkout [브랜치 이름]`
    - 특정 브랜치로 체크아웃해줘 !
- `git checkout -b [브랜치 이름] [커밋체크섬]`
    - 특정 커밋에서 브랜치만들고 체크아웃까지 해줘 !
- `git merge [대상 브랜치]`
    - 현재 브랜치와 대상 브랜치를 병합해줘 !
        - 병합 커밋 (merge commit) 이 새로 생기는 경우가 많다.
- `git rebase [대상 브랜치]`
    - 내 브랜치의 커밋들을 대상 브랜치에 재배치 해줘 !
        - 재배치 대상 커밋이 여러개일 경우, 여러번 충돌이 발생할 수 있다.
        - 기존의 커밋을 하나씩 단계별로 수정한다. 충돌이 없어질 때까지 `git rebase --continue` 명령을 매번 입력해줘야 한다.
        - 충돌이 발생하기 전 상태로 돌리고 싶을 때는, `git rebase --abort` 로 돌릴 수 있다.
    
    >💡 <rebase 주의사항><br>
        1. 원격 저장소에 push한 브랜치는 rebase하지 않는 것이 원칙이다.
    
- `git branch -d [브랜치 이름]`
    - 특정 브랜치를 삭제해줘 !
        - HEAD 브랜치나 병합이 되지 않은 브랜치는 삭제할 수 없다.
- `git branch -D [브랜치 이름]`
    - 지정한 브랜치 강제로 삭제해줘 !
        - `-d` 옵션으로 삭제할 수 없는 브랜치를 지우고 싶을 때 사용한다.
- `git reset --hard [이동할 커밋체크섬]`
    - 현재 브랜치를 지정한 커밋으로 옮긴다. (작업 폴더의 내용도 함께 변경된다.)
<br>
<br>

## 💥 배포 버전에 태깅하기
- `git tag -a -m [간단한 메세지] [태그 이름] [브랜치 or 커밋체크섬]`
- `-a` 로 주석 있는(annotated) 태그를 생성해줘 !
    - 메세지와 태그 이름은 필수, 브랜치 이름을 생략하면 HEAD에 태그를 생성한다.
- `git push [원격저장소 별명] [태그 이름]`
    - 원격 저장소에 태그를 업로드 해줘 !



