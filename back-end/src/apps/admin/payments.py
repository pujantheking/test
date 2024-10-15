from uuid import uuid4
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from apps.payments.models import PaymentModel
from apps.admin.schemas import AddUserDetailsRequest
from core.db import db_session, AsyncSession


router = APIRouter(tags=['Admin'])
templates = Jinja2Templates(directory='htmldir')

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
