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
    
    cur.executemany("INSERT INTO attractions (id, name, description, image_url) VALUES (?, ?, ?, ?)",
                    [(1, "Aquarium", "Underwater world", "https://img.staticmb.com/mbcontent/images/crop/uploads/2022/12/Feng-shui-fish-acquarium_0_1200.jpg"),
                     (2, "Museum", "Historical artifacts", 'https://museumsvictoria.com.au/media/sdwl1btr/victoria-skeleton-2_exhibitionwo.jpg?anchor=center&mode=crop&width=768&height=432&rnd=133706953504930000&bgcolor:fff'),
                     (3, "Art Gallery", "Artwork from various artists", 'https://artgallery.yale.edu/sites/default/files/styles/hero_small/public/2023-01/ag-doc-2281-0036-pub.jpg?h=147a4df9&itok=uclO7OrF')])

    cur.executemany("INSERT INTO time_slots (id, attraction_id, start_time, end_time, available_tickets) VALUES (?, ?, ?, ?, ?)",
                    [(1, 1, "10:00", "11:00", 50),
                     (2, 1, "11:00", "12:00", 50),
                     (3, 1, "12:00", "13:00", 50),
                     (4, 1, "13:00", "14:00", 50),
                     (5, 1, "14:00", "15:00", 50),
                     (6, 1, "15:00", "16:00", 50),
                     (7, 1, "16:00", "17:00", 50), 
                     (8, 2, "10:00", "11:00", 50),
                     (9, 2, "11:00", "12:00", 50),
                     (10, 2, "12:00", "13:00", 50),
                     (11, 2, "13:00", "14:00", 50),
                     (12, 2, "14:00", "15:00", 50),
                     (13, 2, "15:00", "16:00", 50),
                     (14, 2, "16:00", "17:00", 50),
                     (15, 3, "10:00", "11:00", 50),
                     (16, 3, "11:00", "12:00", 50),
                     (17, 3, "12:00", "13:00", 50),
                     (18, 3, "13:00", "14:00", 50),
                     (19, 3, "14:00", "15:00", 50),
                     (20, 3, "15:00", "16:00", 50),
                     (21, 3, "16:00", "17:00", 50)])
    
    cur.executemany("INSERT INTO tickets (id, type, price) VALUES (?, ?, ?)",
                    [(1, "Adult", 15),
                     (2, "Child", 10),
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
    cur.execute("SELECT * FROM tickets")
    return cur.fetchall()

def save_booking(data):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("INSERT INTO bookings (attraction_id, time_slot_id, ticket_id, quantity, booking_code, status) VALUES (?, ?, ?, ?, ?, ?)",
                (data['attraction_id'], data['time_slot_id'], data['ticket_id'], data['quantity'], data['booking_code'], data['status']));
    
    db.commit()

def fetch_attraction_by_id(attraction_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM attractions WHERE id = ?", (attraction_id,))
    return cur.fetchone()

def update_time_slot_available_tickets(time_slot_id, quantity):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("UPDATE time_slots SET available_tickets = available_tickets - ? WHERE id = ?", (quantity, time_slot_id))
    db.commit()

def fetch_time_slot_by_attraction_id(attraction_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM time_slots WHERE attraction_id = ?", (attraction_id,))
    return cur.fetchall()

def fetch_time_slot_by_id(time_slot_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM time_slots WHERE id = ?", (time_slot_id,))
    return cur.fetchone()

def fetch_ticket_by_id(ticket_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    return cur.fetchone()


def get_booking_by_booking_code(booking_code):
    db = get_db()
    cur = db.cursor()
   
    statement = '''
        select 
            a.name as attraction_name, 
            ts.start_time, 
            ts.end_time, 
            ti.type, 
            ti.price, 
            b.quantity, 
            b.booking_code, 
            b.status
        from attractions a 
        join bookings b on a.id = b.attraction_id
        join time_slots ts on ts.id = b.time_slot_id
        join tickets ti on ti.id = b.ticket_id
        where b.booking_code = ?;
    '''
    cur = cur.execute(statement, (booking_code,))
    return cur.fetchall()