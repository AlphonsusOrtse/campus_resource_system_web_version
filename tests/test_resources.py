
import unittest

from app import create_app
from app.extensions import db
from app.models import Resource
from app.services.resources import (
    create_resource,
    list_resources,
    update_resource,
    delete_resource,
)


class ResourceTests(unittest.TestCase):

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
        resource = create_resource("Laptop", "Electronics", 10)

        self.assertEqual(resource.available_units, 10)
        self.assertEqual(len(list_resources()), 1)

    def test_update(self):
        resource = create_resource("Projector", "Electronics", 5)

        updated = update_resource(
            resource.id, "Projector", "Electronics", 8
        )

        self.assertEqual(updated.total_units, 8)
        self.assertEqual(updated.available_units, 8)

    def test_delete(self):
        resource = create_resource("Chair", "Furniture", 3)
        resource_id = resource.id

        delete_resource(resource_id)

        self.assertIsNone(db.session.get(Resource, resource_id))

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            create_resource("Laptop", "Electronics", -5)

        self.assertEqual(len(list_resources()), 0)


if __name__ == "__main__":
    unittest.main()
