# **PIP Buyruqlari**

Ushbu qo'llanma Python paketlarini boshqarish uchun umumiy PIP buyruqlarini mavjud.

- **Paketini o'rnatish:**
    ```bash
    pip install package-name
    ```

    Ushbu buyruq belgilangan Python paketini o'rnatadi.

- **requirements.txt faylni yaratish yoki yangilash:**
    ```bash
    pip freeze > requirements.txt
    ```

- **Barcha paketlarni yangilashga harakat qilish:**
    ```bash
    pip install --upgrade $(pip freeze | cut -d '=' -f 1)
    ```

    Ushbu buyruq barcha o'rnatilgan paketlarni so'nggi versiyalariga yangilashga harakat qiladi. U dastlab `pip freeze` yordamida hozirda o`rnatilgan paketlar ro`yxatini (ularning versiyalaridan tashqari) yaratadi, so`ngra ularni `pip install --upgrade` yordamida yangilashga harakat qiladi.

- **Muayyan paket versiyasini o'rnatish:**
    ```bash
    pip install package-name==version
    ```

- **Paketni o'chirish:**
    ```bash
    pip uninstall package-name
    ```

- **O'rnatilgan paketlar ro'yxati:**
    ```bash
    pip list
    ```

- **Paketlarni qidiring:**
    ```bash
    pip search search-term
    ```

    Ushbu buyruq Python paket indeksini (PyPI) ko'rsatilgan qidiruv so'ziga mos keladigan paketlarni qidiradi.

- **Paket haqida ma'lumotni ko'rsatish:**
    ```bash
    pip show package-name
    ```

- **Paketni requirements faylidan o'rnatish:**
    ```bash
    pip install -r requirements.txt
    ```

    Ushbu buyruq talablar.txt faylida ko'rsatilgan barcha paketlarni o'rnatadi.

- **Paketlarni global o'rnating:**
    ```bash
    pip install package-name --user
    ```

    Ushbu buyruq joriy foydalanuvchi uchun belgilangan paketni global miqyosda o'rnatadi. Agar sizda ma'muriy imtiyozlar bo'lmasa yoki paketlarni tizim Python o'rnatilishidan alohida saqlashni xohlasangiz foydali bo'ladi.

- **Paketlarni ma'lum bir katalogga o'rnating:**
    ```bash
    pip install package-name --target /path/to/directory
    ```
