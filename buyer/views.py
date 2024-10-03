from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsSuperAdmin, IsBuyer
from buyer.models import PurchaseRequest
from buyer.serializers import UserSerializer, PurchaseRequestSerializer


# Create your views here.

class CustomAPIViewMixin:
    def create_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        response_data = {
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)


class BuyersListAPIView(CustomAPIViewMixin, generics.ListAPIView):
    """
        API view to handle listing Buyers.
    """
    queryset = User.objects.filter(role='Buyer', is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def list(self, request, *args, **kwargs):
        """
                Handle GET requests to list all Buyers.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.create_response(data=serializer.data, message="Buyers retrieved successfully")


class BuyerRetrieveUpdateDestroyAPIView(CustomAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        API view for retrieving, updating, or soft deleting a Buyer.
        This view handles GET, PUT/PATCH, and DELETE requests for individual Buyer.
        Permission required to access this view.
    """
    queryset = User.objects.filter(role='Buyer', is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve a specific Buyer instance.

            Args:
                request (Request): The request object contains request data.

            Returns:
                Response: A Response object contains the Buyer data and a success message.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.create_response(data=serializer.data, message="Buyer retrieved successfully")

    def update(self, request, *args, **kwargs):
        """
            Update a specific Buyer instance.

            Args:
                request (Request): The request object contains updated Buyer.

            Returns:
                Response: A DRF Response object contains the serialized Buyer data and a success message.
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.create_response(data=serializer.data, message="Buyer updated successfully")

    def destroy(self, request, *args, **kwargs):
        """
           Soft Delete a specific Buyer.

           Args:
               request (Request): The request object.

           Returns:
               Response: A DRF Response object with a success message
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return self.create_response(message="Buyer deleted successfully")


class PurchaseRequestListCreateAPIView(CustomAPIViewMixin, generics.ListCreateAPIView):
    """
        API view to handle listing and creating Purchase Request.
    """
    queryset = PurchaseRequest.objects.all()
    serializer_class = PurchaseRequestSerializer
    permission_classes = [IsAuthenticated, IsBuyer]

    def list(self, request, *args, **kwargs):
        """
                Handle GET requests to list all Purchase Request made.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.create_response(data=serializer.data, message="Purchase Request retrieved successfully")

    def create(self, request, *args, **kwargs):
        """
            Handle POST request to create Purchase Request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.create_response(data=serializer.data, message="Purchase Request created successfully",
                                    status_code=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Automatically save the buyer as the currently authenticated user.
        """
        serializer.save(buyer=self.request.user)


class BuyerDashboardView(CustomAPIViewMixin, APIView):
    """
           API view for retrieving KPI Dashboard of Buyer.
           This view handles GET requests for individual Buyer.
           Permission required to access this view.
    """
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        """
            Handle GET requests to retrieve KPI data for individual Buyer.
        """
        buyer = request.user
        purchases = PurchaseRequest.objects.filter(buyer=buyer)
        data = {
            'total_purchases': purchases.count(),
            'in_process': purchases.filter(status='In-Process').count(),
            'approved': purchases.filter(status='Approved').count(),
            'rejected': purchases.filter(status='Rejected').count()
        }
        return self.create_response(data=data, message="Buyer KPI dashboard retrieved successfully")
