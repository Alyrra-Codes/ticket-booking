# Usage
```bash
# Create venv 
python -m venv .venv 
pip3 install -r requirements.txt 

# Windows
set FLASK_APP=app.py

# Linux / mac
export FLASK_APP=app.py

# Create db schemas
flask initdb

# Populate init data
flask populatedb

# run the api server 
python api/app.py
```

# Endpoints 

GET /api/attractions 

Response 
  - status 200 OK 
  - Body: Json array of attractions 

```json
[
  {
    "id": 1, 
    "name": "museum", 
    "description": "the museum is where you see museum stuff", 
    "imageUrl": "https://museum_url.jpg"
  }, 
  {
    "id": 2, 
    "name": "Zoo", 
    "description": "This is a zoo description", 
    "imageUrl": "https://some_zoo_img.jpg"
  }
]
```


GET /api/tickets

RESPONSE 
  - status 200 OK 
  - Body: Json array of available tickets

```json 
  [
    {
      "id": 1, 
      "type": "Platinum", 
      "price": "$200",
      "description": "Platinum perks"
    }, 
    {
      "id": 2, 
      "type": "Gold", 
      "price": "$150", 
      "description": "Golden perks"
    }, 
    {
      "id": 3, 
      "type": "Silver", 
      "price": "$100", 
      "description": "Silver perks"
    }
  ]
```

POST /api/attractions/booking

create a new booking 

Request 
  - Body: Json with object detail

```json 
  {
    "attractionId": 1, 
    "timeSlotId": 1, 
    "ticketId": 2, 
    "userDetails": {
      "name": "John Doe", 
      "email": "test@gmail.com", 
      "mobile": "2319239124"
    }
  }
```

Response 
  - status 201 CREATED
  - Body: json with bookingId to track booking 

  ```json
    {
      "bookingId": 1
    }
  ```

POST /api/attractions/payment

process payment for the booking 

Request
  - json of a payment details 

```json
  {
    "bookingId": 1, 
    "paymentDetails": {
      "cardNumber": "124141245", 
      "cvc": "123", 
      "cardExpiry": "03/27", 
      "cardType": "visa"
    }
  }
```

Response 
  - status 201 CREATED 
  - status 402 PAYMENT REQUIRED (this is a failed payment response)

```json 
  {
    "message": "payment successfully processed"
  }
```

```json 
  {
    "message": "payment failed"
  }
```
