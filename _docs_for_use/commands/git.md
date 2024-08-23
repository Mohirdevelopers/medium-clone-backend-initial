# Git Buyruqlari

Ushbu qo'llanma Git versiya nazorati tizimi bilan ishlash uchun asosiy buyruqlarni o'z ichiga oladi.

## Git Konfiguratsiyasi

- **Git konfiguratsiyasini sozlash:**

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

## Git Repozitoriyasini Ishga Tushirish

- **Yangi Git repozitoriyasini yaratish:**

    ```bash
    git init
    ```

- **Mavjud repozitoriyani klonlash:**

    ```bash
    git clone <repository_url>
    ```

## Git Statusi va Ma'lumotlarni Ko'rsatish

- **Git statusini ko'rsatish (o'zgarishlar va mavjud fayllar):**

    ```bash
    git status
    ```

- **Git repozitoriyasi haqida ma'lumot olish:**

    ```bash
    git info
    ```

## O'zgarishlarni Boshqarish

- **O'zgarishlarni qo'shish (staging area):**

    ```bash
    git add .
    ```

- **O'zgarishlarni commit qilish:**

    ```bash
    git commit -m "Commit message"
    ```

- **O'zgarishlarni commit va yangi branch yaratish:**

    ```bash
    git checkout -b <branch_name>
    ```

- **O'zgarishlarni so'nggi commitga qaytarish:**

    ```bash
    git reset --hard HEAD
    ```

## Branchlar Bilan Ishlash

- **Yangi branch yaratish:**

    ```bash
    git branch <branch_name>
    ```

- **Branchni o'zgartirish:**

    ```bash
    git checkout <branch_name>
    ```

- **Branchlarni ko'rsatish:**

    ```bash
    git branch
    ```

- **Branchni o'chirish:**

    ```bash
    git branch -d <branch_name>
    ```

## Git Loglari va Tarixni Ko'rsatish

- **Commit tarixini ko'rsatish:**

    ```bash
    git log
    ```

- **O'zgarishlar tarixini qisqacha ko'rsatish:**

    ```bash
    git log --oneline
    ```

## Git Repozitoriyasiga O'zgarishlarni Push va Pull Qilish

- **O'zgarishlarni remote repozitoriyaga push qilish:**

    ```bash
    git push origin <branch_name>
    ```

- **Remote repozitoriyadan o'zgarishlarni olish (pull qilish):**

    ```bash
    git pull origin <branch_name>
    ```

- **Git konfiguratsiyasini ko'rsatish:**

    ```bash
    git config --list
    ```

## Git Repozitoriyasini Tozalash va O'chirish

- **Katta fayl o'zgartirishlarini tarixdan olib tashlash:**

    ```bash
    git filter-branch --tree-filter 'rm -f <file>' HEAD
    ```

- **Git tarixini qayta yozish va tozalash:**

    ```bash
    git rebase -i <commit_id>
    ```

## Gitning Boshqa Buyruqlari

- **O'zgarishlarni sahifalash:**

    ```bash
    git stash
    ```

- **Sahifalangan o'zgarishlarni qaytarish:**

    ```bash
    git stash pop
    ```

- **Remote repozitoriyalar ro'yxatini ko'rsatish:**

    ```bash
    git remote -v
    ```

- **Remote repozitoriyani qo'shish:**

    ```bash
    git remote add <remote_name> <remote_url>
    ```

- **Remote repozitoriyani o'chirish:**

    ```bash
    git remote remove <remote_name>
    ```

**Git bilan ishlashni samarali boshqarish uchun ushbu buyruqlardan foydalaning. Repozitoriyalarni yaratish, branchlar bilan ishlash va o'zgarishlarni boshqarish uchun barcha buyruqlarni bilish muhimdir.**
