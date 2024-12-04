# Superhero Height API

Этот проект представляет собой API на базе FastAPI, который позволяет получать самого высокого супергероя по заданным параметрам: пол и наличие работы. API использует данные о супергероях из открытого источника [Superhero API](https://akabab.github.io/superhero-api/).

## Описание

API предоставляет эндпоинт, который принимает два параметра:

- **gender** (обязательный): Пол героя (Male/Female).
- **has_work** (обязательный): Наличие работы у героя (True/False).

API возвращает самого высокого героя, который соответствует этим параметрам, на основе данных о росте, которые указаны в дюймах и сантиметрах.

