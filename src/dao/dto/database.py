from datetime import date
from typing import List

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column(default='')
    user_name: Mapped[str] = mapped_column(default='')

    birthday: Mapped[date] = mapped_column(Date)

    chats: Mapped[List["Association"]] = relationship(back_populates="user")


class Chat(Base):
    __tablename__ = "chat"
    __table_args__ = {"schema": "public"}
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column()
    users: Mapped[List["Association"]] = relationship(back_populates="chat")


class Association(Base):
    __tablename__ = "user_chat"
    __table_args__ = {"schema": "public"}

    user_id: Mapped[int] = mapped_column(ForeignKey("public.user.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("public.chat.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="chats")
    chat: Mapped["Chat"] = relationship(back_populates="users")

