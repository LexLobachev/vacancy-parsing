# vacancy-parsing
displays the average salary by programming language for vacancies from [HH](https://hh.ru) &amp; [SuperJob](https://superjob.ru)

## Environment

### Requirements

Python3(python 3.11 is recommended) should be already installed. Then use pip3 to install dependencies:

```bash
pip3 install -r requirements.txt
```

### Environment variables

- SJ_SECRET_KEY

1. Put `.env` file near `requirements.txt`.
2. `.env` contains text data without quotes.

For example, if you print `.env` content, you will see:

```bash
$ cat .env
SJ_SECRET_KEY=your_superjob_secret_key
```

#### How to get

* Register an application [SuperJob](https://api.superjob.ru/info/) and generate there the `Secret key`

## Run

Launch on Linux(Python 3) or Windows:

### main.py

Script for parsing vacancies on SuperJob and HeadHunter and for displaying tables with data about this vacancies

```bash
$ python3 main.py
```

You will receive 2 tables in your console

```bash
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 2113             | 1355                | 105476           |
| Java                  | 1423             | 600                 | 107725           |
| Python                | 1326             | 770                 | 121027           |
| Ruby                  | 101              | 60                  | 169830           |
| PHP                   | 934              | 720                 | 95000            |
| C++                   | 987              | 550                 | 136281           |
| Go                    | 472              | 215                 | 183348           |
| C#                    | 826              | 441                 | 142591           |
| C                     | 1730             | 1134                | 132603           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 44               | 36                  | 56432            |
| Java                  | 11               | 7                   | 96714            |
| Python                | 37               | 25                  | 63283            |
| Ruby                  | 0                | 0                   | 0                |
| PHP                   | 33               | 24                  | 91871            |
| C++                   | 25               | 18                  | 104305           |
| Go                    | 44               | 41                  | 18695            |
| C#                    | 8                | 6                   | 104500           |
| C                     | 367              | 348                 | 48387            |
+-----------------------+------------------+---------------------+------------------+
```
