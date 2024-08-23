# Pytest Buyruqlari

Ushbu qo'llanma pytest yordamida testlarni ishga tushirish uchun turli xil buyruqlarni keltiradi.

- **Pytest-ni ishga tushirish:**
    ```bash
    pytest
    ```

- **Ma'lum bir papkada barcha testlarni ishga tushirish:**
    ```bash
    pytest path/to/directory
    ```

- **Ma'lum bir fayldagi testlarni ishga tushirish:**
    ```bash
    pytest path/to/test_file.py
    ```

- **Ma'lum bir test funktsiyasini ishga tushirish:**
    ```bash
    pytest path/to/test_file.py::test_function
    ```

- **Pytest-ni markerlar bilan ishga tushirish:**
    ```bash
    pytest -m <marker>
    pytest -m "<marker> and <marker>"
    ```

- **Ma'lum bir qismga mos keladigan testlarni ishga tushirish:**
    ```bash
    pytest -k "substring"
    ```

- **Markerlarga asoslangan testlarni ishga tushirish:**
    ```bash
    pytest -m "marker_name"
    pytest -m "model and model_structure"
    pytest -m "model or model_structure"
    ```

- **Testlarni ishga tushirib, kod qamrovi hisobotini yaratish:**
    ```bash
    pytest --cov=path/to/package
    ```

- **Testlarni ishga tushirib, printlarni ko'rsatish:**
    ```bash
    pytest -s
    ```

- **Testlarni ishga tushirib, birinchi xatolikda to'xtatish:**
    ```bash
    pytest --exitfirst
    ```

- **Testlarni parallel ravishda ishga tushiring:**
    ```bash
    pytest -n num_workers
    ```

- **Testlarni batafsil chiqish bilan ishga tushiring:**
    ```bash
    pytest -v
    ```

- **Testlarni ishga tushirib, ogohlantirishlarni e'tiborsiz qoldirish:**
    ```bash
    pytest -p no:warnings
    ```

- **Testlarni ishga tushirib, muvaffaqiyatsiz bo'lgan testlarni qayta ishga tushirish:**
    ```bash
    pytest --reruns num_reruns
    ```

- **Testlarni ishga tushirib, ularni sekin deb belgilash:**
    ```bash
    pytest --slow
    ```

- **Testlarni ishga tushirib, ularni xfail (muvaffaqiyatsiz bo'lishi kutilayotgan) deb belgilash:**
    ```bash
    pytest --xfail
    ```

- **Verbosity-ni oshirish:**

    Pytest-ni oshirilgan verbosity bilan ishga tushirib, har bir test uchun batafsil ma'lumotlarni ko'rish:

    ```bash
    pytest -vv
    ```
