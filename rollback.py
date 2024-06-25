import sqlite3

# Inisialisasi koneksi SQLite
conn = sqlite3.connect('visitors.db')
cursor = conn.cursor()

# Truncate tabel
cursor.execute('''
    DROP TABLE visitors
''')
conn.commit()

# Menampilkan pesan
print('Data pengunjung telah dihapus.')

# Tutup koneksi
conn.close()
