# Finance Tracker API

A clean, role-based finance tracking backend built with **Django 5** and **Django REST Framework**. Designed to manage personal financial records, generate analytics summaries, and enforce role-based access control across all endpoints.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Database | SQLite (zero config, file-based) |
| Authentication | JWT — `djangorestframework-simplejwt` |
| ORM | Django ORM |
| Python | 3.10+ |

---

## Project Structure

```
zorvyn/
├── manage.py
├── requirements.txt
├── core/
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Root URL routing
│   └── wsgi.py
└── finance/
    ├── models.py           # User (with roles) + Transaction
    ├── serializers.py      # Input validation and response shaping
    ├── views.py            # All API views
    ├── urls.py             # App-level URL routing
    ├── permissions.py      # Role-based permission classes
    ├── services.py         # Analytics and summary business logic
    ├── admin.py            # Django admin panel setup
    └── management/
        └── commands/
            └── seed.py     # One-command database seeding
```

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/samyukthaareddy/zorvyn.git
cd zorvyn

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Seed sample data (creates users + transactions)
python manage.py seed

# 6. Start the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

---

## Seed Accounts

Running `python manage.py seed` creates the following accounts along with 8 sample transactions assigned to the admin user.

| Username | Password | Role |
|---|---|---|
| admin | admin123 | admin |
| analyst | analyst123 | analyst |
| viewer | viewer123 | viewer |

---

## Roles and Permissions

Three roles are supported. Each role builds on the previous one.

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

## API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user with a role |
| POST | `/api/auth/login/` | Login and receive JWT access + refresh tokens |

**Register request body:**
```json
{
  "username": "john",
  "password": "secret123",
  "role": "viewer"
}
```

**Login response:**
```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

Use the access token in all subsequent requests:
```
Authorization: Bearer <access_token>
```

---

### Transactions

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/transactions/` | all roles | List transactions with filters and pagination |
| POST | `/api/transactions/` | admin | Create a new transaction |
| GET | `/api/transactions/{id}/` | all roles | Retrieve a single transaction |
| PATCH | `/api/transactions/{id}/` | admin | Partially update a transaction |
| DELETE | `/api/transactions/{id}/` | admin | Delete a transaction |

**Filtering and pagination query params:**

| Param | Type | Example |
|---|---|---|
| `type` | string | `income` or `expense` |
| `category` | string | `Groceries` |
| `start_date` | date | `2024-01-01` |
| `end_date` | date | `2024-03-31` |
| `page` | integer | `1` |
| `page_size` | integer | `10` (max 100) |

**Transaction request body:**
```json
{
  "amount": 1500.00,
  "type": "income",
  "category": "Freelance",
  "date": "2024-05-01",
  "notes": "Website project payment"
}
```

---

### Analytics

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/analytics/summary/` | all roles | Full financial summary for the logged-in user |

**Summary response:**
```json
{
  "total_income": 9500.00,
  "total_expenses": 1550.00,
  "balance": 7950.00,
  "category_breakdown": {
    "Salary": 8000.00,
    "Freelance": 1500.00,
    "Groceries": 350.00
  },
  "monthly_totals": {
    "2024-01": { "income": 5000.00, "expense": 200.00 },
    "2024-02": { "income": 1500.00, "expense": 300.00 }
  },
  "recent_transactions": [...]
}
```

---

### Users (Admin only)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/` | List all registered users |
| DELETE | `/api/users/{id}/` | Delete a user (cannot delete yourself) |

---

## Django Admin Panel

A fully functional Django admin panel is available for managing users and transactions directly.

```
URL:      http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

---

## Assumptions

- Transactions are scoped per user — each user can only view and manage their own records.
- Roles are assigned at registration time and stored on the user model.
- SQLite is used for simplicity. To switch to PostgreSQL, update the `DATABASES` setting in `core/settings.py` — no other changes needed.
- All amounts must be positive. Dates must follow ISO 8601 format (`YYYY-MM-DD`).
- JWT access tokens expire after 60 minutes. Use the refresh token to obtain a new access token.
