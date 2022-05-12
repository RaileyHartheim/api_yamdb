import csv, sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("CREATE TABLE genre (id, name, slug);")
# picture, price, number - это названия столбцов

with open('static/data/genre.csv','r') as fin:
    # csv.DictReader по умолчанию использует первую строку под заголовки столбцов
    dr = csv.DictReader(fin, delimiter=";")
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO genre (id, name, slug) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()