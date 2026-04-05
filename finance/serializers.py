from rest_framework import serializers
from .models import User, Transaction


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "password", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role")


class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Transaction
        fields = ("id", "owner", "amount", "type", "category", "date", "notes")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_category(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category cannot be blank.")
        return value.strip()


class TransactionUpdateSerializer(TransactionSerializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    type = serializers.ChoiceField(choices=Transaction.Type.choices, required=False)
    category = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
