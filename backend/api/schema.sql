CREATE TABLE IF NOT EXISTS attractions (
  id INTEGER PRIMARY KEY, 
  name TEXT NOT NULL, 
  description TEXT, 
  image_url TEXT, 
  available_tickets INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS time_slots (
  id INTEGER PRIMARY KEY NOT NULL, 
  start_time TEXT NOT NULL, 
  end_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY NOT NULL, 
  type TEXT NOT NULL, 
  price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  booking_code TEXT NOT NULL,
  time_slot_id INTEGER NOT NULL, 
  attraction_id INTEGER NOT NULL,
  booking_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  ticket_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('booked', 'cancelled', 'booking_in_progress')), 
  FOREIGN KEY (time_slot_id) REFERENCES time_slots(id),
  FOREIGN KEY (attraction_id) REFERENCES attractions(id)
);