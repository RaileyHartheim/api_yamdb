import csv
import os
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

current_dir = os.path.dirname(__file__)


with open(os.path.join(current_dir, 'static/data/users.csv'), 'r') as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['username'],
        i['email'],
        i['role'],
        i['bio'],
        i['first_name'],
        i['last_name']) for i in dr]
    cur.executemany("INSERT INTO users_user"
                    "(id, username, email, role, bio,"
                    "first_name, last_name, password, is_superuser,"
                    "is_staff, is_active, date_joined, confirmation_code)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, False, False, False,"
                    "False, False, False);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/genre.csv', ), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['name'],
        i['slug']) for i in dr]
    cur.executemany("INSERT INTO reviews_genre"
                    "(id, name, slug)"
                    "VALUES (?, ?, ?);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/category.csv'), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['name'],
        i['slug']) for i in dr]
    cur.executemany("INSERT INTO reviews_category"
                    "(id, name, slug)"
                    "VALUES (?, ?, ?);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/titles.csv'), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['name'],
        i['year'],
        i['category']) for i in dr]
    cur.executemany("INSERT INTO reviews_title"
                    "(id, name, year, category_id)"
                    "VALUES (?, ?, ?, ?);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/genre_title.csv'), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['title_id'],
        i['genre_id']) for i in dr]
    cur.executemany("INSERT INTO reviews_genretitle"
                    "(id, title_id, genre_id)"
                    "VALUES (?, ?, ?);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/review.csv'), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['title_id'],
        i['text'],
        i['author'],
        i['score'],
        i['pub_date']) for i in dr]
    cur.executemany("INSERT INTO reviews_review"
                    "(id, title_id, text, author_id, score, pub_date)"
                    "VALUES (?, ?, ?, ?, ?, ?);", to_db)
    con.commit()


with open(os.path.join(current_dir, 'static/data/comments.csv'), 'r', encoding="utf8") as fl:
    dr = csv.DictReader(fl)
    to_db = [(
        i['id'],
        i['review_id'],
        i['text'],
        i['author'],
        i['pub_date']) for i in dr]
    cur.executemany("INSERT INTO reviews_comments"
                    "(id, review_id, text, author_id, pub_date)"
                    "VALUES (?, ?, ?, ?, ?);", to_db)
    con.commit()


con.close()