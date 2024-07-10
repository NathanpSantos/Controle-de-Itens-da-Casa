import sqlite3

DATABASE = 'inventory.db'

def clean_duplicates():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Cleaning items table
    cur.execute('''
    DELETE FROM items
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM items
        GROUP BY name, status, observation, room_id
    )
    ''')

    # Cleaning cleaning_products table
    cur.execute('''
    DELETE FROM cleaning_products
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM cleaning_products
        GROUP BY name, observation
    )
    ''')

    # Cleaning food_items table
    cur.execute('''
    DELETE FROM food_items
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM food_items
        GROUP BY name, location, observation
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    clean_duplicates()
