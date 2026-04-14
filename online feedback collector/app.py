from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        rating INTEGER,
        comments TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-feedback', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO feedback (name,email,rating,comments) VALUES (?,?,?,?)",
                (name,email,rating,comments))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/admin-dashboard')
def admin():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM feedback")
    data = cur.fetchall()

    conn.close()

    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)