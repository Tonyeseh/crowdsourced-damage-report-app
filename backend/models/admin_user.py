"""admin_user module"""

from models.base_user import BaseUser
from models.base_model import Base

class AdminUser(BaseUser, Base):
    """Representation of AdminUser"""
    __tablename__ = "admin_users"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    