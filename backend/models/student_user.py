"""student_user module"""

from models.base_model import Base
from models.base_user import BaseUser

from sqlalchemy.orm import relationship


class StudentUser(BaseUser, Base):
    """Representation of a StudentUser"""

    __tablename__ = "student_users"
    reports = relationship("Damage", backref="student_users")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
