import sqlite3
from datetime import datetime

def initialize_database(db_file='products.db'):
    """Initializes the database with required columns."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_tracking (
            product_id TEXT,
            station_number TEXT,
            in_time DATETIME,
            out_time DATETIME,
            live BOOLEAN,
            stackable BOOLEAN DEFAULT 0,
            bags_in_stack INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def update_database(product_id: str, station_number: str, db_file='products.db'):
    """Handles non-stackable product database update."""
    initialize_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
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
            INSERT INTO product_tracking (product_id, station_number, in_time, live, stackable, bags_in_stack)
            VALUES (?, ?, ?, 1, 0, 0)
        ''', (product_id, station_number, current_time))
        conn.commit()

    conn.close()

def dispose_product(product_id: str, db_file='products.db'):
    """Updates the product to indicate it is no longer live (disposed) and prompts for stack info if stackable."""
    initialize_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    current_time = datetime.now()
    
    # Retrieve the active row for the product
    cursor.execute('''
        SELECT * FROM product_tracking
        WHERE product_id = ? AND live = 1
    ''', (product_id,))
    final_station = cursor.fetchone()

    if final_station:
        # Check if the item is stackable
        is_stackable = final_station[5]  # Assuming `stackable` is the 6th column (index 5)
        
        # If stackable, prompt user for the number of stacks available
        if is_stackable:
            while True:
                try:
                    stacks_available = int(input("Enter the number of stacks available for the stackable item: "))
                    if stacks_available < 0:
                        print("Please enter a non-negative integer.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            
            # Update the row with the number of stacks available for record-keeping
            cursor.execute('''
                UPDATE product_tracking
                SET out_time = ?, live = 0, bags_in_stack = ?
                WHERE product_id = ? AND station_number = ? AND live = 1
            ''', (current_time, stacks_available, product_id, final_station[1]))
        else:
            # For non-stackable items, simply mark as disposed
            cursor.execute('''
                UPDATE product_tracking
                SET out_time = ?, live = 0
                WHERE product_id = ? AND station_number = ? AND live = 1
            ''', (current_time, product_id, final_station[1]))

        conn.commit()
    else:
        print("No active record found for the specified product.")
    
    conn.close()

def stackable_update_database(product_id: str, station_number: str, bags_in_stack: int, db_file='products.db'):
    """Handles stackable product database update with stack count."""
    initialize_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    current_time = datetime.now()

    # Check if product is already live in this station
    cursor.execute('''
        SELECT * FROM product_tracking 
        WHERE product_id = ? AND station_number = ? AND live = 1
    ''', (product_id, station_number))
    row = cursor.fetchone()
    
    if row:
        print("Product is already live:", row)
    else:
        # Update previous station's live status and out_time if the product is live elsewhere
        cursor.execute('''
            SELECT * FROM product_tracking
            WHERE product_id = ? AND live = 1
        ''', (product_id,))
        previous_row = cursor.fetchone()

        if previous_row:
            cursor.execute('''
                UPDATE product_tracking
                SET live = 0, out_time = ?
                WHERE product_id = ? AND station_number = ? AND live = 1
            ''', (current_time, product_id, previous_row[1]))
            conn.commit()

        # Insert a new record with stackable set to true and bags_in_stack
        cursor.execute('''
            INSERT INTO product_tracking (product_id, station_number, in_time, live, stackable, bags_in_stack)
            VALUES (?, ?, ?, 1, 1, ?)
        ''', (product_id, station_number, current_time, bags_in_stack))
    
    conn.commit()
    conn.close()
 