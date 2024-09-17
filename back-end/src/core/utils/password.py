import re
from typing import Match


def strong_password(password) -> Match[str] | None:
    """
    Password checker.
    """

    return re.search(r"^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d)(?=[^#?!@$%^&*-]*[#?!@$%^&*-]).{8,}$", password, re.I)
