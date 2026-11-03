
from datetime import datetime, timezone

from app.extensions import db


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    total_units = db.Column(db.Integer, nullable=False)
    available_units = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "total_units >= 0",
            name="check_total_nonnegative"
        ),
        db.CheckConstraint(
            "available_units >= 0",
            name="check_available_nonnegative"
        ),
        db.CheckConstraint(
            "available_units <= total_units",
            name="check_available_within_total"
        ),
    )


class Fellow(db.Model):
    __tablename__ = "fellows"

    id = db.Column(db.Integer, primary_key=True)
    fellow_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    graduated = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)

    fellow_id = db.Column(
        db.Integer,
        db.ForeignKey("fellows.id"),
        nullable=False
    )

    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    borrowed_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    returned_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            "quantity > 0",
            name="check_loan_quantity_positive"
        ),
    )

    fellow = db.relationship("Fellow", backref="loans")
    resource = db.relationship("Resource", backref="loans")
