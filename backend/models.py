from sqlalchemy import INTEGER, TEXT, Column
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    username = Column(TEXT)
    password = Column(TEXT)
    roles = Column(TEXT)  # role_code_1,role_code_2,role_code_3
    refreshToken = Column(TEXT, nullable=True)
