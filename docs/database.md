# Database Guide

This document describes how the Inventory System Practice project uses SQLite.

## Database Engine

The project uses **SQLite**, a lightweight file-based database ideal for local development and learning projects. No separate database server is required.

## Database Location

The database file is stored at:

```
instance/inventory.db
```

This path is configured in `app/database.py`. The `instance/` folder is created automatically if it does not exist.

## Tables

On first startup, the application creates one table:

### `products`

| Column | Type | Constraints | Description |
|--------|------|-------------|-----------|
| `id` | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| `name` | VARCHAR(255) | NOT NULL | Product name |
| `description` | TEXT | NULLABLE | Optional description |
| `category` | VARCHAR(100) | NOT NULL | Category as free text |
| `price` | FLOAT | NOT NULL, default 0 | Unit price |
| `current_stock` | INTEGER | NOT NULL, default 0 | Current inventory count |
| `minimum_stock` | INTEGER | NOT NULL, default 0 | Minimum stock threshold |
| `created_at` | DATETIME | NOT NULL | Record creation timestamp |
| `updated_at` | DATETIME | NOT NULL | Last update timestamp |

## How the Database Is Created

1. When the app starts (`uvicorn main:app --reload`), the `lifespan` handler in `main.py` runs
2. `Base.metadata.create_all(bind=engine)` creates all tables defined in SQLAlchemy models
3. If the `products` table is empty, sample data is inserted automatically

You do not need to run migrations or SQL scripts manually.

## Sample Data

If no products exist, the app inserts 5 sample items:

| Name | Category | Price | Current Stock | Min Stock | Low Stock? |
|------|----------|-------|---------------|-----------|------------|
| Wireless Mouse | Electronics | $24.99 | 45 | 10 | No |
| Notebook A5 | Stationery | $5.50 | 8 | 15 | Yes |
| USB-C Cable | Electronics | $12.00 | 3 | 5 | Yes |
| Desk Lamp | Furniture | $35.00 | 12 | 5 | No |
| Ballpoint Pen Pack | Stationery | $3.25 | 50 | 20 | No |

A product is considered **low stock** when `current_stock <= minimum_stock`.

## Why `inventory.db` Is Not Committed to Git

The database file is excluded in `.gitignore`:

```
instance/*.db
```

Reasons:

1. **Local data** — Each developer has their own test data
2. **Avoid conflicts** — Binary database files cause painful merge conflicts
3. **Security** — Future sensitive data should not end up in the repository
4. **Reproducibility** — The app recreates the schema and seeds data automatically

Only `instance/.gitkeep` is tracked so the folder structure exists after cloning.

## Resetting the Database

To start fresh:

```bash
# Stop the server first (Ctrl+C)
rm instance/inventory.db
uvicorn main:app --reload
```

The database will be recreated with sample data on the next startup.

## Good Practices

- Do not commit `.db` files to Git
- Use the API or web interface to manage data during development
- If you add new columns or tables later, document the changes in this file
- For production, consider PostgreSQL or another server-based database
