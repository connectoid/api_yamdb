import csv
import sqlite3

DB = '../db.sqlite3'
CSV_PATH = '../static/data/'

def import_csv(filename):

    def ru(list):
        for set in list:
            for value in set:
                value.encode('utf-8')
        return list

    con = sqlite3.connect(DB)
    cur = con.cursor()

    with open(CSV_PATH+filename,'r') as file:
        # csv.DictReader по умолчанию использует первую строку под заголовки столбцов
        values = csv.DictReader(file, delimiter=",")
        fields = values.fieldnames
        to_db = []
        for row in values:
            to_db.append([row[col] for col in fields])
        to_db = ru(to_db)
        #to_db = [(i['id'], ru(i['name']), i['slug']) for i in dr]
        print(to_db)

    cur.executemany("INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);", to_db)
    con.commit()
    con.close()

import_csv('category.csv')