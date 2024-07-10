import sqlite3

DATABASE = 'inventory.db'

def check_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Check rooms table
    cur.execute('SELECT * FROM rooms')
    rooms = cur.fetchall()
    print("Rooms:")
    for room in rooms:
        print(room)

    # Check items table
    cur.execute('SELECT * FROM items')
    items = cur.fetchall()
    print("\nItems:")
    for item in items:
        print(item)

    # Check cleaning_products table
    cur.execute('SELECT * FROM cleaning_products')
    products = cur.fetchall()
    print("\nCleaning Products:")
    for product in products:
        print(product)

    # Check food_items table
    cur.execute('SELECT * FROM food_items')
    food_items = cur.fetchall()
    print("\nFood Items:")
    for food_item in food_items:
        print(food_item)

    conn.close()

if __name__ == '__main__':
    check_db()
