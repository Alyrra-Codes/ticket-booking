import random
from database import fetch_attraction_by_id, \
    fetch_attractions, fetch_available_tickets, \
    fetch_time_slot_by_attraction_id, fetch_time_slot_by_id, \
    get_booking_by_booking_code, init_app, init_db, populate_db, \
    save_booking, update_time_slot_available_tickets

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['DATABASE'] = 'database.db'

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(logging.Formatter(
       '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    ))
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    app.logger.setLevel(logging.INFO)

setup_logging(app)
init_app(app)

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.cli.command('populatedb')
def populatedb_command():
    populate_db()
    print('Populated the database with initial data.')


@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    task_id = '1'
    
    session_id = request.headers.get('X-Session-ID')
    app.logger.info(f'{task_id} {session_id}: fetching attractions')
    
    attractions = [] 
    
    for attraction in fetch_attractions():
        attractions.append({
            'id': attraction['id'],
            'name': attraction['name'],
            'description': attraction['description'], 
            'imageUrl': attraction['image_url']
        })
    
    app.logger.info(f'{task_id} {session_id}: fetched {len(attractions)} attractions')
    return jsonify(attractions)

@app.route('/api/attractions/<attraction_id>/timeslots', methods=['GET'])
def get_attractions_time_slots(attraction_id):
    task_id = '2'
    
    session_id = request.headers.get('X-Session-ID')
    app.logger.info(f'{task_id} {session_id}: fetching time slots')
    
    time_slots = [] 
    
    for time_slot in fetch_time_slot_by_attraction_id(attraction_id):
        time_slots.append({
            'id': time_slot['id'],
            'startTime': time_slot['start_time'],
            'endTime': time_slot['end_time'], 
            'availableTickets': time_slot['available_tickets']
        })
    app.logger.info(f'{task_id} {session_id}: fetched {len(time_slots)} time slots')
    return jsonify(time_slots)

@app.route('/api/attractions/tickets', methods=['GET'])
def get_attractions_tickets():
    task_id = '3'
    
    session_id = request.headers.get('X-Session-ID')
    app.logger.info(f'{task_id} {session_id}: fetching available tickets')
    available_tickets = [] 
    
    for ticket in fetch_available_tickets():
        available_tickets.append({
            'id': ticket['id'],
            'type': ticket['type'],
            'price': ticket['price']
        })
    app.logger.info(f'{task_id} {session_id}: fetched {len(available_tickets)} available tickets')
    return jsonify(available_tickets)

@app.route('/api/attractions/<attraction_id>/bookings', methods=['POST'])
def booking(attraction_id):
    task_id = '4'
    
    session_id = request.headers.get('X-Session-ID')
    
    data = request.get_json()
    
    statuses = ['failed', 'success']
    
    status = random.choice(statuses)

    if status == 'failed':
        app.logger.error(f"{task_id} {session_id}: invalid payment details")
        return jsonify({'status': 'failed', 'message': 'Invalid payment details. Please try again'}), 400
    
    booking_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2)) + ''.join(random.choices('0123456789', k=4))
    
    time_slot = data.get('timeSlot')
    tickets = data.get('tickets')
    booking = data.get('booking')
    payment = data.get('payment')
    
    fetched_attraction = fetch_attraction_by_id(attraction_id)
    
    if not fetched_attraction:
        app.logger.error(f"{task_id} {session_id}: attraction with id {attraction_id} not found")
        return jsonify({'status': 'failed', 'message': 'Attraction not found.'}), 404
    
    if not time_slot or not tickets or not booking:
        app.logger.error(f"{task_id} {session_id}: invalid booking data")
        return jsonify({'status': 'failed', 'message': 'Booking failed. Please try again.'}), 400
    
    fetched_time_slot = fetch_time_slot_by_id(time_slot.get('id')); 

    # Check if the selected time slot is valid
    if fetched_time_slot is None:
        app.logger.error(f"{task_id} {session_id}: invalid time slot selected")
        return jsonify({'status': 'failed', 'message': 'Invalid time slot selected.'}), 400
    
    fetched_tickets = fetch_available_tickets()
    
    # Check if the selected tickets are valid
    for ticket in tickets.get('tickets'):
        fetched_ticket = next((t for t in fetched_tickets if t['id'] == ticket.get('id')), None)
        
        if fetched_ticket is None:
            return jsonify({'status': 'failed', 'message': 'Invalid ticket selected.'}), 400
    
    total_tickets = 0
    for ticket in tickets.get('tickets'):
        booking_data = {
            'attraction_id': fetched_attraction['id'],
            'time_slot_id': time_slot.get('id'),
            'ticket_id': ticket.get('id'),
            'quantity': ticket.get('quantity'),
            'booking_code': booking_code, 
            'status': 'booked'
        }
        total_tickets += ticket.get('quantity')
        
        app.logger.info(f"{task_id} {session_id}: saving booking for attraction {fetched_attraction['name']}")
        save_booking(booking_data)
        
    
    app.logger.info(f"{task_id} {session_id}: updating available tickets for attraction {fetched_attraction['name']}")
    update_time_slot_available_tickets(time_slot.get('id'), total_tickets)
    
    app.logger.info(f"{task_id} {session_id}: booking successful")
    
    return jsonify({
        'bookingCode': booking_code,
    }), 201

@app.route('/api/attractions/bookings/<booking_code>', methods=['GET'])
def get_booking(booking_code):
    task_id = '5'
    
    session_id = request.headers.get('X-Session-ID')
    
    app.logger.info(f'{task_id} {session_id}: fetching booking')
    bookings = get_booking_by_booking_code(booking_code)
    
    if not bookings:
        app.logger.error(f"{task_id} {session_id}: booking not found")
        return jsonify({'status': 'failed', 'message': 'Booking not found.'}), 404
    
    response_data = {}
    
    purchased_tickets = []
    
    for booking in bookings:
        purchased_tickets.append({
            'type': booking['type'],
            'price': booking['price'],
            'quantity': booking['quantity']
        })
    
    response_data['attractionName'] = bookings[0]['attraction_name']
    response_data['startTime'] = bookings[0]['start_time']
    response_data['endTime'] = bookings[0]['end_time']
    response_data['tickets'] = purchased_tickets
    response_data['bookingCode'] = bookings[0]['booking_code']
    response_data['status'] = bookings[0]['status']
    
    app.logger.info(f'{task_id} {session_id}: fetched booking')
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.logger.info('Starting the application')
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db()
            populate_db()

    app.run(host='0.0.0.0', port=5000, use_reloader=True)