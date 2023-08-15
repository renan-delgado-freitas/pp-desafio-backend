import httpx
import urllib3
import asyncio

from models import users, UserData, TransferData
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/users")
async def get_users():
    return users


@app.post("/register")
async def register_user(user_data: UserData):
    existing_user = next(
        (user for user in users.values() if user["cpf_cnpj"] == user_data.cpf_cnpj or user["email"] == user_data.email), None)
    if existing_user:
        return {"message": "CPF/CNPJ or e-mail already registered"}

    user_id = len(users) + 1
    users[user_id] = {
        "name": user_data.name,
        "cpf_cnpj": user_data.cpf_cnpj,
        "email": user_data.email,
        "password": user_data.password,
        "balance": user_data.balance,
        "is_merchant": user_data.is_merchant
    }

    return {"message": "User successfully registered", "user_id": user_id}


async def authorize_transfer(sender_id: int, amount: float):
    async with httpx.AsyncClient() as client:
        url = "https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6"
        response = await client.get(url)
        response_data = response.json()

        if not response_data.get("message") == "Autorizado":
            raise HTTPException(status_code=403, detail="Unauthorized transfer")


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
        return "Notification system down, confirmation notification cannot be sent. Log in to your app to verify transfer, and send the transfer receipt to the recipient."
    elif status == 200:
        return "Notification sent successfully"
    else:
        return "Notification was not sent"


@app.post("/transaction")
async def transfer_money(data: TransferData):
    sender = users.get(data.sender_id)
    recipient = users.get(data.recipient_id)

    if not sender or not recipient:
        return {"message": "User not found"}

    if sender["balance"] < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if sender["is_merchant"]:
        return {"message": "merchants cannot send transfers"}

    await authorize_transfer(data.sender_id, data.amount)

    sender["balance"] -= data.amount
    recipient["balance"] += data.amount

    # notification_sent = await check_status("http://google.com") # Usado apenas para teste, pois e um site que retorna status code 200
    notification_sent = await check_status("http://o4d9z.mocklab.io/notify")

    return notification_sent, {
        "message": "Transfer successfully completedo",
        "sender_balance": sender["balance"],
        "recipient_balance": recipient["balance"]
    }