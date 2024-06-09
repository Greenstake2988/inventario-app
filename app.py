from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

def init_db():
    with sqlite3.connect('inventario.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS items
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        description TEXT)''')
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        description = request.form['description']

        with sqlite3.connect('inventario.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name, quantity, description) VALUES (?, ?, ?)',
                           (name, quantity, description))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port="8000",debug=True)
