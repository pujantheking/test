from typing import Annotated

import requests
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from apps.payments.models import PaymentModel
from core.db import db_session, AsyncSession


router = APIRouter(tags=['Admin'])

@router.get(
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


@router.post(
    "/user/payment",
    description=""
)
async def checkout():
    url = "https://test.payu.in/_payment"

    payload = {
        "key": "string",
        "txnid": "ypl938459435",
        "amount": 0,
        "productinfo": "iPhone",
        "firstname": "string",
        "email": "string",
        "phone": 0,
        "hash": "string",
        "surl": "string",
        "furl": "string",
        "lastname": "string",
        "address1": "string",
        "address2": "string",
        "city": "string",
        "state": "string",
        "country": "string",
        "zipcode": "string",
        "enforce_paymethod": "creditcard|debitcard",
        "drop_category": "DC|VISA|MAST",
        "udf1": "string",
        "udf2": "DC|VISA|MAST",
        "udf3": "string",
        "udf4": "string",
        "udf5": "string"
    }

    headers = {
        "accept": "text/plain",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
    if "text/html" in response.headers.get("Content-Type", ""):
        return HTMLResponse(content=response.text)
    else:
        return {"error": "Invalid response from PayU"}

