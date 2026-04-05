from collections import defaultdict
from .models import Transaction


def get_summary(user):
    transactions = Transaction.objects.filter(owner=user)

    total_income = sum(float(t.amount) for t in transactions if t.type == Transaction.Type.INCOME)
    total_expense = sum(float(t.amount) for t in transactions if t.type == Transaction.Type.EXPENSE)

    category_breakdown = defaultdict(float)
    monthly_totals = defaultdict(lambda: {"income": 0.0, "expense": 0.0})

    for t in transactions:
        category_breakdown[t.category] += float(t.amount)
        month_key = t.date.strftime("%Y-%m")
        monthly_totals[month_key][t.type] += float(t.amount)

    recent = transactions.order_by("-date")[:5]

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
        "category_breakdown": dict(category_breakdown),
        "monthly_totals": {k: dict(v) for k, v in monthly_totals.items()},
        "recent_transactions": [
            {
                "id": t.id,
                "amount": float(t.amount),
                "type": t.type,
                "category": t.category,
                "date": str(t.date),
            }
            for t in recent
        ],
    }
