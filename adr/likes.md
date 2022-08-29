**Issue:**
Выбрать структуру хранения для лайков
и тип лайков (оценка либо лайк/дизлайк)

**Decision:**

В качестве лайка хранится оценка - от 0 до 10

DB - ugc_db
collection - likes
documents - {movie_id, user_id, score},
           {movie_id, user_id, score}

**Notes:**

Оценка более точно позволит рассчитать рейтинг фильма, чем лайк/дизлак
