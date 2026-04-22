# Maison Verdant — Restaurant Table Booking System

A clean, full-featured restaurant reservation web app built with Flask and SQLite.

## Features
- Browse available tables by date & time (live AJAX check)
- Book a table with guest details and special requests
- Confirmation page with booking summary
- Admin dashboard to view and cancel bookings
- SQLite database (no setup needed)

## Setup & Run

```bash
# 1. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open your browser at: **http://localhost:5000**

## Pages
| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/book` | Reservation form |
| `/confirmation/<id>` | Booking confirmed page |
| `/admin` | Admin dashboard |
| `/api/availability?date=YYYY-MM-DD&time=HH:MM` | JSON availability endpoint |

## Tech Stack
- **Backend**: Python / Flask
- **Database**: SQLite (auto-created as `bookings.db`)
- **Frontend**: HTML, CSS, Vanilla JS
- **Fonts**: Cormorant Garamond + Jost (Google Fonts)
