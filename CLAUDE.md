# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly is a Flask-based expense tracking web application. The project is structured as a learning exercise where students implement features step-by-step (database setup, authentication, CRUD operations).

## Commands

**Run the application:**
```bash
python app.py
```
The app runs on `http://localhost:5001` with debug mode enabled.

**Virtual environment:**
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Run tests:**
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -v -k test_name    # Run specific test by name
pytest tests/test_file.py # Run a specific test file
```

## Project Constraints

- **Vanilla JavaScript only** - No frameworks or libraries (React, Vue, jQuery, etc.). Use plain DOM APIs, `fetch()`, and standard browser features.

## Architecture

- **app.py** - Flask application with routes. Currently implements landing, register, login, terms, and privacy pages. Placeholder routes exist for logout, profile, and expense CRUD operations (to be implemented by students).
- **database/db.py** - Database layer (currently a stub). Students implement:
  - `get_db()` - SQLite connection with row_factory and foreign keys enabled
  - `init_db()` - Creates tables using CREATE TABLE IF NOT EXISTS
  - `seed_db()` - Inserts sample development data
- **templates/** - Jinja2 HTML templates using template inheritance (`base.html` as the base)
- **static/css/style.css** - All styles in a single file with CSS variables for theming
- **static/js/main.js** - JavaScript (currently empty stub for future features)

## Key Patterns

- Template inheritance: All pages extend `base.html` which provides navbar, footer, and common blocks
- Form submissions use POST to corresponding routes (e.g., `/register`, `/login`)
- Error messages passed to templates via `error` context variable
- SQLite database at `expense_tracker.db` (gitignored)
