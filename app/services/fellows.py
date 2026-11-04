
from app.extensions import db
from app.models import Fellow


def create_fellow(fellow_id, name):
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID is required")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Fellow name is required")

    fellow_id = fellow_id.strip()
    name = name.strip()

    if db.session.execute(
        db.select(Fellow).filter_by(fellow_id=fellow_id)
    ).scalar_one_or_none():
        raise ValueError("Fellow ID already exists")

    fellow = Fellow(
        fellow_id=fellow_id,
        name=name,
        graduated=False
    )

    db.session.add(fellow)
    db.session.commit()

    return fellow


def list_fellows():
    return db.session.execute(
        db.select(Fellow).order_by(Fellow.id)
    ).scalars().all()


def update_fellow(fellow_id, name):
    fellow = db.session.get(Fellow, fellow_id)

    if fellow is None:
        raise ValueError("Fellow not found")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Fellow name is required")

    fellow.name = name.strip()
    db.session.commit()

    return fellow


def graduate_fellow(fellow_id):
    fellow = db.session.get(Fellow, fellow_id)

    if fellow is None:
        raise ValueError("Fellow not found")

    if any(loan.returned_at is None for loan in fellow.loans):
        raise ValueError("Fellow has outstanding loans")

    fellow.graduated = True
    db.session.commit()

    return fellow


def delete_fellow(fellow_id):
    fellow = db.session.get(Fellow, fellow_id)

    if fellow is None:
        raise ValueError("Fellow not found")

    if not fellow.graduated:
        raise ValueError("Only graduated fellows can be deleted")

    if fellow.loans:
        raise ValueError(
            "Cannot delete fellow with borrowing history"
        )

    db.session.delete(fellow)
    db.session.commit()

    return True
