from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from finance.models import User, Transaction


class Command(BaseCommand):
    help = "Seed the database with an admin user and sample transactions"

    def handle(self, *args, **kwargs):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("Seed data already exists. Skipping.")
            return

        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            role=User.Role.ADMIN,
        )

        User.objects.create_user(username="viewer", password="viewer123", role=User.Role.VIEWER)
        User.objects.create_user(username="analyst", password="analyst123", role=User.Role.ANALYST)

        sample = [
            Transaction(owner=admin, amount=5000, type=Transaction.Type.INCOME,  category="Salary",    date=parse_date("2024-01-01"), notes="January salary"),
            Transaction(owner=admin, amount=200,  type=Transaction.Type.EXPENSE, category="Groceries", date=parse_date("2024-01-05"), notes="Weekly groceries"),
            Transaction(owner=admin, amount=1500, type=Transaction.Type.INCOME,  category="Freelance", date=parse_date("2024-02-10"), notes="Web project"),
            Transaction(owner=admin, amount=300,  type=Transaction.Type.EXPENSE, category="Utilities", date=parse_date("2024-02-15"), notes="Electricity bill"),
            Transaction(owner=admin, amount=100,  type=Transaction.Type.EXPENSE, category="Transport", date=parse_date("2024-03-01"), notes="Monthly pass"),
            Transaction(owner=admin, amount=800,  type=Transaction.Type.EXPENSE, category="Rent",      date=parse_date("2024-03-05"), notes="March rent"),
            Transaction(owner=admin, amount=3000, type=Transaction.Type.INCOME,  category="Salary",    date=parse_date("2024-04-01"), notes="April salary"),
            Transaction(owner=admin, amount=150,  type=Transaction.Type.EXPENSE, category="Groceries", date=parse_date("2024-04-10"), notes="Supermarket"),
        ]
        Transaction.objects.bulk_create(sample)

        self.stdout.write(self.style.SUCCESS(
            "Seeded: admin/admin123 | viewer/viewer123 | analyst/analyst123"
        ))
