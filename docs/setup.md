# Setup Guide

This guide walks you through setting up the Inventory System Practice project on your local machine.

## 1. Clone the Repository

```bash
git clone <repository-url>
cd inventory-system-practice
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

This creates an isolated Python environment in the `.venv` folder.

## 3. Activate the Virtual Environment

### Windows with Git Bash

```bash
source .venv/Scripts/activate
```

You should see `(.venv)` at the beginning of your terminal prompt.

### Windows with PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the Application

```bash
uvicorn main:app --reload
```

The `--reload` flag restarts the server automatically when you change code (useful during development).

## 6. Open the Application

- **Web interface:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 7. API Documentation

FastAPI provides interactive API docs at `/docs`. From there you can:

- See all available endpoints
- Test API calls directly in the browser
- View request/response schemas

## Troubleshooting

### Database Issues

The SQLite database is created automatically at `instance/inventory.db` on first startup.

If you encounter database errors:

1. Stop the server (Ctrl+C)
2. Delete the database file:
   ```bash
   rm instance/inventory.db
   ```
3. Restart the server:
   ```bash
   uvicorn main:app --reload
   ```

The app will recreate the database and insert sample data.

### Port Already in Use

If port 8000 is busy, use a different port:

```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found Errors

Make sure your virtual environment is activated and dependencies are installed:

```bash
source .venv/Scripts/activate   # Git Bash
pip install -r requirements.txt
```

Run commands from the project root directory (where `main.py` is located).
