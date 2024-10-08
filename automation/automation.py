from faker import Faker
import requests 
import json 
import random

BASE_API = 'http://localhost:5000/api'

def generate_session_code():
  return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))

def get_attractions(header):
  response = requests.get(f'{BASE_API}/attractions', headers=header)
  attractions = json.loads(response.text)
  
  return attractions

def get_time_slots(header):
  response = requests.get(f'{BASE_API}/attractions/timeslots', headers=header)
  time_slots = json.loads(response.text)
  
  return time_slots

def get_tickets(header):
  response = requests.get(f'{BASE_API}/attractions/tickets', headers=header)
  
  return json.loads(response.text)

def get_personal_info():
  faker = Faker()
  
  return {
    'name': faker.name(),
    'email': faker.email(),
    'phone': faker.phone_number(),
    'address': faker.address()
  }

def select_tickets(tickets, max_available_tickets):
  selected_tickets = []
  total_cost = 0
  
  quantity_selected = 0
  
  for ticket in tickets:
    quantity = random.randint(0, max_available_tickets)
    if quantity > 0 and quantity_selected + quantity <= max_available_tickets:
      selected_tickets.append({
        'id': ticket.get('id'),
        'type': ticket.get('type'),
        'price': ticket.get('price'),
        'quantity': quantity
      })
      total_cost += ticket.get('price') * quantity
      
      quantity_selected += quantity
  return {
    'tickets': selected_tickets,
    'totalCost': total_cost
  }

def get_payment_info():
  faker = Faker()
  
  return {
    'name': faker.name(),
    'number': faker.credit_card_number(),
    'expiry': faker.credit_card_expire(),
    'cvv': faker.credit_card_security_code()
  }
  
def book_attraction(data, header):
  response = requests.post(f'{BASE_API}/attractions/bookings', headers=header, json=data)
  
  if response.status_code != 201:
    raise Exception(response.text)
  
  return json.loads(response.text).get('bookingCode')
  
def main():
  session_code = generate_session_code()
  header = {'X-Session-ID': session_code}
  
  print(f'Generated session code: {session_code}')
  
  attractions = get_attractions(header)
  selected_attraction = random.choice(attractions)
  
  print(f'Selected attraction: {selected_attraction}')
  
  time_slots = get_time_slots(header)
  selected_time_slot = random.choice(time_slots)
  
  print(f'Selected time slot: {selected_time_slot}')
  
  tickets = get_tickets(header)
  selected_tickets = select_tickets(tickets, selected_attraction.get('availableTickets'))
  
  print(f'Selected tickets: {selected_tickets}')
  
  booking_details = get_personal_info()
  
  print(f'Booking details: {booking_details}')
  
  payment_details = get_payment_info()
  print(f'Payment details: {payment_details}')
  
  booking_data = {
    'attraction': selected_attraction,
    'timeSlot': selected_time_slot,
    'tickets': selected_tickets,
    'booking': booking_details,
    'payment': payment_details
  }
  
  try:
    booking_code = book_attraction(booking_data, header)
    print(f'Booking successful. Booking code: {booking_code}')
  except Exception as e:
    print(f'Failed to book attraction: {e}')
  
  
if __name__ == '__main__':
  # Simulate
  for index in range(100):
    main()