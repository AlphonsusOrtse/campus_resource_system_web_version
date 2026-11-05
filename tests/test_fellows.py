
import unittest

from app import create_app
from app.extensions import db
from app.models import Fellow
from app.services.fellows import (
    create_fellow,
    list_fellows,
    update_fellow,
    graduate_fellow,
    delete_fellow,
)


class FellowTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_and_list(self):
        fellow = create_fellow("F001", "John")

        self.assertEqual(fellow.name, "John")
        self.assertEqual(len(list_fellows()), 1)

    def test_duplicate_fellow(self):
        create_fellow("F001", "John")

        with self.assertRaises(ValueError):
            create_fellow("F001", "Mary")

    def test_update_fellow(self):
        fellow = create_fellow("F002", "Mary")

        updated = update_fellow(fellow.id, "Mary James")

        self.assertEqual(updated.name, "Mary James")

    def test_graduate_and_delete(self):
        fellow = create_fellow("F003", "Peter")
        fellow_id = fellow.id

        graduate_fellow(fellow_id)
        delete_fellow(fellow_id)

        self.assertIsNone(db.session.get(Fellow, fellow_id))

    def test_cannot_delete_active_fellow(self):
        fellow = create_fellow("F004", "Grace")

        with self.assertRaises(ValueError):
            delete_fellow(fellow.id)

    def test_case_insensitive_fellow_id(self):
        first = create_fellow("f001", "John")

        self.assertEqual(first.fellow_id, "F001")

        with self.assertRaises(ValueError):
            create_fellow("F001", "Mary")

        self.assertEqual(len(list_fellows()), 1)

if __name__ == "__main__":
    unittest.main()
