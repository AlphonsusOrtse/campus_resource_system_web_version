# Campus Resource Management System

A Flask-based web application for managing campus resources, fellows, borrowing, returns, and inventory reports.

## Features

### Resource Management
- Register resources with names, categories, and quantities.
- View, search, and filter resources.
- Update resource details and quantities.
- Delete resources without borrowing history.
- Prevent invalid stock quantities.

### Fellow Management
- Register fellows using unique registration IDs.
- View and update fellow information.
- Graduate fellows without outstanding loans.
- Delete graduated fellows without borrowing history.

### Borrowing and Returns
- Assign resources to registered, active fellows.
- Validate available stock before borrowing.
- Automatically decrease available inventory when borrowing.
- Restore available inventory when resources are returned.
- Prevent duplicate returns.
- Preserve borrowing history.

### Dashboard and Reports
- Display resource, fellow, and active-loan counts.
- Track total, available, and borrowed units.
- Identify resources with fewer than three available units.
- Identify the most borrowed resources, including ties.

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- HTML, CSS, and Jinja2
- Python unittest

## Project Structure

```text
campus_resource_system_web_version/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resources.py
│   │   ├── fellows.py
│   │   └── loans.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── resources.html
│   │   ├── fellows.html
│   │   ├── loans.html
│   │   └── reports.html
│   └── static/css/style.css
├── tests/
│   ├── test_resources.py
│   ├── test_fellows.py
│   ├── test_loans.py
│   └── test_routes.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/AlphonsusOrtse/campus_resource_system_web_version.git
cd campus_resource_system_web_version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python -c "from app import create_app; from app.extensions import db; app = create_app(); ctx = app.app_context(); ctx.push(); db.create_all(); ctx.pop()"
```

Start the application:

```bash
python run.py
```

Open `http://127.0.0.1:5000` in your browser.

## Running Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover resource management, fellow management, borrowing, returns, browser routes, and SQLite foreign-key enforcement.

## Database Integrity

The application uses database constraints to prevent negative inventory quantities and invalid loan quantities.

SQLite foreign-key enforcement is enabled for database connections.

The database is stored locally and excluded from Git version control.

## Current Scope

This project is a functional local MVP intended for development, learning, and portfolio demonstration.

It is not yet suitable for public multi-user deployment. Before production deployment, it needs authentication, authorization, CSRF protection, secure configuration, and stronger concurrent inventory updates.

## Future Improvements

- User authentication and role-based access
- Improved mobile interface
- Pagination and advanced inventory filtering
- CSV/PDF report exports
- Database migrations
- Production deployment

## Author

Alphonsus Ortse

GitHub: https://github.com/AlphonsusOrtse

Portfolio: https://alphonsusortse.github.io
