import csv
import sqlite3

DB = '../db.sqlite3'
CSV_PATH = '../static/data/'
TABLES = {
    'category.csv': 'reviews_category',
    'genre.csv': 'reviews_genre',
    'titles.csv': 'reviews_title',
    'genre_title.csv': 'reviews_title_genre',
    'review.csv': 'reviews_review',
    'comments.csv': 'reviews_comment',
    'users.csv': 'reviews_user',   
}

def import_csv(filename):

    con = sqlite3.connect(DB)
    cur = con.cursor()
    
    with open(CSV_PATH+filename, 'r', encoding='utf-8') as file:
        values = csv.DictReader(file, delimiter=",")
        fields = values.fieldnames
        to_db = []
        for row in values:
            to_db.append([row[col] for col in fields])
    count = len(fields)
    table_name = TABLES[filename]
    query_str = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({('?, '*count)[:-2]});"
    #cur.executemany("INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);", to_db, )

    cur.executemany(query_str, to_db, )
    con.commit()
    con.close()

import_csv('category.csv')
import_csv('genre.csv')
import_csv('titles.csv')
import_csv('genre_title.csv')
import_csv('review.csv')
import_csv('comments.csv')
#import_csv('users.csv')