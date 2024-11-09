import sqlite3
from datetime import datetime

def update_database(product_id: str, station_number: str, db_file='products.db'):
    # Connect to the SQLite database 
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_tracking (
            product_id TEXT,
            station_number TEXT,
            in_time DATETIME,
            out_time DATETIME,
            live BOOLEAN
        )
    ''')
    conn.commit()

    current_time = datetime.now()

    # Check if there is an active row with the given product_id and station_number
    cursor.execute('''
        SELECT * FROM product_tracking
        WHERE product_id = ? AND station_number = ? AND live = 1
    ''', (product_id, station_number))
    active_row = cursor.fetchone()

    if active_row:
        print("Active row found:", active_row)
    else:
        # Check if the product_id is active in a different station
        cursor.execute('''
            SELECT * FROM product_tracking
            WHERE product_id = ? AND live = 1
        ''', (product_id,))
        row_different_station = cursor.fetchone()

        if row_different_station:
            # Update the existing row to set out_time and live = false
            cursor.execute('''
                UPDATE product_tracking
                SET out_time = ?, live = 0
                WHERE product_id = ? AND station_number = ? AND live = 1
            ''', (current_time, product_id, row_different_station[1]))
            conn.commit()

        # Insert a new row with the current product_id and station_number
        cursor.execute('''
            INSERT INTO product_tracking (product_id, station_number, in_time, live)
            VALUES (?, ?, ?, 1)
        ''', (product_id, station_number, current_time))
        conn.commit()

    conn.close()

def dispose_product(product_id: str, db_file='products.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    current_time = datetime.now()
    cursor.execute('''
        SELECT * FROM product_tracking
        WHERE product_id = ? AND live = 1
    ''', (product_id,))
    final_station = cursor.fetchone()

    if final_station:
        # Update the existing row to set out_time and live = false
        cursor.execute('''
            UPDATE product_tracking
            SET out_time = ?, live = 0
            WHERE product_id = ? AND station_number = ? AND live = 1
        ''', (current_time, product_id, final_station[1]))
        conn.commit()
    conn.close()

