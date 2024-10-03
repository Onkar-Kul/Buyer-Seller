from rest_framework import serializers

from accounts.models import User
from buyer.models import PurchaseRequest


class BuyerSerializer(serializers.ModelSerializer):
    """
    Serializer for representing the seller details in a Purchase Request.
    """

    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class PurchaseRequestSellerSerializer(serializers.ModelSerializer):
    """
       Serializer for handling the Purchase Request model for Seller to change the status
       with additional buyer details in the response.
    """

    buyer = BuyerSerializer(read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = ['id', 'buyer', 'description', 'total_amount', 'status']
        read_only_fields = ['id', 'description', 'total_amount']

    def validate_status(self, value):
        """
        Validate that the status is provided and it's a valid value.
        """
        if not value:
            raise serializers.ValidationError("Status is required.")

        # You can add further validation to check if the status is one of the allowed values
        allowed_statuses = ['In-Process', 'Approved', 'Rejected']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Invalid status. Allowed values are: {', '.join(allowed_statuses)}")

        return value

    def update(self, instance, validated_data):
        """
        Override the update method to enforce status validation.
        """
        status = validated_data.get('status', None)

        if status is None:
            raise serializers.ValidationError({"status": "Status is required."})

        # Validate status if it's being updated
        self.validate_status(status)

        # Perform the update
        instance = super().update(instance, validated_data)
        return instance
