# Finance Tracker API

A role-based finance tracking backend built with **Django** and **Django REST Framework**.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Database | SQLite |
| Auth | JWT via djangorestframework-simplejwt |
| ORM | Django ORM |

---

## Project Structure

```
zorvyn/
├── manage.py
├── requirements.txt
├── finance.db                  # auto-created on first run
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── finance/
    ├── models.py               # User (with roles) + Transaction
    ├── serializers.py          # Input validation and output shaping
    ├── views.py                # All API views
    ├── urls.py                 # URL routing
    ├── permissions.py          # Role-based permission classes
    ├── services.py             # Analytics business logic
    ├── admin.py                # Django admin registration
    └── management/
        └── commands/
            └── seed.py         # Seed command
```

---

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed sample data
python manage.py seed

# 5. Start the server
python manage.py runserver
```

API is live at `http://127.0.0.1:8000/api/`

---

## Seed Accounts

| Username | Password | Role |
|---|---|---|
| admin | admin123 | admin |
| analyst | analyst123 | analyst |
| viewer | viewer123 | viewer |

---

## Roles and Permissions

| Action | viewer | analyst | admin |
|---|---|---|---|
| View own transactions | ✅ | ✅ | ✅ |
| Filter transactions | ✅ | ✅ | ✅ |
| View analytics summary | ✅ | ✅ | ✅ |
| Create transaction | ❌ | ❌ | ✅ |
| Update transaction | ❌ | ❌ | ✅ |
| Delete transaction | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## API Endpoints

### Auth
| Method | URL | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login, returns JWT access + refresh tokens |

### Transactions
| Method | URL | Access | Description |
|---|---|---|---|
| GET | `/api/transactions/` | all | List transactions (paginated + filtered) |
| POST | `/api/transactions/` | admin | Create a transaction |
| GET | `/api/transactions/{id}/` | all | Get a single transaction |
| PATCH | `/api/transactions/{id}/` | admin | Partially update a transaction |
| DELETE | `/api/transactions/{id}/` | admin | Delete a transaction |

**Filter query params:** `type`, `category`, `start_date`, `end_date`, `page`, `page_size`

### Analytics
| Method | URL | Access | Description |
|---|---|---|---|
| GET | `/api/analytics/summary/` | all | Financial summary |

**Summary includes:** `total_income`, `total_expenses`, `balance`, `category_breakdown`, `monthly_totals`, `recent_transactions`

### Users (Admin only)
| Method | URL | Description |
|---|---|---|
| GET | `/api/users/` | List all users |
| DELETE | `/api/users/{id}/` | Delete a user |

---

## Quick Test Flow

```bash
# 1. Login
POST /api/auth/login/
{ "username": "admin", "password": "admin123" }

# 2. Copy the access token, add to header:
Authorization: Bearer <access_token>

# 3. Create a transaction
POST /api/transactions/
{ "amount": 1200, "type": "income", "category": "Salary", "date": "2024-05-01" }

# 4. View summary
GET /api/analytics/summary/

# 5. Filter transactions
GET /api/transactions/?type=expense&start_date=2024-01-01&end_date=2024-04-30

# 6. Paginate
GET /api/transactions/?page=1&page_size=5
```

---

## Django Admin Panel

```
http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

---

## Assumptions

- Each transaction is scoped to the user who created it; users only see their own records.
- Roles are assigned at registration and enforced via DRF permission classes.
- SQLite is used for simplicity — changing `DATABASES` in `core/settings.py` is all that's needed to switch to PostgreSQL.
- Amounts must be positive decimals; dates follow ISO 8601 (`YYYY-MM-DD`).
- JWT access tokens expire after 60 minutes.
