# Asosiy repositoriyadan so’ngi yangilanishlarni olish

Boshlang’ich sozlamalar ichida quyidagi fayllar oldindan yozib tayyorlab qo’yilgan bo’ladi. Vaqt o’tib asosiy repo va sizning repongiz orasida farq paydo bo’ladigan bo’lsa, ushbu yangilanishlarni quyidagicha yuklab olishingiz mumkin.

- **Ushbu qatorda qaysi repodan yangilanishlarni olish kerakligini ko'rsatadi va qaysi originga olishni**
    ```
    git remote add upstream https://github.com/Mohirdevelopers/medium-clone-backend-initial.git
    ```

- **Biz upstreamga fetch (olib kelish) buyrug'iri berdik**
    ```
    git fetch upstream
    ```

- **Upstreamdagi ko'rsatilgan papkalardagi uzgarishlarni main dagi shu papkalarga o'tkazish buyrug'iri**
   ```
   git checkout upstream/main -- _docs_for_use tests .github/workflows/unittest-checker.yaml .deploy Dockerfile docker-compose.yaml pytest.ini
   ```
