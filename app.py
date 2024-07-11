from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    rooms = conn.execute('SELECT * FROM rooms').fetchall()
    conn.close()
    return render_template('index.html', rooms=rooms)

@app.route('/room/<int:room_id>')
def room(room_id):
    conn = get_db_connection()
    room = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
    items = conn.execute('SELECT * FROM items WHERE room_id = ?', (room_id,)).fetchall()
    conn.close()
    if room:
        return render_template('room.html', room=room, items=items)
    else:
        return "Room not found", 404

@app.route('/add_item/<int:room_id>', methods=('GET', 'POST'))
def add_item(room_id):
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        observation = request.form['observation']

        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, status, observation, room_id) VALUES (?, ?, ?, ?)',
                     (name, status, observation, room_id))
        conn.commit()
        conn.close()
        return redirect(url_for('room', room_id=room_id))

    return render_template('add_item.html', room_id=room_id)

@app.route('/delete_item/<int:item_id>', methods=('POST',))
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@app.route('/mark_done/<int:item_id>', methods=('POST',))
def mark_done(item_id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET feito = 1 WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@app.route('/cleaning_products')
def cleaning_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM cleaning_products').fetchall()
    conn.close()
    return render_template('cleaning_products.html', products=products)

@app.route('/add_cleaning_product', methods=['GET', 'POST'])
def add_cleaning_product():
    if request.method == 'POST':
        name = request.form['name']
        observation = request.form['observation']
        conn = get_db_connection()
        conn.execute('INSERT INTO cleaning_products (name, observation) VALUES (?, ?)', (name, observation))
        conn.commit()
        conn.close()
        return redirect(url_for('cleaning_products'))
    return render_template('add_cleaning_product.html')

@app.route('/food_items')
def food_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM food_items').fetchall()
    conn.close()
    return render_template('food_items.html', items=items)

@app.route('/add_food_item', methods=['GET', 'POST'])
def add_food_item():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        observation = request.form['observation']
        conn = get_db_connection()
        conn.execute('INSERT INTO food_items (name, location, observation) VALUES (?, ?, ?)', (name, location, observation))
        conn.commit()
        conn.close()
        return redirect(url_for('food_items'))
    return render_template('add_food_item.html')

@app.route('/add_location', methods=('GET', 'POST'))
def add_location():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO rooms (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_location.html')

@app.route('/delete_cleaning_product/<int:product_id>', methods=['POST'])
def delete_cleaning_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cleaning_products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('cleaning_products'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)