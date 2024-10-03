from rest_framework import serializers

from accounts.models import User
from buyer.models import PurchaseRequest


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for handling the User model for Buyers and Sellers.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SellerSerializer(serializers.ModelSerializer):
    """
    Serializer for representing the seller details in a Purchase Request.
    """

    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class PurchaseRequestSerializer(serializers.ModelSerializer):
    """
       Serializer for handling the Purchase Request model for Buyers to create purchase request
       with additional seller details in the response.
    """
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Seller'), write_only=True)
    seller_details = SellerSerializer(source='seller', read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = ['id', 'seller', 'seller_details', 'description', 'total_amount', 'status']
        read_only_fields = ['id', 'status']

    # Object-level validation
    def validate(self, data):
        request = self.context.get('request')
        description = data.get('description')
        total_amount = data.get('total_amount')
        if request.method == "POST":
            if not request.data.get('seller'):
                raise serializers.ValidationError({
                    'seller': 'Seller is required.'
                })
            # Validate description
            if not description:
                raise serializers.ValidationError({
                    'description': 'Description is required.'
                })

            # Validate total_amount
            if total_amount is None:
                raise serializers.ValidationError({
                    'total_amount': 'Total amount is required.'
                })
            if total_amount <= 0:
                raise serializers.ValidationError({
                    'total_amount': 'Total amount must be a positive value.'
                })

        return data
