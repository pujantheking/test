from uuid import UUID, uuid4

from sqlalchemy.orm import mapped_column, Mapped

from core.db import Base
from core.types import PaymentStatusType


class PaymentModel(Base):
    __tablename__ = "payments"
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    company_name: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column()
    town: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()
    zip: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    transaction_id: Mapped[str] = mapped_column(nullable=True)
    order_id: Mapped[str] = mapped_column()
    payment_status: Mapped[str] = mapped_column()

    @classmethod
    def create(
            cls,
            firstname: str,
            lastname: str,
            country: str,
            town: str,
            state: str,
            zip: int,
            order_id: str,
            phone: str,
            email: str,
            amount: float,
            company_name: str | None = None
    ):
        return cls(
            firstname=firstname,
            lastname=lastname,
            country=country,
            town=town,
            state=state,
            zip=zip,
            order_id=order_id,
            phone=phone,
            email=email,
            amount=amount,
            company_name=company_name,
            payment_status=PaymentStatusType.REQUESTED,
        )


