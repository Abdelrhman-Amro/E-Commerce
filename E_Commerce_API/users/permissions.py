from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Check if the user is a seller.
    """

    def has_permission(self, request, view):

        return request.user.role == "seller"


class IsMarketOwner(BasePermission):
    """
    Check if the user is the owner of the market.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user
