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
    "timeSlots": [
      {
        "id": 1, 
        "startTime": "9:00 am"
        "endTime": "10:00 am", 
      }, 
      {
        "id": 2, 
        "startTime": "10:00 am", 
        "endPoint": "11:00 am"
      }, 
      {
        "id": "3", 
        "startTime": "11:00 am", 
        "endTime": "12:00 pm" 
      }, 
      {
        "id": 4, 
        "startTime": "12:00 pm", 
        "endTime": "01:00 pm"
      }, 
      {
        "id": 5, 
        "startTime": "01:00 pm", 
        "endTime": "02:00 pm", 
      }, 
      {
        "id": 6, 
        "startTime": "02:00 pm", 
        "endTime": "03:00 pm"
      }, 
      {
        "id": 7, 
        "startTime": "03:00 pm", 
        "endTime": "04:00 pm"
      }
    ], 
    "description": "the museum is where you see museum stuff", 
    "imageUrl": "https://museum_url.jpg"
  }, 
  {
    "id": 2, 
    "name": "Zoo", 
    "timeSlots": [
      {
        "id": 1, 
        "startTime": "9:00 am"
        "endTime": "10:00 am", 
      }, 
      {
        "id": 2, 
        "startTime": "10:00 am", 
        "endPoint": "11:00 am"
      }, 
      {
        "id": "3", 
        "startTime": "11:00 am", 
        "endTime": "12:00 pm" 
      }, 
      {
        "id": 4, 
        "startTime": "12:00 pm", 
        "endTime": "01:00 pm"
      }, 
      {
        "id": 5, 
        "startTime": "01:00 pm", 
        "endTime": "02:00 pm", 
      }, 
      {
        "id": 6, 
        "startTime": "02:00 pm", 
        "endTime": "03:00 pm"
      }, 
      {
        "id": 7, 
        "startTime": "03:00 pm", 
        "endTime": "04:00 pm"
      }
    ], 
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

```bash 
  {
    "message": "payment successfully processed"
  }
```

```bash 
  {
    "message": "payment failed"
  }
```
