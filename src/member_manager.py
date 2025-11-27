from sqlalchemy import or_
from datetime import date

from testdatabase import get_session
from models import Members


def list_members():
    session = get_session()
    try:
        members = session.query(Members).order_by(
            Members.last_name, Members.first_name
        ).all()
        if not members:
            print("Inga medlemmar registrerade.")
            return
        for m in members:
            print(
                f"{m.id}: {m.first_name} {m.last_name} - {m.email} (medlem sedan {m.membership_date})"
            )
    finally:
        session.close()


def add_member():
    print("\n--- Lägg till medlem ---")
    first_name = input("Förnamn: ").strip()
    last_name = input("Efternamn: ").strip()
    email = input("E-post: ").strip()

    if not first_name or not last_name or not email:
        print("Förnamn, efternamn och e-post är obligatoriska.")
        return

    session = get_session()
    try:
        m = Members(
            first_name=first_name,
            last_name=last_name,
            email=email,
            membership_date=date.today(),
        )
        session.add(m)
        session.commit()
        print("Medlem tillagd.")
    finally:
        session.close()


def search_members():
    term = input("Sök på namn eller e-post: ").strip()
    term_like = f"%{term}%"

    session = get_session()
    try:
        members = (
            session.query(Members)
            .filter(
                or_(
                    Members.first_name.ilike(term_like),
                    Members.last_name.ilike(term_like),
                    Members.email.ilike(term_like),
                )
            )
            .all()
        )
        if not members:
            print("Inga medlemmar matchade sökningen.")
            return
        for m in members:
            print(
                f"{m.id}: {m.first_name} {m.last_name} - {m.email} (medlem sedan {m.membership_date})"
            )
    finally:
        session.close()


def member_menu():
    while True:
        print("\n--- Medlemsmeny ---")
        print("1. Visa alla medlemmar")
        print("2. Lägg till medlem")
        print("3. Sök medlem")
        print("0. Tillbaka")
        val = input("Välj: ").strip()

        if val == "1":
            list_members()
        elif val == "2":
            add_member()
        elif val == "3":
            search_members()
        elif val == "0":
            break
        else:
            print("Ogiltigt val.")
