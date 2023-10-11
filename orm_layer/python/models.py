from typing import List
from json import dumps
from sqlalchemy import DateTime, ForeignKey, Table, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


debate_debate_category_table = Table(
    "debate_debate_category_table",
    Base.metadata,
    Column("debate_id", ForeignKey("debate.id"), primary_key=True),
    Column("debate_category_id", ForeignKey("debate_category.id"), primary_key=True),
)


class Debate(Base):
    __tablename__ = "debate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    end_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    picture_url: Mapped[str] = mapped_column(String, nullable=True)
    winner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id])
    winner: Mapped["User"] = relationship(foreign_keys=[winner_id])
    debate_categories: Mapped[List["DebateCategory"]] = relationship(
        secondary=debate_debate_category_table, back_populates="debates"
    )
    responses: Mapped[List["Response"]] = relationship(back_populates="debate")

    def __repr__(self):
        return f"""
        <Debate(id: {self.id}, title: {self.title}, summary: {self.summary}, created_at: {self.created_at},
        created_by_id: {self.created_by_id}, end_at: {self.end_at}, picture_url: {self.picture_url}
        winner_id: {self.winner_id})>
        """


class DebateCategory(Base):
    __tablename__ = "debate_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))

    debates: Mapped[List["Debate"]] = relationship(
        secondary=debate_debate_category_table, back_populates="debate_categories"
    )

    def __repr__(self):
        return f"""
        <DebateCategory(id: {self.id}, name: {self.name})>
        """


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    profile_picture_url: Mapped[str] = mapped_column(String, nullable=True)

    responses: Mapped[List["Response"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"""
        <User(id: {self.id}, username: {self.username}, profile_picture_url: {self.profile_picture_url})>
        """


class Response(Base):
    __tablename__ = "response"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(String)
    agree: Mapped[int] = mapped_column(Integer)
    disagree: Mapped[int] = mapped_column(Integer)
    debate_id: Mapped[int] = mapped_column(ForeignKey("debate.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    debate: Mapped["Debate"] = relationship(back_populates="responses")
    user: Mapped["User"] = relationship(back_populates="responses")

    def __repr__(self):
        return f"""
        <Response(id: {self.id}, body: {self.body}, agree: {self.agree}, disagree: {self.disagree},
        debate_id: {self.debate_id}, user_id: {self.user_id})>
        """
