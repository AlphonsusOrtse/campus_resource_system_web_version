
import unittest

from app import create_app
from app.extensions import db
from app.models import Fellow, Loan, Resource


class RouteTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret",
        })

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_pages_load(self):
        pages = [
            "/",
            "/resources",
            "/fellows",
            "/loans",
            "/reports",
        ]

        for page in pages:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)

    def test_register_fellow(self):
        response = self.client.post(
            "/fellows/create",
            data={
                "fellow_id": "F001",
                "name": "John",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            db.session.query(Fellow).count(), 1
        )

    def test_create_resource(self):
        response = self.client.post(
            "/resources/create",
            data={
                "name": "Laptop",
                "category": "Electronics",
                "total_units": "5",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        resource = db.session.query(Resource).first()
        self.assertEqual(resource.available_units, 5)

    def test_invalid_resource_quantity(self):
        self.client.post(
            "/resources/create",
            data={
                "name": "Laptop",
                "category": "Electronics",
                "total_units": "-2",
            },
        )

        self.assertEqual(
            db.session.query(Resource).count(), 0
        )

    def test_borrow_and_return(self):
        self.client.post(
            "/fellows/create",
            data={"fellow_id": "F001", "name": "John"},
        )

        self.client.post(
            "/resources/create",
            data={
                "name": "Projector",
                "category": "Electronics",
                "total_units": "5",
            },
        )

        fellow = db.session.query(Fellow).first()
        resource = db.session.query(Resource).first()

        response = self.client.post(
            "/loans/borrow",
            data={
                "fellow_id": str(fellow.id),
                "resource_id": str(resource.id),
                "quantity": "2",
            },
        )

        self.assertEqual(response.status_code, 302)

        loan = db.session.query(Loan).first()
        self.assertIsNotNone(loan)
        self.assertEqual(resource.available_units, 3)

        response = self.client.post(
            f"/loans/{loan.id}/return"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resource.available_units, 5)
        self.assertIsNotNone(loan.returned_at)


    def test_foreign_keys_enabled(self):
        result = db.session.execute(
            db.text("PRAGMA foreign_keys")
        ).scalar()

        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()
