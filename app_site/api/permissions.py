from rest_framework.permissions import BasePermission
from django.utils.translation import ugettext_lazy as _


class IsObjectOwner(BasePermission):
    message = _('Você deve ser o alterar apenas os seus requistros')

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCatadorOrCollectOwner(BasePermission):
    message = _('Você precisa ser o catador ou usuário da coleta')

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user) or (obj.carroceiro.user == request.user)

