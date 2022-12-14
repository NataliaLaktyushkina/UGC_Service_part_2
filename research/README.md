1. **Хранилище для задачи:**

Для текущей задачи в качестве хранилища используется MongoDB.
Данная СУБД отлично масштабируется, и по сравнению с традиционными SQL-системами, гораздо быстрее осуществляет чтение и запись.

2. **Cкрипт, который генерирует в хранилище данные**

Запуск Mongo из директории [research/Mongo](/research/Mongo):

`docker compose -f docker-compose-mongo.yml up`

Запуск Jupyter из директории [research/Jupyter](/research/Jupyter):

`docker compose up`

[Скрипт](/research/Jupyter/research.ipynb)

3. **Измерить скорость добавления и чтения данных:**

Требования к скорости обработки данных = 200 мс.

 - Тестирование чтения уже загруженных данных:
   - количество лайков или дизлайков у определённого фильма;

   Количество данных = 15 000

   Время чтения = 0:06:14.844879

   - список закладок;

   Количество данных = 15 000

   Время чтения = 0:01:00.668124
4. **Тестирование чтения данных, поступающих в реальном времени:**
   - добавление лайка или дизлайка и время появления лайка или дизлайка в сценариях, описанных выше.

   Среднее время чтения = 0:00:00.027487.0


5. Для текущей задачи используется отдельный сервис, так как
используется другое хранилище.
Предполагаем, что разработчиков для поддержки разных сервисов хватает.
Также при необходимо можно данный сервис отключить, не задев остальные.
