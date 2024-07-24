# Medium Clone Loyihasi

## Umumiy Ma'lumot

Bu Django loyihasi Docker va lokalni uchun sozlangan. Ushbu qo'llanma sizga lokal muhitni sozlash va loyihani ishga tushirishga yordam beradi.

## Talablar

- Docker
- Docker Compose
- Python 3.x

## Sozlash

### `.env` Faylini Yaratish

1. Loyihaning asosiy papkasida `.env` nomli fayl yarating.

2. `.env` fayliga quyidagi muhit o'zgaruvchilarini qo'shing:

    ```env
    SECRET_KEY=g7df7fg8hgfdg9fdg8d7fg567sd5f098dfg7df
    DEBUG=True
    DB_ENGINE=django.db.backends.sqlite3
    DB_NAME=db.sqlite3
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    ```
 3. Pre commit hookni o'rnatish (Ixtiyoriy)

    Siz pre-commit hookni o'rnatish orqali kodlaringizni git orqali kommit qilishdan oldin bir nechta avtomatik tekshiruvlardan o'tkazishingiz mumkin. Masalan: migratsiyalarni tekshirish, kodlardagi xatoliklarni aniqlash, kodlarni qayta formatlash va hokazo. Ushbu tekshiruvlarni bajarish buyruqlar .pre-commit-config.yaml faylida yozilgan.

    Pre-commit hookni o'rnatish buyurug'i:
    ```
    pre-commit install
    ```

### Docker Compose-ni Ishga Tushurish

1. Kompyuteringizda Docker va Docker Compose o'rnatilganligini tekshiring.

2. Loyihaning asosiy papkasida quyidagi buyruqni bajaring:

    ```bash
    docker-compose up --build
    ```

   Bu buyruq sizning `docker-compose.yml` faylingizda belgilangan konteynerlarni quradi va ishga tushiradi.

3. Konteynerlarni fon rejimida (background) ishga tushurish uchun:

    ```bash
    docker-compose up -d --build
    ```

4. Konteynerlarni to'xtatish va o'chirish uchun:

    ```bash
    docker-compose down
    ```

### Django-ni Lokalda Ishga Tushurish

Agar Django-ni Docker orqali emas, balki lokalda ishga tushirmoqchi bo'lsangiz, quyidagi amallarni bajaring:

1. Virtual muhit yaratish va faollashtirish:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows uchun `venv\Scripts\activate` foydalaning
    ```

2. Loyihaning kutubxonalarini o'rnatish:

    ```bash
    pip install -r requirements.txt
    ```

3. Migratsiyalarni qo'llash:

    ```bash
    python manage.py migrate
    ```

4. Superuser yaratish (agar kerak bo'lsa):

    ```bash
    python manage.py createsuperuser
    ```

5. Django rivojlantirish serverini ishga tushurish:

    ```bash
    python manage.py runserver
    ```

   Server `http://127.0.0.1:8000/` manzilida ishlaydi.
