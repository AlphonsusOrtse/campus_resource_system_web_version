
from app.extensions import db
from app.models import Resource


def create_resource(name, category, total_units):
    name = name.strip()
    category = category.strip()

    if not name or not category:
        raise ValueError("Name and category are required")

    if type(total_units) is not int or total_units <= 0:
        raise ValueError("Total units must be a positive integer")

    resource = Resource(
        name=name,
        category=category,
        total_units=total_units,
        available_units=total_units
    )

    db.session.add(resource)
    db.session.commit()

    return resource


def list_resources():
    return db.session.execute(
        db.select(Resource).order_by(Resource.id)
    ).scalars().all()


def update_resource(resource_id, name, category, total_units):
    resource = db.session.get(Resource, resource_id)

    if resource is None:
        raise ValueError("Resource not found")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Resource name is required")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category is required")

    if type(total_units) is not int or total_units < 0:
        raise ValueError("Total units must be a non-negative integer")

    borrowed_units = resource.total_units - resource.available_units

    if total_units < borrowed_units:
        raise ValueError("Total units cannot be less than borrowed units")

    resource.name = name.strip()
    resource.category = category.strip()
    resource.total_units = total_units
    resource.available_units = total_units - borrowed_units

    db.session.commit()

    return resource


def delete_resource(resource_id):
    resource = db.session.get(Resource, resource_id)

    if resource is None:
        raise ValueError("Resource not found")

    if resource.loans:
        raise ValueError(
            "Cannot delete a resource with borrowing history"
        )

    db.session.delete(resource)
    db.session.commit()

    return True

