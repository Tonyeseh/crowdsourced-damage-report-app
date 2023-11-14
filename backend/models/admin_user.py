"""admin_user module"""

from models.base_user import BaseUser
from models.base_model import Base

class AdminUser(BaseUser, Base):
    """Representation of AdminUser"""

    