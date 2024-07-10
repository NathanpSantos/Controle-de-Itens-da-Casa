import sqlite3

DATABASE = 'inventory.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Create tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT NOT NULL,
        observation TEXT,
        feito INTEGER NOT NULL DEFAULT 0,
        room_id INTEGER NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms (id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS cleaning_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        observation TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        observation TEXT
    )
    ''')

    # Insert default rooms
    rooms = [
        ('Sala',),
        ('Quarto 1',),
        ('Quarto 2',),
        ('Banheiro 1',),
        ('Banheiro 2',),
        ('Cozinha',),
        ('Quintal',),
        ('Garagem',),
        ('Lavabo',)
    ]

    cur.executemany('INSERT OR IGNORE INTO rooms (name) VALUES (?)', rooms)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
