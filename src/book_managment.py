from testdatabase import get_session
from models import Books


def show_all_books():
    session = get_session()
    try:
        books = session.query(Books).order_by(Books.title).all()
        if not books:
            print("Inga böcker hittades.")
            return
        for b in books:
            print(f"{b.id}: {b.title} av {b.author}")
    finally:
        session.close()


def search_books():
    keyword = input("Sök titel eller författare: ").strip()
    session = get_session()
    try:
        books = (
            session.query(Books)
            .filter(
                (Books.title.ilike(f"%{keyword}%"))
                | (Books.author.ilike(f"%{keyword}%"))
            )
            .all()
        )
        if not books:
            print("Inga böcker matchade sökningen.")
            return
        for b in books:
            print(f"{b.id}: {b.title} av {b.author}")
    finally:
        session.close()


def add_new_book():
    title = input("Titel: ").strip()
    author = input("Författare: ").strip()
    if not title or not author:
        print("Titel och författare får inte vara tomma.")
        return

    session = get_session()
    try:
        book = Books(
            title=title,
            author=author,
            total_copies=1,
            available_copies=1,
        )
        session.add(book)
        session.commit()
        print("Bok tillagd.")
    finally:
        session.close()


def show_available_books():
    session = get_session()
    try:
        books = session.query(Books).filter(Books.available_copies > 0).all()
        if not books:
            print("Inga tillgängliga böcker just nu.")
            return
        for b in books:
            print(f"{b.id}: {b.title} ({b.available_copies} tillgängliga)")
    finally:
        session.close()


def book_menu():
    while True:
        print("\n--- Bokmeny ---")
        print("1. Visa alla böcker")
        print("2. Sök bok")
        print("3. Lägg till bok")
        print("4. Visa tillgängliga böcker")
        print("0. Tillbaka")
        val = input("Välj: ").strip()

        if val == "1":
            show_all_books()
        elif val == "2":
            search_books()
        elif val == "3":
            add_new_book()
        elif val == "4":
            show_available_books()
        elif val == "0":
            break
        else:
            print("Ogiltigt val.")
