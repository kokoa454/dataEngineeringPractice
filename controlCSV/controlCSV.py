import sqlite3
import csv

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY,
        date TEXT,
        product TEXT,
        price REAL,
        quantity INTEGER
    );
''')

with open('sales_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
        INSERT INTO sales (date, product, price, quantity)
        VALUES (?, ?, ?, ?)
        ''', (row['date'], row['product'], float(row['price']), int(row['quantity'])))

conn.commit()
conn.close()