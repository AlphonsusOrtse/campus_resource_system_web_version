
from datetime import datetime, timezone

from app.extensions import db
from app.models import Fellow, Loan, Resource


def borrow_resource(fellow_id, resource_id, quantity):
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")

    fellow = db.session.get(Fellow, fellow_id)
    resource = db.session.get(Resource, resource_id)

    if fellow is None:
        raise ValueError("Fellow not found")

    if fellow.graduated:
        raise ValueError("Graduated fellows cannot borrow resources")

    if resource is None:
        raise ValueError("Resource not found")

    if quantity > resource.available_units:
        raise ValueError("Insufficient available stock")

    loan = Loan(
        fellow_id=fellow.id,
        resource_id=resource.id,
        quantity=quantity
    )

    resource.available_units -= quantity
    db.session.add(loan)
    db.session.commit()

    return loan


def return_resource(loan_id):
    loan = db.session.get(Loan, loan_id)

    if loan is None:
        raise ValueError("Loan not found")

    if loan.returned_at is not None:
        raise ValueError("Loan has already been returned")

    resource = db.session.get(Resource, loan.resource_id)

    if resource is None:
        raise ValueError("Associated resource not found")

    if resource.available_units + loan.quantity > resource.total_units:
        raise ValueError("Return would exceed total stock")

    resource.available_units += loan.quantity
    loan.returned_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.session.commit()

    return loan


def list_loans():
    return db.session.execute(
        db.select(Loan).order_by(Loan.id)
    ).scalars().all()
