from datetime import date
from sqlalchemy import func, desc

from testdatabase import get_session
from models import Books, Members, Loans


def show_most_borrowed_books():
    """Visa böcker sorterade efter antal lån (mest lånade först)."""
    session = get_session()
    try:
        results = (
            session.query(
                Books.title,
                Books.author,
                func.count(Loans.id).label("loan_count"),
            )
            .join(Loans, Loans.book_id == Books.id)
            .group_by(Books.id)
            .order_by(desc("loan_count"))
            .limit(10)
            .all()
        )

        if not results:
            print("\nInga lån har registrerats ännu. Kan inte visa mest lånade böcker.")
            return

        print("\n--- Mest lånade böcker ---")
        for title, author, count in results:
            print(f"{title} av {author} – {count} lån totalt")
    finally:
        session.close()


def show_top_member():
    """Visa medlem eller medlemmar med flest lån."""
    session = get_session()
    try:
        results = (
            session.query(
                Members.id,
                Members.first_name,
                Members.last_name,
                func.count(Loans.id).label("loan_count"),
            )
            .join(Loans, Loans.member_id == Members.id)
            .group_by(Members.id)
            .order_by(desc("loan_count"))
            .all()
        )

        if not results:
            print("\nInga lån har registrerats ännu. Kan inte visa medlem med flest lån.")
            return

        # Hitta max antal lån
        max_loans = results[0].loan_count
        top_members = [m for m in results if m.loan_count == max_loans]

        print("\n--- Medlem/medlemmar med flest lån ---")
        for m in top_members:
            print(f"ID {m.id}: {m.first_name} {m.last_name} – {m.loan_count} lån totalt")
    finally:
        session.close()


def show_library_overview():
    """Visa översikt över biblioteket."""
    session = get_session()
    try:
        num_book_titles = session.query(func.count(Books.id)).scalar() or 0
        total_copies = session.query(func.coalesce(func.sum(Books.total_copies), 0)).scalar() or 0
        num_members = session.query(func.count(Members.id)).scalar() or 0

        active_loans = (
            session.query(func.count(Loans.id))
            .filter(Loans.return_date.is_(None))
            .scalar()
            or 0
        )

        today = date.today()
        overdue_loans = (
            session.query(func.count(Loans.id))
            .filter(
                Loans.return_date.is_(None),
                Loans.due_date < today
            )
            .scalar()
            or 0
        )

        print("\n--- Biblioteksöversikt ---")
        print(f"Antal boktitlar: {num_book_titles}")
        print(f"Totalt antal exemplar: {total_copies}")
        print(f"Antal medlemmar: {num_members}")
        print(f"Aktiva lån: {active_loans}")
        print(f"Försenade lån: {overdue_loans}")
    finally:
        session.close()


def stats_menu():
    """Meny för statistik och rapporter."""
    while True:
        print("\n--- Statistik & Rapporter ---")
        print("1. Visa mest lånade böcker")
        print("2. Visa medlem med flest lån")
        print("3. Visa översikt av biblioteket")
        print("0. Tillbaka")

        val = input("Välj: ").strip()

        if val == "1":
            show_most_borrowed_books()
        elif val == "2":
            show_top_member()
        elif val == "3":
            show_library_overview()
        elif val == "0":
            break
        else:
            print("Ogiltigt val.")