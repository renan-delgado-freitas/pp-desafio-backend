# Banking System

This is a simple banking system API built using FastAPI. It allows users to register, check user details, and perform money transfers between users. The system includes basic authorization and notification features.

## Instructions

- We have 2 types of users, ordinary users and shopkeepers, both have wallets with money and make transfers between them. We will only look at the transfer flow between two users.

- Requirements:

- For both types of users, we need Full Name, CPF, email and Password. CPF / CNPJ and e-mails must be unique in the system. Therefore, your system should allow only one registration with the same CPF or e-mail address.

- Users can send money (transfer) to shopkeepers and between users.

- Shopkeepers only receive transfers, they do not send money to anyone.

- Before finalising the transfer, an external authorising service must be consulted, use this mock to simulate (https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6).

- The transfer operation must be a transaction (i.e. reversed in any case of inconsistency) and the money must go back to the sending user's wallet.

- On payment receipt, the user or shopkeeper needs to receive notification (sending email, sms) sent by a third party service and eventually this service may be unavailable/unstable. Use this mock to simulate sending (http://o4d9z.mocklab.io/notify).

## Requirements

- Python 3.11

## Installation

1. Make sure you have Python 3.11 installed on your system.
2. Clone this repository: `git clone https://github.com/renan-delgado-freitas/pp-desafio-backend
3. Install the dependencies: `pip install -r requirements.txt`

## Usage

- To run the data processing, execute the following command:

- uvicorn main:app --host 0.0.0.0 --port 8000


# API Endpoints

## POST /register

#### Request Body:

{
  "name": "John Doe",
  "cpf_cnpj": "12345678905",
  "email": "john@example.com",
  "password": "securepassword",
  "balance": 200.00,
  "is_merchant": false
}


## GET /users

#### Response:

{
  "1": {
    "name": "João",
    "cpf_cnpj": "12345678900",
    "email": "j@j.com",
    "balance": 100.0,
    "is_merchant": false
  }
}


## POST /transaction

#### Request Body:

{
  "sender_id": 1,
  "recipient_id": 2,
  "amount": 50.0
}

#### Response:

[
  "Notification sent successfully",
  {
    "message": "Transfer successfully completed",
    "sender_balance": 50.0,
    "recipient_balance": 150.0
  }
]


