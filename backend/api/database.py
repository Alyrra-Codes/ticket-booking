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
    
    cur.executemany("INSERT INTO attractions (id, name, description, image_url, available_tickets) VALUES (?, ?, ?, ?, ?)",
                    [(1, "Aquarium", "Underwater world", "https://img.staticmb.com/mbcontent/images/crop/uploads/2022/12/Feng-shui-fish-acquarium_0_1200.jpg", 50),
                     (2, "Museum", "Historical artifacts", 'https://museumsvictoria.com.au/media/sdwl1btr/victoria-skeleton-2_exhibitionwo.jpg?anchor=center&mode=crop&width=768&height=432&rnd=133706953504930000&bgcolor:fff', 50),
                     (3, "Art Gallery", "Artwork from various artists", 'https://artgallery.yale.edu/sites/default/files/styles/hero_small/public/2023-01/ag-doc-2281-0036-pub.jpg?h=147a4df9&itok=uclO7OrF', 50)])

    cur.executemany("INSERT INTO time_slots (id, start_time, end_time) VALUES (?, ?, ?)",
                    [(1, "09:00", "10:00"),
                     (2, "10:00", "11:00"),
                     (3, "11:00", "12:00"), 
                     (4, "12:00", "13:00"),
                     (5, "13:00", "14:00"),
                     (6, "14:00", "15:00"),
                     (7, "15:00", "16:00"),
                     (8, "16:00", "17:00")])
    
    cur.executemany("INSERT INTO tickets (id, type, price) VALUES (?, ?, ?)",
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
    cur.execute("SELECT * FROM tickets")
    return cur.fetchall()

def save_booking(data):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("INSERT INTO bookings (attraction_id, time_slot_id, ticket_id, quantity, booking_code, status) VALUES (?, ?, ?, ?, ?, ?)",
                (data['attraction_id'], data['time_slot_id'], data['ticket_id'], data['quantity'], data['booking_code'], data['status']));
    
    db.commit()

def update_attraction_available_tickets(attraction_id, quantity):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("UPDATE attractions SET available_tickets = available_tickets - ? WHERE id = ?", (quantity, attraction_id))
    db.commit()
    
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