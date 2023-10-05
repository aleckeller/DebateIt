from typing import List
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

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    summary: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    end_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    picture_url: Mapped[str] = mapped_column(String, nullable=True)
    winner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    created_by: Mapped["User"] = relationship(back_populates="debates")
    winner: Mapped["User"] = relationship(back_populates="debates")
    debate_categories: Mapped[List["DebateCategory"]] = relationship(
        secondary=debate_debate_category_table, back_populates="debates"
    )
    responses: Mapped[List["Response"]] = relationship(back_populates="debate")


class DebateCategory(Base):
    __tablename__ = "debate_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    debates: Mapped[List["Debate"]] = relationship(
        secondary=debate_debate_category_table, back_populates="debate_categories"
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    profile_picture_url: Mapped[str] = mapped_column(String, nullable=True)

    responses: Mapped[List["Response"]] = relationship(back_populates="user")
    debates_won: Mapped[List["Debate"]] = relationship(back_populates="user")
    debates_created: Mapped[List["Debate"]] = relationship(back_populates="user")


class Response(Base):
    __tablename__ = "response"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String)
    agree: Mapped[int] = mapped_column(Integer)
    disagree: Mapped[int] = mapped_column(Integer)
    debate_id: Mapped[int] = mapped_column(ForeignKey("debate.id"))
    debate: Mapped["Debate"] = relationship(back_populates="responses")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="responses")
