from sqlalchemy import Column, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship

from .database import Base
from .model_enums import RolesEnum


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True, unique=True, nullable=False)
    second_blocks_spent = Column(Integer, nullable=False, default=0)
    character_blocks_spent = Column(Integer, nullable=False, default=0)
    tokens_spent = Column(Integer, nullable=False, default=0)

    messages = relationship('UserMessage', back_populates='user')


class UserMessage(Base):

    __tablename__ = 'user_messages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(
        Enum(RolesEnum, name='roles_enum', values_callable=lambda roles: [role.value for role in roles]),
        nullable=False,
    )
    text = Column(String, nullable=False)

    user = relationship('User', back_populates='messages')
