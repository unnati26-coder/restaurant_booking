from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  date TEXT NOT NULL,
                  time TEXT NOT NULL,
                  guests INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        guests = request.form['guests']
        
        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, date, time, guests) VALUES (?, ?, ?, ?, ?)",
                 (name, email, date, time, guests))
        conn.commit()
        conn.close()
        
        return redirect(url_for('bookings'))
    return render_template('book.html')

@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)