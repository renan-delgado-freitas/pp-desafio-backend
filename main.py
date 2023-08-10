import httpx
import urllib3
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


app = FastAPI()

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
        "name": "Renan Freitas",
        "cpf_cnpj": "12345678904",
        "email": "renanfreeiitas@gmail.com",
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


@app.get("/users")
async def get_users():
    return users


@app.post("/register")
async def register_user(user_data: UserData):
    existing_user = next(
        (user for user in users.values() if user["cpf_cnpj"] == user_data.cpf_cnpj or user["email"] == user_data.email), None)
    if existing_user:
        return {"message": "CPF/CNPJ ou e-mail já cadastrados"}

    user_id = len(users) + 1
    users[user_id] = {
        "name": user_data.name,
        "cpf_cnpj": user_data.cpf_cnpj,
        "email": user_data.email,
        "password": user_data.password,
        "balance": user_data.balance,
        "is_merchant": user_data.is_merchant
    }

    return {"message": "Usuário cadastrado com sucesso", "user_id": user_id}


async def authorize_transfer(sender_id: int, amount: float):
    async with httpx.AsyncClient() as client:
        url = "https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6"
        response = await client.get(url)
        response_data = response.json()

        if not response_data.get("message") == "Autorizado":
            raise HTTPException(status_code=403, detail="Transferência não autorizada")


def get_url(url):
    http = urllib3.PoolManager()
    try:
        get_site = http.request("GET", url, timeout=15.0)
        return get_site.status

    except urllib3.exceptions.MaxRetryError:
        return None


async def check_status(url):
    loop = asyncio.get_event_loop()
    try:
        status = await asyncio.wait_for(loop.run_in_executor(None, get_url, url), timeout=15)
    except asyncio.TimeoutError:
        status = None

    if status is None:
        return "Sistema de notificacao fora do ar, notificacao de confirmacao nao pode ser enviada. Entre no seu app para verificar transferencia, e enviei o comprovante de transferencia ao recebedor"
    elif status == 200:
        return "Notificacao enviada com sucesso"
    else:
        return "Notificacao nao foi enviada"


@app.post("/transaction")
async def transfer_money(data: TransferData):
    sender = users.get(data.sender_id)
    recipient = users.get(data.recipient_id)

    if not sender or not recipient:
        return {"message": "User not found"}

    if sender["balance"] < data.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    if sender["is_merchant"]:
        return {"message": "Lojistas não podem enviar transferências"}

    await authorize_transfer(data.sender_id, data.amount)

    sender["balance"] -= data.amount
    recipient["balance"] += data.amount

    # notification_sent = await check_status("http://google.com") # Usado apenas para teste, pois e um site que retorna status code 200
    notification_sent = await check_status("http://o4d9z.mocklab.io/notify")

    return notification_sent, {
        "message": "Transferência realizada com sucesso",
        "sender_balance": sender["balance"],
        "recipient_balance": recipient["balance"]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
