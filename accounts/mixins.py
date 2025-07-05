from django.core.exceptions import PermissionDenied

class StoreManagerMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_store_manager:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class CustomerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)