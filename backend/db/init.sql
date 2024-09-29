-- Create attraction_info table
CREATE TABLE attraction_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_url VARCHAR(255)
);

-- Create attraction_time_slot table
CREATE TABLE attraction_time_slot (
    id SERIAL PRIMARY KEY,
    attraction_id INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (attraction_id) REFERENCES attraction_info(id)
);

-- Create attraction_booking table
CREATE TABLE attraction_booking (
    id SERIAL PRIMARY KEY,
    time_slot_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    booking_time TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('booked', 'cancelled', 'booking_in_progress')),
    FOREIGN KEY (time_slot_id) REFERENCES attraction_time_slot(id)
);

-- Create user_info table
CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create event_logs table
CREATE TABLE event_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_info(id)
);