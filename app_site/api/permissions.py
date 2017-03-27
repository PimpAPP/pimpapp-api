from rest_framework.permissions import BasePermission
from django.utils.translation import ugettext_lazy as _


class IsObjectOwner(BasePermission):
    message = _('Você pode alterar apenas os seus registros')

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if hasattr(obj, 'user'):
                return obj.user == request.user
            elif hasattr(obj, 'author'):
                return obj.author == request.user
            else:
                self.message = _('A permissão não pode ser determinada')
                return False
        elif request.method == 'GET':
            return True


class IsCatadorOrCollectOwner(BasePermission):
    message = _('Você precisa ser o catador ou usuário da coleta')

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user) or (obj.carroceiro.user == request.user)

