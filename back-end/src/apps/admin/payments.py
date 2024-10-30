from uuid import uuid4
from typing import Annotated

from pydantic import BaseModel
import requests
from fastapi import APIRouter, Depends, Body, Request, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from apps.payments.models import PaymentModel
from apps.admin.schemas import AddUserDetailsRequest
from core.db import db_session, AsyncSession

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

app = FastAPI()
templates = Jinja2Templates(directory='htmldir')

@app.get(
    "/admin/payments",
    description="Get Payments",
    name="Get Payments",
    operation_id="get_payments"
)
async def get_payments(
        session: Annotated[AsyncSession, Depends(db_session)],
        page_params: Annotated[Params, Depends()]
):

    payments = (select(PaymentModel))

    return await paginate(session, payments, page_params)


@app.post(
    "/user/payment",
    description="Add user details",
    name="Add users details",
    operation_id="add_user_details",
    response_class=HTMLResponse
)
async def add_user_details(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_session)],
        body: Annotated[AddUserDetailsRequest, Body()]
):
    # payment = PaymentModel.create(
    #         firstname=body.firstname,
    #         lastname=body.lastname,
    #         company_name=body.company_name,
    #         order_id=f"{body.product_name}_{uuid4()}",
    #         country=body.country,
    #         zip=body.zip,
    #         town=body.town,
    #         email=body.email,
    #         phone=body.phone,
    #         state=body.state,
    #         amount=body.amount
    #     )
    # session.add(payment)

    return templates.TemplateResponse("checkout.html", {"request": request})


class TokenRequest(BaseModel):
    txnId: str
    consumerId: str
    amount: str

def encrypt_data(data, key, iv):
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * ' '
    encrypted = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')

@app.post("/generate-token")
async def generate_token(request: TokenRequest):
    # Extract data from the request
    txn_id = request.txnId
    consumer_id = request.consumerId
    amount = request.amount

    # Merchant and encryption details
    merchant_id = 'T1043733'
    encryption_key = '5981514647TMLRTF'
    encryption_iv = '8132655595JJDQLP'

    # Concatenate the string to be encrypted
    data_string = f"{merchant_id}|{txn_id}|{amount}|{consumer_id}"

    # Encrypt the data
    token = encrypt_data(data_string, encryption_key, encryption_iv)

    return {"token": token}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)