from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    TIMESTAMP,
    ForeignKey,
    text,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from testdatabase import Base  # bas-klass för modellerna


class Members(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    membership_date = Column(Date, server_default=text("CURRENT_DATE"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    loans = relationship("Loans", back_populates="member")


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    loans = relationship("Loans", back_populates="book")

    __table_args__ = (
        CheckConstraint("total_copies >= 0", name="chk_total_nonneg"),
        CheckConstraint("available_copies >= 0", name="chk_avail_nonneg"),
    )


class Loans(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )
    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
    )
    loan_date = Column(Date, server_default=text("CURRENT_DATE"))
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    book = relationship("Books", back_populates="loans")
    member = relationship("Members", back_populates="loans")

    __table_args__ = (
        CheckConstraint("due_date >= loan_date", name="chk_due_after_loan"),
    )
