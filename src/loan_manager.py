from datetime import date, timedelta

from sqlalchemy import and_

from testdatabase import get_session
from models import Loans, Books, Members


DEFAULT_LOAN_DAYS = 14


def create_loan():
    session = get_session()
    try:
        book_id = input("Ange bok-ID: ").strip()
        member_id = input("Ange medlems-ID: ").strip()

        if not book_id.isdigit() or not member_id.isdigit():
            print("Bok-ID och medlems-ID måste vara siffror.")
            return

        book = session.get(Books, int(book_id))
        member = session.get(Members, int(member_id))

        if not book:
            print("Boken hittades inte.")
            return
        if not member:
            print("Medlemmen hittades inte.")
            return
        if (book.available_copies or 0) <= 0:
            print("Ingen tillgänglig kopia av boken.")
            return

        loan_date = date.today()
        due_date = loan_date + timedelta(days=DEFAULT_LOAN_DAYS)

        loan = Loans(
            book_id=book.id,
            member_id=member.id,
            loan_date=loan_date,
            due_date=due_date,
        )
        book.available_copies = (book.available_copies or 0) - 1
        session.add(loan)
        session.commit()
        print(
            f"Lån skapat. Lån-ID: {loan.id}, förfaller: {loan.due_date} för bok '{book.title}' till {member.first_name} {member.last_name}.",
        )
    finally:
        session.close()


def return_loan():
    session = get_session()
    try:
        loan_id = input("Ange låne-ID att återlämna: ").strip()
        if not loan_id.isdigit():
            print("Låne-ID måste vara en siffra.")
            return

        loan = session.get(Loans, int(loan_id))
        if not loan:
            print("Lånet hittades inte.")
            return
        if loan.return_date is not None:
            print("Lånet är redan återlämnat.")
            return

        loan.return_date = date.today()
        book = session.get(Books, loan.book_id)
        if book:
            book.available_copies = (book.available_copies or 0) + 1
        session.commit()
        print("Lån återlämnat.")
    finally:
        session.close()


def list_active_loans():
    session = get_session()
    try:
        loans = session.query(Loans).filter(Loans.return_date.is_(None)).all()
        if not loans:
            print("Inga aktiva lån.")
            return
        for l in loans:
            print(
                f"Lån-ID {l.id}: Bok-ID {l.book_id}, Medlems-ID {l.member_id}, Lånedatum {l.loan_date}, Förfaller {l.due_date}"
            )
    finally:
        session.close()


def list_overdue_loans():
    session = get_session()
    try:
        today = date.today()
        loans = (
            session.query(Loans)
            .filter(and_(Loans.return_date.is_(None), Loans.due_date < today))
            .all()
        )
        if not loans:
            print("Inga försenade lån.")
            return
        for l in loans:
            print(
                f"FÖRSENAD - Lån-ID {l.id}: Bok-ID {l.book_id}, Medlems-ID {l.member_id}, Förfallodatum {l.due_date}"
            )
    finally:
        session.close()


def loan_menu():
    while True:
        print("\n--- Lånmeny ---")
        print("1. Skapa nytt lån")
        print("2. Återlämna lån")
        print("3. Visa aktiva lån")
        print("4. Visa försenade lån")
        print("0. Tillbaka")
        val = input("Välj: ").strip()

        if val == "1":
            create_loan()
        elif val == "2":
            return_loan()
        elif val == "3":
            list_active_loans()
        elif val == "4":
            list_overdue_loans()
        elif val == "0":
            break
        else:
            print("Ogiltigt val.")
