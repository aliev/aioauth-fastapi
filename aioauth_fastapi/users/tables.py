from ..storage.tables import BaseTable
from sqlalchemy import (
    Column,
    String,
    Boolean,
)
from .crypto import make_random_password, pbkdf2, verify


class UserTable(BaseTable):
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    is_superuser = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        password = kwargs.pop("password", None)

        if password is not None:
            self.set_password(password)
        else:
            self.set_random_password()

        super().__init__(*args, password=self.password, **kwargs)

    def set_password(self, password) -> None:
        """
        Sets users password using pbkdf2.
        """
        self.password = pbkdf2(password)

    def set_random_password(self) -> str:
        """
        Set random password.
        """
        password = make_random_password()
        self.password = pbkdf2(password)
        return password

    def verify_password(self, password: str) -> bool:
        """
        Verify users password
        """
        return verify(password, self.password)
