import sqlite3
from flask import current_app, g

def get_db():
    """Veritabanına bağlanır; satırlara sütun adıyla erişim sağlar."""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db(app):
    """Tabloları oluşturur (yoksa)."""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                koleksiyon TEXT,
                tarih TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS test_baslangic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS test_sonuclari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                koleksiyon TEXT NOT NULL,
                tarih TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj=None, koleksiyon=None):
    """Yeni kayıt ekler."""
    db = get_db()
    db.execute(
        'INSERT INTO leads (isim, telefon, mesaj, koleksiyon) VALUES (?, ?, ?, ?)',
        (isim, telefon, mesaj, koleksiyon)
    )
    db.commit()

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye getirir."""
    db = get_db()
    rows = db.execute('SELECT * FROM leads ORDER BY tarih DESC').fetchall()
    return [dict(row) for row in rows]

def test_baslangic_ekle():
    """Testin başlatıldığını kaydeder."""
    db = get_db()
    db.execute('INSERT INTO test_baslangic DEFAULT VALUES')
    db.commit()

def test_sonuc_ekle(koleksiyon):
    """Tamamlanan bir testin sonucunu kaydeder."""
    db = get_db()
    db.execute('INSERT INTO test_sonuclari (koleksiyon) VALUES (?)', (koleksiyon,))
    db.commit()

def istatistikleri_getir():
    """Dashboard için özet istatistikleri hesaplar."""
    db = get_db()

    lead_sayisi = db.execute('SELECT COUNT(*) AS sayi FROM leads').fetchone()['sayi']
    test_baslangic_sayisi = db.execute('SELECT COUNT(*) AS sayi FROM test_baslangic').fetchone()['sayi']
    test_tamamlama_sayisi = db.execute('SELECT COUNT(*) AS sayi FROM test_sonuclari').fetchone()['sayi']

    dagilim_satirlari = db.execute('''
        SELECT koleksiyon, COUNT(*) AS sayi
        FROM test_sonuclari
        GROUP BY koleksiyon
        ORDER BY sayi DESC
    ''').fetchall()

    koleksiyon_dagilimi = [dict(row) for row in dagilim_satirlari]
    en_populer_koleksiyon = koleksiyon_dagilimi[0]['koleksiyon'] if koleksiyon_dagilimi else "-"

    return {
        "lead_sayisi": lead_sayisi,
        "test_baslangic_sayisi": test_baslangic_sayisi,
        "test_tamamlama_sayisi": test_tamamlama_sayisi,
        "en_populer_koleksiyon": en_populer_koleksiyon,
        "koleksiyon_dagilimi": koleksiyon_dagilimi
    }