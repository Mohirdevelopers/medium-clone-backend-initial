# PostgreSQL Buyruqlari

Ushbu qo'llanma PostgreSQL ma'lumotlar bazasi bilan ishlash uchun Windows va Unix-ga o'xshash tizimlarda (MacOS) asosiy buyruqlarni o'z ichiga oladi.

## Unix-ga O'xshash Tizimlarda (MacOS)

### PostgreSQL Serverini Ishga Tushirish

### MacOS uchun `sudo` o'rniga `brew` ishlatishingiz mumkin.

- **PostgreSQL serverini ishga tushirish:**

    ```bash
    sudo service postgresql start
    ```

- **PostgreSQL serverini to'xtatish:**

    ```bash
    sudo service postgresql stop
    ```

- **PostgreSQL serverini qayta ishga tushirish:**

    ```bash
    sudo service postgresql restart
    ```

### PostgreSQL bilan O'zaro Aloqa

- **PostgreSQL interaktiv buyruq satrini ishga tushirish (psql):**

    ```bash
    psql -U <username> -d <database_name>
    ```

- **Foydalanuvchilar va ma'lumotlar bazalari ro'yxatini ko'rsatish:**

    ```bash
    \l
    ```

- **Ma'lumotlar bazasi bilan ishlash:**

    ```bash
    \c <database_name>
    ```

### Ma'lumotlar Bazasi Bilan Ishlash

- **Yangi ma'lumotlar bazasini yaratish:**

    ```bash
    createdb <database_name>
    ```

- **Ma'lumotlar bazasini o'chirish:**

    ```bash
    dropdb <database_name>
    ```

- **Yangi foydalanuvchi yaratish:**

    ```bash
    createuser <username>
    ```

- **Foydalanuvchini o'chirish:**

    ```bash
    dropuser <username>
    ```

### SQL Buyruqlari

- **Jadval yaratish:**

    ```sql
    CREATE TABLE <table_name> (
        <column_name> <data_type> [constraints],
        ...
    );
    ```

- **Jadvalga yangi satr qo'shish:**

    ```sql
    INSERT INTO <table_name> (<column1>, <column2>, ...)
    VALUES (<value1>, <value2>, ...);
    ```

- **Jadvaldagi ma'lumotlarni o'qish:**

    ```sql
    SELECT <column1>, <column2>, ...
    FROM <table_name>
    WHERE <condition>;
    ```

- **Jadvaldagi ma'lumotlarni yangilash:**

    ```sql
    UPDATE <table_name>
    SET <column1> = <value1>, <column2> = <value2>, ...
    WHERE <condition>;
    ```

- **Jadvaldagi ma'lumotlarni o'chirish:**

    ```sql
    DELETE FROM <table_name>
    WHERE <condition>;
    ```

- **Jadvalni o'chirish:**

    ```sql
    DROP TABLE <table_name>;
    ```

### Ma'lumotlarni Backup va Restore

- **Ma'lumotlarni backup qilish:**

    ```bash
    pg_dump <database_name> > <backup_file>.sql
    ```

- **Ma'lumotlarni restore qilish:**

    ```bash
    psql <database_name> < <backup_file>.sql
    ```

### Indekslar Bilan Ishlash

- **Indeks yaratish:**

    ```sql
    CREATE INDEX <index_name>
    ON <table_name> (<column_name>);
    ```

- **Indeksni o'chirish:**

    ```sql
    DROP INDEX <index_name>;
    ```

### Ma'lumotlar Bazasi Ma'lumotlarini Tekshirish

- **Ma'lumotlar bazasidagi jadval ro'yxatini ko'rsatish:**

    ```bash
    \dt
    ```

- **Jadvalning tuzilmasini ko'rsatish:**

    ```bash
    \d <table_name>
    ```

- **Jadvaldagi barcha ma'lumotlarni ko'rsatish:**

    ```sql
    SELECT * FROM <table_name>;
    ```

**PostgreSQL bilan ishlashni samarali boshqarish uchun ushbu buyruqlardan foydalaning. Ma'lumotlar bazasini yaratish, boshqarish va ma'lumotlarni saqlash uchun barcha buyruqlarni bilish muhimdir.**
