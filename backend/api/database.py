import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def populate_db():
    db = get_db()
    cur = db.cursor()
    
    cur.executemany("INSERT INTO attractions (id, name, description) VALUES (?, ?, ?)",
                    [(1, "Aquarium", "Underwater world"),
                     (2, "Museum", "Historical artifacts"),
                     (3, "Art Gallery", "Artwork from various artists")])

    cur.executemany("INSERT INTO time_slots (id, start_time, end_time) VALUES (?, ?, ?)",
                    [(1, "09:00", "10:00"),
                     (2, "10:00", "11:00"),
                     (3, "11:00", "12:00"), 
                     (4, "12:00", "13:00"),
                     (5, "13:00", "14:00"),
                     (6, "14:00", "15:00"),
                     (7, "15:00", "16:00"),
                     (8, "16:00", "17:00")])
    
    cur.executemany("INSERT INTO available_tickets (id, type, price) VALUES (?, ?, ?)",
                    [(1, "Adult", 15),
                     (2, "Child", 5),
                     (3, "Concession", 5)])
    
    db.commit()
    print('Populated the database with initial data.')

def init_app(app):
    app.teardown_appcontext(close_db)
    

def fetch_attractions():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM attractions")
    return cur.fetchall()

def fetch_time_slots():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM time_slots")
    return cur.fetchall()

def fetch_available_tickets():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM available_tickets")
    return cur.fetchall()