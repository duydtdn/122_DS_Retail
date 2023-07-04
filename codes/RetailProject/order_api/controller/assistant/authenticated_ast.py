from rest_framework import permissions
from rest_framework_role_filters.role_filters import RoleFilter
from rest_framework_role_filters.viewsets import RoleFilterModelViewSet
from rest_framework.permissions import IsAdminUser

class AdminRoleFilter(RoleFilter):
    role_id = 'admin'

class CustomerRoleFilter(RoleFilter):
    role_id = 'customer'

    def get_allowed_actions(self, request, view, obj=None):
        return ['get','list','retrieve']

class EmployeeRoleFilter(RoleFilter):
    role_id = 'employee'
    def get_allowed_actions(self, request, view, obj=None):
        return ['list', 'retrieve', 'update', 'partial_update']

class ManagerRoleFilter(RoleFilter):
    role_id = 'store_manager'
    def get_allowed_actions(self, request, view, obj=None):
        return ['create', 'list', 'retrieve', 'update', 'partial_update', 'destroy']


class ModelViewSet(RoleFilterModelViewSet):
    role_filter_classes = [AdminRoleFilter, ManagerRoleFilter,EmployeeRoleFilter, CustomerRoleFilter]

    def get_role_id(self, request):
        if request.user.is_anonymous:
            return 'customer'
        if request.user.is_admin:
            return 'admin'
        return request.user.role

class AllowAnyPutDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True

class ManagerOfStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
            # return True
        if request.user.role == 'store_manager':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.store_operate == request.user.store_operate:
            return True
        return False