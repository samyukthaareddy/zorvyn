from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, Transaction
from .serializers import RegisterSerializer, UserSerializer, TransactionSerializer, TransactionUpdateSerializer
from .permissions import IsAdmin, IsAnalystOrAbove, IsViewerOrAbove
from .services import get_summary


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


# ── Transactions ───────────────────────────────────────────────────────────────

class TransactionListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsViewerOrAbove()]

    def get(self, request):
        qs = Transaction.objects.filter(owner=request.user)

        tx_type = request.query_params.get("type")
        category = request.query_params.get("category")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if tx_type:
            qs = qs.filter(type=tx_type)
        if category:
            qs = qs.filter(category__icontains=category)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        page = int(request.query_params.get("page", 1))
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        start = (page - 1) * page_size
        total = qs.count()
        qs = qs[start: start + page_size]

        return Response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": TransactionSerializer(qs, many=True).data,
        })

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDetailView(APIView):

    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            return [IsAdmin()]
        return [IsViewerOrAbove()]

    def get_object(self, pk, user):
        try:
            return Transaction.objects.get(pk=pk, owner=user)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk):
        tx = self.get_object(pk, request.user)
        if not tx:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(TransactionSerializer(tx).data)

    def patch(self, request, pk):
        tx = self.get_object(pk, request.user)
        if not tx:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionUpdateSerializer(tx, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        tx = self.get_object(pk, request.user)
        if not tx:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        tx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Analytics ─────────────────────────────────────────────────────────────────

class SummaryView(APIView):
    permission_classes = [IsViewerOrAbove]

    def get(self, request):
        return Response(get_summary(request.user))


# ── Users (Admin only) ────────────────────────────────────────────────────────

class UserListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)


class UserDeleteView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, pk):
        if pk == request.user.pk:
            return Response({"detail": "Cannot delete yourself."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
