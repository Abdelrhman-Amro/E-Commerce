from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Check if the user is a seller.
    """

    def has_permission(self, request, view):

        return request.user.role == "seller"


class IsStoreOwner(BasePermission):
    """
    Check if the user is the owner of the store.
    """

    def has_object_permission(self, request, view, obj):
        print(obj.user)
        print(request.user)
        return obj.user == request.user
