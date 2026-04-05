from django.urls import path
from .views import (
    RegisterView, LoginView,
    TransactionListCreateView, TransactionDetailView,
    SummaryView,
    UserListView, UserDeleteView,
)

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),

    # Transactions
    path("transactions/", TransactionListCreateView.as_view()),
    path("transactions/<int:pk>/", TransactionDetailView.as_view()),

    # Analytics
    path("analytics/summary/", SummaryView.as_view()),

    # Users
    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserDeleteView.as_view()),
]
