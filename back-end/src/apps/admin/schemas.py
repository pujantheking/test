from pydantic import BaseModel, EmailStr

class AddUserDetailsRequest(BaseModel):
    product_name: str
    firstname: str
    lastname: str
    company_name: str | None = None
    country: str
    town: str
    state: str
    zip: int
    phone: str
    email: EmailStr
    amount: float


class GetPaymentDetails(BaseModel):
    order_id: str
    firstname: str
    lastname: str
    payment_status: str
    amount: float
