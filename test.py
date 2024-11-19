import sqlite3
from main import initialize_database
# def update_table_schema(db_file='products.db'):
#     """Update the product_tracking table to include the product_name column."""
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     # Check if the column already exists
#     cursor.execute("PRAGMA table_info(product_tracking)")
#     columns = [column[1] for column in cursor.fetchall()]
    
#     if "product_name" not in columns:
#         # Add the new column
#         cursor.execute("ALTER TABLE product_tracking ADD COLUMN product_name TEXT")
#         print("Column 'product_name' added to the table.")
#     else:
#         print("Column 'product_name' already exists in the table.")

#     conn.commit()
#     conn.close()

initialize_database()