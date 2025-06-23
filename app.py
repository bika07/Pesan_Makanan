from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Buat database jika belum ada
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS pesanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    menu TEXT,
    jumlah INTEGER,
    catatan TEXT,
    no_wa TEXT,
    waktu_pesan TEXT,
    status TEXT DEFAULT 'Pending'
)
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM pesanan ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama']
    menu = request.form['menu']
    jumlah = request.form['jumlah']
    catatan = request.form['catatan']
    no_wa = request.form['no_wa']
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO pesanan (nama, menu, jumlah, catatan, no_wa, waktu_pesan) VALUES (?, ?, ?, ?, ?, ?)',
                (nama, menu, jumlah, catatan, no_wa, waktu))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/ubah_status/<int:id>/<string:status>')
def ubah_status(id, status):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('UPDATE pesanan SET status=? WHERE id=?', (status, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
