from logging.handlers import RotatingFileHandler
from database import fetch_attractions, fetch_available_tickets, fetch_time_slots, init_app, init_db, populate_db

import os
import logging

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['DATABASE'] = 'database.db'

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
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
    attractions = [] 
    
    for attraction in fetch_attractions():
        attractions.append({
            'id': attraction['id'],
            'name': attraction['name'],
            'description': attraction['description']
        })
    return jsonify(attractions)

@app.route('/api/attractions/timeslots', methods=['GET'])
def get_attractions_time_slots():
    time_slots = [] 
    
    for time_slot in fetch_time_slots():
        time_slots.append({
            'id': time_slot['id'],
            'start_time': time_slot['start_time'],
            'end_time': time_slot['end_time']
        })
    return jsonify(time_slots)

@app.route('/api/attractions/tickets', methods=['GET'])
def get_attractions_tickets():
    available_tickets = [] 
    
    for ticket in fetch_available_tickets():
        available_tickets.append({
            'id': ticket['id'],
            'type': ticket['type'],
            'price': ticket['price']
        })
    return jsonify(available_tickets)


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db()
            populate_db()

    app.run(host='0.0.0.0', port=5000, use_reloader=True)