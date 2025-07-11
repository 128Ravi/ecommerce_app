from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

def get_db_connection():
    con = sqlite3.connect('db.sqlite3')
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = get_db_connection()
        user = con.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        con.close()
        if user:
            session['user'] = username
            return redirect(url_for('products'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/products')
def products():
    if 'user' not in session:
        return redirect(url_for('login'))
    con = get_db_connection()
    items = con.execute('SELECT * FROM products').fetchall()
    con.close()
    return render_template('products.html', products=items)

@app.route('/select/<int:product_id>')
def select(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    con = get_db_connection()
    product = con.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    con.close()
    return f"You selected: {product['name']} priced at Rs.{product['price']}"

if __name__ == '__main__':
    app.run(debug=True)
