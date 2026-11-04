
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from app.extensions import db
from app.models import Loan, Resource
from app.services.resources import (
    create_resource, list_resources, update_resource, delete_resource
)
from app.services.fellows import (
    create_fellow, list_fellows, update_fellow,
    graduate_fellow, delete_fellow
)
from app.services.loans import borrow_resource, return_resource, list_loans

main = Blueprint("main", __name__)


def perform(action, destination):
    try:
        action()
        flash("Operation completed successfully.", "success")
    except (ValueError, TypeError) as error:
        flash(str(error), "error")
    return redirect(url_for(destination))


def positive_id(value):
    number = int(value)
    if number <= 0:
        raise ValueError("ID must be positive")
    return number


@main.route("/")
def home():
    resources = list_resources()
    fellows = list_fellows()
    loans = list_loans()
    active = [loan for loan in loans if loan.returned_at is None]

    return render_template(
        "home.html",
        resource_count=len(resources),
        fellow_count=len(fellows),
        active_count=len(active),
        available=sum(r.available_units for r in resources),
    )


@main.route("/resources")
def resources():
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    items = list_resources()

    if search:
        items = [r for r in items if search in r.name.lower()]
    if category:
        items = [r for r in items if category in r.category.lower()]

    return render_template(
        "resources.html", resources=items,
        search=search, category=category
    )


@main.post("/resources/create")
def resource_create():
    return perform(
        lambda: create_resource(
            request.form.get("name", ""),
            request.form.get("category", ""),
            int(request.form.get("total_units", "")),
        ),
        "main.resources",
    )


@main.post("/resources/<int:resource_id>/update")
def resource_update(resource_id):
    return perform(
        lambda: update_resource(
            resource_id,
            request.form.get("name", ""),
            request.form.get("category", ""),
            int(request.form.get("total_units", "")),
        ),
        "main.resources",
    )


@main.post("/resources/<int:resource_id>/delete")
def resource_delete(resource_id):
    return perform(lambda: delete_resource(resource_id), "main.resources")


@main.route("/fellows")
def fellows():
    return render_template("fellows.html", fellows=list_fellows())


@main.post("/fellows/create")
def fellow_create():
    return perform(
        lambda: create_fellow(
            request.form.get("fellow_id", ""),
            request.form.get("name", ""),
        ),
        "main.fellows",
    )


@main.post("/fellows/<int:fellow_id>/update")
def fellow_update(fellow_id):
    return perform(
        lambda: update_fellow(fellow_id, request.form.get("name", "")),
        "main.fellows",
    )


@main.post("/fellows/<int:fellow_id>/graduate")
def fellow_graduate(fellow_id):
    return perform(lambda: graduate_fellow(fellow_id), "main.fellows")


@main.post("/fellows/<int:fellow_id>/delete")
def fellow_delete(fellow_id):
    return perform(lambda: delete_fellow(fellow_id), "main.fellows")


@main.route("/loans")
def loans():
    return render_template(
        "loans.html",
        loans=list_loans(),
        fellows=list_fellows(),
        resources=list_resources(),
    )


@main.post("/loans/borrow")
def loan_borrow():
    return perform(
        lambda: borrow_resource(
            positive_id(request.form.get("fellow_id", "")),
            positive_id(request.form.get("resource_id", "")),
            int(request.form.get("quantity", "")),
        ),
        "main.loans",
    )


@main.post("/loans/<int:loan_id>/return")
def loan_return(loan_id):
    return perform(lambda: return_resource(loan_id), "main.loans")


@main.route("/reports")
def reports():
    resources = list_resources()
    total = sum(r.total_units for r in resources)
    available = sum(r.available_units for r in resources)

    counts = db.session.execute(
        db.select(
            Loan.resource_id,
            func.sum(Loan.quantity).label("borrowed_count")
        ).group_by(Loan.resource_id)
    ).all()

    highest = max((row.borrowed_count for row in counts), default=0)
    most_borrowed = [
        (db.session.get(Resource, row.resource_id), row.borrowed_count)
        for row in counts
        if row.borrowed_count == highest and highest > 0
    ]

    return render_template(
        "reports.html",
        total=total,
        available=available,
        borrowed=total - available,
        low_stock=[r for r in resources if r.available_units < 3],
        most_borrowed=most_borrowed,
    )
