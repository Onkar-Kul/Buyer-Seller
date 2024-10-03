from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsSuperAdmin, IsSeller
from buyer.models import PurchaseRequest
from buyer.serializers import UserSerializer
from seller.serializers import PurchaseRequestSellerSerializer


# Create your views here.

class CustomAPIViewMixin:
    def create_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        response_data = {
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)


class SellerListAPIView(CustomAPIViewMixin, generics.ListAPIView):
    """
        API view to handle listing Sellers.
    """
    queryset = User.objects.filter(role='Seller', is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def list(self, request, *args, **kwargs):
        """
                Handle GET requests to list all Sellers.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.create_response(data=serializer.data, message="Sellers retrieved successfully")


class SellerRetrieveUpdateDestroyAPIView(CustomAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        API view for retrieving, updating, or soft deleting a Seller.
        This view handles GET, PUT/PATCH, and DELETE requests for individual Seller.
        Permission required to access this view.
    """
    queryset = User.objects.filter(role='Seller', is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve a specific Seller instance.

            Args:
                request (Request): The request object contains request data.

            Returns:
                Response: A Response object contains the Seller data and a success message.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.create_response(data=serializer.data, message="Seller retrieved successfully")

    def update(self, request, *args, **kwargs):
        """
            Update a specific Seller instance.

            Args:
                request (Request): The request object contains updated seller.

            Returns:
                Response: A DRF Response object contains the serialized seller data and a success message.
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.create_response(data=serializer.data, message="Seller updated successfully")

    def destroy(self, request, *args, **kwargs):
        """
           Soft Delete a specific Seller.

           Args:
               request (Request): The request object.

           Returns:
               Response: A DRF Response object with a success message
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return self.create_response(message="Seller deleted successfully")


class SellerDashboardView(CustomAPIViewMixin, APIView):
    """
            API view for retrieving KPI Dashboard of Seller.
            This view handles GET requests for individual Seller.
            Permission required to access this view.
    """
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        """
            Handle GET requests to retrieve KPI data for individual Seller.
        """
        seller = request.user
        purchases = PurchaseRequest.objects.filter(seller=seller)
        data = {
            'total_purchases': purchases.count(),
            'in_process': purchases.filter(status='In-Process').count(),
            'approved': purchases.filter(status='Approved').count(),
            'rejected': purchases.filter(status='Rejected').count()
        }
        return self.create_response(data=data, message="Seller KPI dashboard retrieved successfully")


class SellerPurchaseRequestListView(generics.ListAPIView):
    """
    View for a seller to list all purchase requests belonging to them.
    """
    serializer_class = PurchaseRequestSellerSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        # Filter the purchase requests by the seller who is currently logged in
        return PurchaseRequest.objects.filter(seller=self.request.user)


class SellerUpdatePurchaseRequestStatusView(CustomAPIViewMixin, generics.RetrieveUpdateAPIView):
    """
    View for a seller to update the status of their purchase requests.
    """
    serializer_class = PurchaseRequestSellerSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        # Only allow the seller to update requests that belong to them
        return PurchaseRequest.objects.filter(seller=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve a specific Sale Request instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.create_response(data=serializer.data, message="Sale Request retrieved successfully")

    def update(self, request, *args, **kwargs):
        # Handle the status update for the purchase request
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Sale Request status updated successfully'}, status=status.HTTP_200_OK)
