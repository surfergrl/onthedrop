from flask import Flask, render_template, request, redirect, url_for, flash
import os
import psycopg2
from psycopg2.extras import DictCursor

# Import environment variables if in development
try:
    import env
except ImportError:
    pass  # In production, env vars are set on the platform

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Database connection
def get_db_connection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    conn.cursor_factory = DictCursor
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create beaches table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS beaches (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            spot_type TEXT,
            wave TEXT,
            offshore TEXT,
            tide TEXT,
            level TEXT
        );
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Workaround for before_first_request issue
first_request = True

@app.before_request
def initialize_db():
    global first_request
    if first_request:
        print("Initializing database before first request...")
        init_db()
        first_request = False

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM beaches')
    beaches = cur.fetchall()
    cur.close()
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
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO beaches (name, spot_type, wave, offshore, tide, level) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, spot_type, wave, offshore, tide, level)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM beaches WHERE id = %s', (id,))
    beach = cur.fetchone()
    cur.close()
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
            cur = conn.cursor()
            cur.execute(
                'UPDATE beaches SET name = %s, spot_type = %s, wave = %s, offshore = %s, tide = %s, level = %s WHERE id = %s',
                (name, spot_type, wave, offshore, tide, level, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('edit.html', beach=beach)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM beaches WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("DEBUG") == "True"
    )