from strenum import StrEnum


class RoleType(StrEnum):
    """
    Enum class of Role type
    """

    ADMIN = "ADMIN"
    USER = "USER"

class PaymentStatusType(StrEnum):

    REQUESTED = "REQUESTED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


