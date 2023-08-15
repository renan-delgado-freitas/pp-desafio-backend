from pydantic import BaseModel
from typing import Dict


users: Dict[int, dict] = {
    1: {
        "name": "João",
        "cpf_cnpj": "12345678900",
        "email": "j@j.com",
        "password": "12345678",
        "balance": 100.00,
        "is_merchant": False
    },
    2: {
        "name": "Maria",
        "cpf_cnpj": "12345678901",
        "email": "m@m.com",
        "password": "12345678",
        "balance": 100.00,
        "is_merchant": True
    },
    3: {
        "name": "José",
        "cpf_cnpj": "12345678902",
        "email": "j@j.com",
        "password": "12345678",
        "balance": 100.00,
        "is_merchant": False
    },
    4: {
        "name": "Ana",
        "cpf_cnpj": "12345678903",
        "email": "a@a.com",
        "password": "12345678",
        "balance": 100.00,
        "is_merchant": True
    },
    5: {
        "name": "Renan",
        "cpf_cnpj": "12345678904",
        "email": "renan@gmail.com",
        "password": "12345678",
        "balance": 450.50,
        "is_merchant": False
    }
}


class TransferData(BaseModel):
    sender_id: int
    recipient_id: int
    amount: float


class UserData(BaseModel):
    name: str
    cpf_cnpj: str
    email: str
    password: str
    balance: float
    is_merchant: bool


