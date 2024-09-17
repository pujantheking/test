from uuid import UUID, uuid4

from sqlalchemy.orm import mapped_column, Mapped

from core.db import Base


class PaymentModel(Base):
    __tablename__ = "payments"
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    email: Mapped[str] = mapped_column()
    mobile: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()

    @classmethod
    def create(cls, email: str, mobile: str, amount: float):
        return cls(email=email, mobile=mobile, amount=amount)


