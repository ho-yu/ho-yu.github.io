---
title: '[Git] Git (1) '
author: ho-yu
date: 2022-02-23 18:15:21 +0900
categories: [Study, Git]
tags: [git, sourcetree]
---

![git](https://user-images.githubusercontent.com/64628448/155834033-6e1dbb9a-3531-47c9-805f-6ed3ffa34702.png){: width="75%"}

# π Introduction
λ€μ΄κ°κΈ°μ μ λ²μ κ΄λ¦¬κ° λ¬΄μμΈμ§ μμλ³΄μ.

RPG κ²μμ μλ₯Ό λ€λ©΄, ν μΊλ¦­ν°λ‘ κ²μμ μ§ννλ€κ° κ²μμ μ’λ£νκΈ° μ μ μ§κΈκΉμ§ μ§νν κ²μλ°μ΄ν°λ₯Ό μ μ₯μ νλ€. κ·Έλ¦¬κ³  λμ€μ μ μ₯ν λ°μ΄ν°λ₯Ό λΆλ¬μμ μ΄μ΄μ κ²μμ ν μκ° μλ€.

νΉμ νμΌμ νΈμ§νλ€κ° ctrl+z λ±μΌλ‘ μμ νλ μ  λ¨κ³λ‘ λμκ° μ μλ€.

μ΄λ κ² μμ μ΄ μνλ μμ  νΉμ λ²μ μΌλ‘ μ΄λν  μ μκ² ν΄μ£Όλ κ²μ΄ `λ²μ κ΄λ¦¬`μ΄κ³ , μ΄λ₯Ό λμμ£Όλ ν΄μ `λ²μ κ΄λ¦¬μμ€ν` μ΄λΌκ³  νλ€. ( νμκ΄λ¦¬, νμκ΄λ¦¬μμ€ν, νμκ΄λ¦¬ ν΄ )

λ³΄ν΅ νΌμ νλ‘μ νΈλ₯Ό μ§ννλ©΄ λ²μ κ΄λ¦¬κ° λλ¦ μ©μ΄νκ² μ§λ§, μ¬λ¬λͺμ΄ ν¨κ» ν νλ‘μ νΈλ₯Ό μ§ννλ€λ©΄, <br>
μ¬λ¬λͺμ΄ λμμ κ°μ λ²μ μΌλ‘ μ»€λ°μ νκ±°λ, <br> 
νλ‘μ νΈ μΈμ μ νΉμ νλ‘μ νΈ κΈ°κ°μ΄ μ°μ₯λλ κ²½μ°λ μμ κ²μ΄λ€.<br>
μ΄λ κ² λλ€λ©΄ μ΅μ’λ²μ μ΄ λ¬΄μμΈμ§λ ν·κ°λ¦¬κ² λκ³ , κ²°λ‘ μ μΌλ‘ λ²μ μ κ΄λ¦¬νλκ² κΉλ€λ‘μΈ κ²μ΄λ€. 

μ΄ λ κ΄λ¦¬λ₯Ό μ©μ΄νκ² ν΄μ£ΌκΈ° μν΄ μ¬μ©νλ κ²μ΄ λ²μ κ΄λ¦¬μ΄λ©°, λ²μ κ΄λ¦¬μμ€νμ΄λ€.

λ²μ κ΄λ¦¬ ν΄μ `GitHub`, `GitLab`, `BitBucket` λ±μ΄ μλ€.

# π₯ κΈ°λ³Έμ μΈ μ©μ΄
    1. μνΉνΈλ¦¬ (working tree) β 
        - μ»€λ°μ μ²΄ν¬μμνλ©΄ μμ±λλ νμΌκ³Ό λλ ν λ¦¬.
            (μμν΄λμμ [.git]ν΄λ (λ‘μ»¬μ μ₯μ) λ₯Ό μ μΈν λλ¨Έμ§ λΆλΆ.
        - μ¬μ©μκ° νμΌκ³Ό νμ ν΄λλ₯Ό λ§λ€κ³  μμ κ²°κ³Όλ¬Όμ μ μ₯νλ κ³³
    2. λ‘μ»¬μ μ₯μ (local repository) β
        - Git init λͺλ ΉμΌλ‘ μμ±λλ [.git] ν΄λκ° λ‘μ»¬μ μ₯μμ΄λ€.
    3. μκ²©μ μ₯μ (remote repository) β
        - λ‘μ»¬μ μ₯μλ₯Ό μλ‘λνλ κ³³. (GitHub, BitBucket λ±)
    4. Git μ μ₯μ β
        - μΌλ°μ μΌλ‘ Git λͺλ ΉμΌλ‘ κ΄λ¦¬ν  μ μλ ν΄λ μ μ²΄λ₯Ό λ»νλ€.

# π₯ κ³μ μ λ³΄μΈμ¦

μ£Όλ‘ <br>
1.  Githubμμ λΉλ°λ²νΈλ₯Ό λ³κ²½νλλ°, local gitμ μ μ₯λ μΈμ¦μ λ³΄λ₯Ό μμ νμ§ μμ κ²½μ°.
2.  local gitμ μΈμ¦μ λ³΄λ₯Ό μ μ₯ν  λ, μ λ³΄λ₯Ό μλͺ»μλ ₯νμ κ²½μ°<br>

λ±μ μμΈμΌλ‘ λ°μνλ μ€λ₯λ₯Ό ν΄κ²°ν  λ λμμ΄ λμμ΄μ μΆκ°μ λ¦¬λ₯Ό ν΄λ΄€λ€. π

## π₯ μΈμ¦κ΄λ ¨ λͺλ Ήμ΄
- `git config --local credential.helper`
- `git config --global credential.helper`
- `git config --system credential.helper`
- `git config credential.helper "cache --timeout=30"`
    - 30μ΄κ° μμ΄λ λ° ν¨μ€μλ μ€μ .
- `git config credential.helper store`
    - μΈμ¦ λ°©μ storeλ‘ λ³κ²½.
- `git config --unset credential.helper`
    - μ΅μ μ­μ .
- `file ~/.git-credentials`
    - μΈμ¦νμΌ μ λ³΄ νμΈ.
- `rm ~/.git-credentials`
    - μΈμ¦νμΌ μ­μ .

## π₯ μ΅μμ€μ κ΄λ ¨ λͺλ Ήμ΄
    μ½λμ { }, [ ] λ±κ³Ό κ°μ κ΄νΈλ€μ κ΅¬λΆμ΄ μ©μ΄νλλ‘ μμ±ν κ² μ΄λ―λ‘, κ΄νΈλ μ κ±°νκ³  μλ ₯ν΄μΌνλ€.  

- `git config --global {μ΅μλͺ}`
    - μ§μ ν μ μ­ μ΅μμ λ΄μ©μ λ³΄μ¬μ€ !
- `git config --global {μ΅μλͺ} {μλ‘μ΄ κ°}`
    - μ§μ ν μ μ­ μ΅μμ κ°μ μλ‘ μ€μ ν΄μ€ !
- `git config --global --unset {μ΅μλͺ}`
    - μ§μ ν μ μ­ μ΅μμ μ­μ ν΄μ€ !
- `git config --local {μ΅μλͺ}`
    - μ§μ ν μ§μ­ μ΅μμ λ΄μ©μ λ³΄μ¬μ€ !
- `git config --local {μ΅μλͺ} {μλ‘μ΄ κ°}`
    - μ§μ ν μ§μ­ μ΅μμ κ°μ μλ‘ μ€μ ν΄μ€ !
- `git config --local --unset {μ΅μλͺ}`
    - μ§μ ν μ§μ­ μ΅μμ κ°μ μ­μ ν΄μ€ !
- `git config --system {μ΅μλͺ}`
    - μ§μ ν μμ€ν μ΅μμ λ΄μ©λ€μ λ³΄μ¬μ€ !
- `git config --system {μ΅μλͺ} {κ°}`
    - μ§μ ν μμ€ν μ΅μμ κ°μ μλ‘ μ€μ ν΄μ€ !
- `git config --system --unset {μ΅μλͺ} {κ°}`
    - μ§μ ν μμ€ν μ΅μμ κ°μ μ­μ ν΄μ€ !
- `git config --list`
<br><br>

μμμ local, global, systemμ λ²μλ₯Ό μλ―Ένλ€. <br>
(μ°μ μμ = local > global > system)
- local : νΉμ  μ μ₯μ.
- global : νΉμ  μ¬μ©μ. 
- system : μμ€νμ λͺ¨λ  μ¬μ©μμ μ μ₯μ

λ³΄ν΅ localκ³Ό globalμ μ¬μ©ν΄λ μΆ©λΆνμ§λ§, <br>
μμ μ μμΈμ νμν νμ, μ μ© λ²μλ₯Ό μ μ νν΄μ μ§ννλ©΄ λ  κ²μ΄λ€.








