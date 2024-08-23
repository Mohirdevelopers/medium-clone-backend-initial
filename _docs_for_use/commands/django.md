# Django Buyruqlari

Ushbu qo'llanmada Django yordamida testlarni o'tkazish uchun turli buyruqlar keltirilgan.

- **Serverini ishga tushirish**
    ```
    python manage.py runserver
    ```

- **Migratsiyalarni amalga oshiring (agar sizda modellar mavjud bo'lsa)**
    ```
    python manage.py makemigrations
    ```

- **Ma'lumotlar bazasiga migratsiyalarni qo'llash**
    ```
    python manage.py migrate
    ```

- **Statik fayllarni to'plash (loyihangizda statik fayllar mavjud bo'lsa)**
    ```
    python manage.py collectstatic
    ```

- **Superuser yaratish ("foydalanuvchi nomi" va "parol" ni o'zingiz xohlagan ma'lumotlari bilan almashtiring)**
    ```
    python manage.py createsuperuser username password
    ```

- **Django muhiti ishga tushirish**
    ```
    python manage.py shell
    ```

- **Testlarni ishga tushiring (agar sizda pytest testlar yozilgan bo'lsa)**
    ```
    pytest
    ```

- **Loyiha muammolarini tekshiring**
    ```
    python manage.py check
    ```

- **Qurilma maʼlumotlarini maʼlumotlar bazasiga yuklang**
    ```
    python manage.py loaddata mydata.json
    ```

- **Ma'lumotlar bazasini dump qilish**
    ```
    python manage.py dumpdata > mydata.json
    ```
