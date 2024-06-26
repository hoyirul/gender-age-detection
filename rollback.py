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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        faceID TEXT PRIMARY KEY,
        gender TEXT,
        age_group TEXT
    )
''')
conn.commit()

# Menampilkan pesan

print('Data pengunjung telah direset.')

# Tutup koneksi
conn.close()
