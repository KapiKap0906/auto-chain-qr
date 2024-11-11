import sqlite3

db_file='products.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('''
    DELETE FROM product_tracking
    WHERE product_id NOT LIKE 'S%' AND product_id NOT LIKE 'C%'
''')

conn.commit()
conn.close()