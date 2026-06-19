# Inventory System Practice

A simple but well-structured inventory management application designed for practicing real GitHub workflows: branches, issues, pull requests, code review, and team collaboration.

## Description

This project provides a functional inventory system where you can manage products, monitor low stock alerts, and explore both a web interface and a REST API. It is intentionally kept simple so students and teammates can focus on collaboration practices rather than complex infrastructure.

## Tech Stack

- **Python**
- **FastAPI** — backend framework and API
- **SQLite** — local database
- **SQLAlchemy** — ORM and database management
- **Pydantic** — data validation
- **Uvicorn** — ASGI server
- **Jinja2** — HTML templates
- **HTML, CSS, JavaScript** — frontend (no external CSS frameworks)

## Requirements

- Python 3.10 or higher
- pip
- Git

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd inventory-system-practice

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (Git Bash):
source .venv/Scripts/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## How to Run

```bash
uvicorn main:app --reload
```

Open the application in your browser:

- **Web app:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Main Routes

### Web Pages

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard |
| GET | `/products` | Product list with search and filters |
| GET | `/products/create` | Create product form |
| POST | `/products/create` | Save new product |
| GET | `/products/{id}` | Product detail |
| GET | `/products/{id}/edit` | Edit product form |
| POST | `/products/{id}/edit` | Update product |
| POST | `/products/{id}/delete` | Delete product |

### API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/products` | List products (supports search/filters) |
| GET | `/api/products/{id}` | Get product by ID |
| POST | `/api/products` | Create product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |
| GET | `/api/dashboard` | Dashboard statistics |

## API Documentation

FastAPI generates interactive API documentation automatically:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
inventory-system-practice/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── instance/              # SQLite database (not committed)
├── app/
│   ├── database.py        # DB connection and session
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   └── routes/
│       ├── pages.py       # HTML page routes
│       └── products.py    # API routes
├── templates/             # Jinja2 HTML templates
├── static/                # CSS and JavaScript
└── docs/                  # Additional documentation
```

## GitHub Workflow

This project is designed to practice collaborative development:

1. Create an issue describing the task
2. Create a branch from `develop`
3. Implement changes and commit with clear messages
4. Push the branch and open a Pull Request
5. Request code review from a teammate
6. Address feedback and merge when approved

See [docs/workflow.md](docs/workflow.md) for detailed steps.

### Recommended Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable production-ready code |
| `develop` | Integration branch for features |
| `feature/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation updates |

### Commit Convention

Use conventional commits:

```
feat: add product search filter
fix: correct low stock calculation
docs: update setup instructions
refactor: simplify crud functions
```

## Current Features

- Dashboard with inventory metrics
- Full product CRUD (create, read, update, delete)
- Low stock alerts and visual indicators
- Search by product name
- Filter by category and low stock status
- REST API endpoints for backend practice
- Responsive web design
- Sample data seeded on first run

## Future Features

- Dedicated categories module
- User authentication and roles
- Stock movement history
- Export inventory to CSV
- Pagination for large product lists
- Unit and integration tests
- Docker support

## Additional Documentation

- [Setup Guide](docs/setup.md)
- [GitHub Workflow](docs/workflow.md)
- [Database Guide](docs/database.md)
