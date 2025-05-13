from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'surfersecretkey'

# Database initialization
def get_db_connection():
    conn = sqlite3.connect('beaches.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('beaches.db'):
        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.close()

@app.before_first_request
def before_first_request():
    init_db()

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    beaches = conn.execute('SELECT * FROM beaches').fetchall()
    conn.close()
    return render_template('index.html', beaches=beaches)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        spot_type = request.form['spot_type']
        wave = request.form['wave']
        offshore = request.form['offshore']
        tide = request.form['tide']
        level = request.form['level']
        
        if not name:
            flash('Beach name is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO beaches (name, spot_type, wave, offshore, tide, level) VALUES (?, ?, ?, ?, ?, ?)',
                (name, spot_type, wave, offshore, tide, level)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    beach = conn.execute('SELECT * FROM beaches WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        spot_type = request.form['spot_type']
        wave = request.form['wave']
        offshore = request.form['offshore']
        tide = request.form['tide']
        level = request.form['level']
        
        if not name:
            flash('Beach name is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                'UPDATE beaches SET name = ?, spot_type = ?, wave = ?, offshore = ?, tide = ?, level = ? WHERE id = ?',
                (name, spot_type, wave, offshore, tide, level, id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('edit.html', beach=beach)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM beaches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)