
import unittest

from app import create_app
from app.extensions import db
from app.models import Loan, Resource
from app.services.resources import create_resource
from app.services.fellows import create_fellow
from app.services.loans import (
    borrow_resource,
    return_resource,
    list_loans,
)


class LoanTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.fellow = create_fellow("F001", "John")
        self.resource = create_resource(
            "Projector", "Electronics", 5
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_borrow_resource(self):
        loan = borrow_resource(
            self.fellow.id, self.resource.id, 2
        )

        self.assertEqual(loan.quantity, 2)
        self.assertEqual(self.resource.available_units, 3)
        self.assertEqual(len(list_loans()), 1)

    def test_return_resource(self):
        loan = borrow_resource(
            self.fellow.id, self.resource.id, 2
        )

        return_resource(loan.id)

        self.assertEqual(self.resource.available_units, 5)
        self.assertIsNotNone(loan.returned_at)

    def test_insufficient_stock(self):
        with self.assertRaises(ValueError):
            borrow_resource(self.fellow.id, self.resource.id, 6)

        self.assertEqual(self.resource.available_units, 5)
        self.assertEqual(len(list_loans()), 0)

    def test_double_return(self):
        loan = borrow_resource(
            self.fellow.id, self.resource.id, 2
        )

        return_resource(loan.id)

        with self.assertRaises(ValueError):
            return_resource(loan.id)

        self.assertEqual(self.resource.available_units, 5)

    def test_invalid_quantity(self):
        for quantity in [0, -1, True]:
            with self.assertRaises(ValueError):
                borrow_resource(
                    self.fellow.id, self.resource.id, quantity
                )

        self.assertEqual(len(list_loans()), 0)


if __name__ == "__main__":
    unittest.main()
