from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        #Uzytkownik moze edytowac koktajl tylko jezeli on go stworzyl
        return obj.author == request.user or request.user.is_staff