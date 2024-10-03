from rest_framework.permissions import BasePermission


class IsBuyer(BasePermission):
    """
    Custom permission to only allow users who has role buyer.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_active and request.user.role == 'Buyer')


class IsSuperAdmin(BasePermission):
    """
    Custom permission to only allow users who can add items.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_active and request.user.role == 'Superadmin')


class IsSeller(BasePermission):
    """
    Custom permission to only allow users who can add items.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_active and request.user.role == 'Seller')